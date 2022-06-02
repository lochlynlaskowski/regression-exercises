import pandas as pd
import numpy as np
import os
from env import get_db_url
from sklearn.model_selection import train_test_split

def get_zillow_data():
    '''Returns a dataframe of all single family residential properties from 2017.'''
    filename = "zillow.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        sql_query = '''
        SELECT properties_2017.bedroomcnt AS Number_of_Bedrooms,
        properties_2017.bathroomcnt AS Number_of_Bathrooms,
        properties_2017.calculatedfinishedsquarefeet AS Square_Footage, 
        properties_2017.taxvaluedollarcnt AS Tax_Appraised_Value, 
        properties_2017.yearbuilt AS Year_Built, 
        properties_2017.taxamount AS Tax_Assessed, properties_2017.fips AS County_Code
        FROM properties_2017
        JOIN propertylandusetype using (propertylandusetypeid)
        WHERE propertylandusedesc = "Single Family Residential";
        '''
        df = pd.read_sql(sql_query, get_db_url('zillow'))
        
    return df


def prepare_zillow_data(df):
    ''' Prepares zillow data'''
    #drop null values
    df = df.dropna()
    # change fips codes to actual county name
    def counties(row):  
        if row['County_Code'] == 6037.00:
            return 'Los Angeles County'
        elif row['County_Code'] == 6059.00:
            return 'Orange County'
        elif row['County_Code'] == 6111.00:
            return 'Ventura County'
    df['County_Code'] = df.apply(lambda row: counties(row), axis=1)
    df.rename(columns = {'County_Code':'County'}, inplace = True)
    #limit homes to 1 bed , .5 bath, and at least 120sq ft     
    df = df[df.Square_Footage > 120]
    df = df[df.Number_of_Bedrooms > 0]
    df = df[df.Number_of_Bathrooms >0]
    # convert floats to int except taxes and bedrooms
    df['Year_Built'] = df['Year_Built'].astype(int)
    df['Square_Footage'] = df['Square_Footage'].astype(int)
    df['Number_of_Bedrooms'] = df['Number_of_Bedrooms'].astype(int)
    df['Tax_Appraised_Value'] = df['Tax_Appraised_Value'].astype(int)
    # handle outliers: square footage less than 56,000 and 7 beds and 7.5 baths or less
    # df = df[df.Number_of_Bedrooms <=7]
    # df = df[df.Number_of_Bathrooms <=7.5]
    # df = df[df.Square_Footage <=56_000]
    # df = df[df.Tax_Appraised_Value <=3_500_000]

    # save as .csv
    # df.to_csv('zillow.csv')
    return df

def split_zillow_data(df):
    ''' This function splits the cleaned dataframe into train, validate, and test 
    datasets and statrifies based on the target - Tax_Appraised_Value.'''

    train_validate, test = train_test_split(df, test_size=.2, 
                                        random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3, 
                                   random_state=123)
    
    return train, validate, test

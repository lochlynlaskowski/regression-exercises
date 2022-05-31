import pandas as pd
import numpy as np
import os
from env import get_db_url

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
        properties_2017.taxamount AS Tax_Assessed, properties_2017.fips
        FROM properties_2017
        JOIN propertylandusetype using (propertylandusetypeid)
        WHERE propertylandusedesc = "Single Family Residential";
        '''
        df = pd.read_sql(sql_query, get_db_url('zillow'))
        df.to_csv(filename)
    return df




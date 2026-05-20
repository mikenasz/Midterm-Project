from country_codes import country_codes
import pandas as pd

#Keep the columns we need such as year, fertility rate, population, etc.
def keep_columns(df):
    
    df = df[['#YR', 'GEO_ID', 'POP_DENS', 'TFR', 'GR', 'E0', 'POP']]
    return df
    
#Transform GEO_ID to country name by slicing last 2 chars and mapping to our country codes dictionary
def transform_country(df):
    
    df['GEO_ID'] = df['GEO_ID'].str[-2:]
    print(df['GEO_ID'].head())
    df['country_name'] = df['GEO_ID'].map(country_codes)
    df = df[df['country_name'].notna()]
    return df

#Keep records only from 1990 - 2025
def filter_years(df):
    df = df[df['#YR'] >= 1990]
    df = df[df['#YR'] <= 2026]
    return df

#Drop all nulls that are left
def drop_nulls(df):
    df = df.dropna()
    return df
    
def transform_df(df):
    
    df = keep_columns(df)
    df = transform_country(df)
    df = filter_years(df)
    df = drop_nulls(df)
    
    print(f"Row count after transformation {len(df)} ")
    return df
    
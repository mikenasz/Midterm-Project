
import pandas as pd
from sqlalchemy import create_engine
from dynaconf import Dynaconf


#Load the transformed data into the country table in our database, get only unique countries
def load_country(df, engine):
    
    df_country = df[['country_name']].drop_duplicates()
    df_country.to_sql('country', engine, if_exists = 'append', index = False)
    print(f"Country table loaded with {len(df_country)} records")

#Get country ids from country merge to get df with id
def get_country_ids(df, engine):
    df_country = pd.read_sql('SELECT country_id, country_name FROM country', engine)
    df_merged = df.merge(df_country, on = 'country_name', how = 'inner')
    return df_merged
    
#Load the transformed data into the population_metric table in our database, merge to country table to get country_id as foreign key
def load_population_metric(df, engine):
    
    df = get_country_ids(df,engine)
    pop_cols = df[['total_population', 'year', 'population_density', 'growth_rate', 'country_id']]
    pop_cols.to_sql('population_metric', engine, if_exists = 'append', index = False)
    print(f"Population metric table loaded with {len(pop_cols)} records")
    
#Load health metric table, get country ids from country table
def load_health_metric(df, engine):
    
    df = get_country_ids(df,engine)
    df_health = df[['fertility_rate', 'life_expectancy', 'year', 'country_id']]
    df_health.to_sql('health_metric', engine, if_exists = 'append', index = False)
    print(f"Health metric table loaded with {len(df_health)} records")
    
def load(df, engine):
    load_country(df, engine)
    load_population_metric(df, engine)
    load_health_metric(df,engine)
    
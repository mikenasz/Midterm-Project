from etl import extract, transform, load
import pandas
import os
from dynaconf import Dynaconf
import psycopg
from sqlalchemy import create_engine

def build_engine():
    settings = Dynaconf(
        envvar_prefix="DB",
        settings_files=['.env'],
        load_dotenv=True
    )
    return create_engine(settings.ENGINE_URL, echo=False)

def main():
    df = extract.extract_file()
    df = transform.transform_df(df)
    print("New DF")
    print(df.head())
    df = load.load(df,build_engine())
    
    

if __name__ == "__main__":
    main()
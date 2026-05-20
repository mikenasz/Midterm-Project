# Load raw data from IDB into pandas DF
import pandas as pd


#Extract the 5 year idb file into df
def extract_file():
    df = pd.read_csv("data/idb5yr.txt", sep= "|")
    print(df.head())
    print(f'Data extracted with row count {len(df)}')
    return df






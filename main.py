from etl import extract, transform, load
import pandas

def main():
    df = extract.extract_file()
    df = transform.transform_df(df)
    print("New DF")
    print(df.head())
    
    

if __name__ == "__main__":
    main()
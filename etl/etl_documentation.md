## ETL Documentation

## Introduction

The problem and purpose of this ETL pipeline is to extract data from the IDB, and get relevant data to test our hypothesis which is, countries that have a higher life expectancy and higher population density tend to have a lower fertility rate than countries that have a lower life expectancy and lower population density. Our major source of data is the IDB downloadable dataset.

The reason behind transformation is the raw dataset is large, the raw data has 253013 records. In addition, there are many columns we don't need for our analysis, and we need to transform GEO_ID to get the country name.

## Data Sources

I found this data source by browsing on the census.gov website and finding the International Database, I accessed the data on 5/18, and  I first explored the web interactive tool to explore the data and see what metrics are in the dataset. From there, I used the download dataset option and extracted the zip file into my program. 

**Source**

United States Census Bureau. (2025). *International Database (IDB): World population estimates and projections* [Data file]. U.S. Department of Commerce. https://www.census.gov/programs-surveys/international-programs/about/idb.html

## Extraction

I extracted the data by first using the downloaded zip file containing the IDB dataset, from there I put the files into a data directory where it contains the idb5yr.txt, and idbsingleyear.txt. I looked through both files and I realized the 5yr file was the one I needed as it contained population data for multiple years of each country. 

**Steps**

1. Identify the delimiter in the file, in this case it was the "|" character
2. Utilize the pandas readcsv method, make sure to pass the delimiter as the separator.
3. Return the pandas df containing all of the raw data, pass it to our transformation script
4. Validate the extraction by printing out length of the df.

## Transformation

After the raw data has been extracted to a pandas df, the data could not be used as is since it was messy and contained unnecessary data for my analysis. I first decided what exact columns I needed by looking at the documentation to see which columns had data on population and health metrics I needed, from there I kept a list of each column name and transformed it that way. I also did change all of the names to match up with my DDL, but I did not change any formats.

**Steps**

1. Transform the df by creating a new one containing only the necessary columns from the raw data.
2. Transform the GEO_ID column to return a country name instead of a geocode, do this by slicing to get the last 2 characters utilize the helper country_codes dictionary to map each code to country name. Drop any na values after mapping
3. Filter the df by year range to keep data records from 1990-2026.
4. Drop any na values left, and also drop the GEO_ID column from our df.
5. Rename columns to match up with DDL and idb_data schema diagram.
6. Return the transformed df and pass to our load script.

## Load

After transforming the data, I went on to load the df into a schema I created called idb_data. Before running the load script, I made sure I created the tables in Postgres and ran the DDL, also before running anything I made sure I created an .env file containing database credentials, and used this to create an engine to establish a connection between my ETL and Postgres server. 

**Steps**

1. Load into country table first as this will be referenced by our population and health metric tables. We need to drop any final duplicates to ensure only unique countries will be populated to our country table. 
2. Load into children tables, get country_id by running a sql query to find all countries and their id, merge the df into a new one containing the country_id so we can easily load population and health metric data with country relation.
3. Grab necessary columns for population_metric and filter df, load the df into database.
4. Repeat step 3 for health metric tables.
5. Once load is complete, run a SQL query to see if data has been populated into Postgres.
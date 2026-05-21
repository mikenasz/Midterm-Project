Hypothesis

Countries that have a higher life expectancy and higher population density tend to have a lower fertility rate than countries that have a lower life expectancy and population density.

Evaluating the dataset
- Extract data from the IDB database zip file, evaluate needed columns and fields such as population density, fertility rate, etc. Look for USA data too?
- Time estimate : 3 hrs
- Actual 4 hrs

Creating schema
- Decide schema design, with tables such as country, population_metric, and health_metric. Schema name is idb_data, idb.sql contains the DDL
- Time estimate : 2 hrs
- Actual 2 hrs

Extracting from Pandas
- Load CSV files into Pandas dataframe, maybe if we use API use requests to get data to load
- Data Sources: U.S. Census Bureau. (2026). International Database (IDB). Retrieved [5 19, 2026], from [https://www.census.gov/data-tools/demo/idb/#/dashboard?dashboard_page=country&COUNTRY_YR_ANIM=2026]
- We will be extracting the data by downloading the files and placing into our data directory
- Time estimate: 2 hrs
- Actual 3 hrs

Transforming
- Look for columns that need to be transformed, drop nulls, blanks, and clean
- Time estimate : 4 hrs
- Actual : 5 hrs


Load to SQL
- Use pandas function to_sql to load transformed data into SQL, mapped correctly to our DDL, validate in DB editor for records
- Time estimate : 3 hrs
- Actual : 2 hrs

Visualizations
- Use Dash to display visualizations from our data, use appropriate chart types.
- Time estimate 4 hrs

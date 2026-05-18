Hypothesis

Countries that have a higher life expectancy and higher population density tend to have a lower fertility rate than countries that have a lower life expectancy and population density.

Evaluating the dataset
- Extract data from the IDB database zip file, evaluate needed columns and fields such as population density, fertility rate, etc. Look for USA data too?
- Time estimate : 3 hrs

Creating schema
- Decide schema design, with tables such as country, population, fertility,
- Time estimate : 2 hrs

Extracting from Pandas
- Load CSV files into Pandas dataframe, maybe if we use API use requests to get data to load
- Time estimate: 2 hrs

Transforming
- Look for columns that need to be transformed, drop nulls, blanks, and clean
- Time estimate : 4 hrs

Load to SQL
- Use pandas function to_sql to load transformed data into SQL, mapped correctly to our DDL, validate in DB editor for records
- Time estimate : 3 hrs

Visualizations
- Use Dash to display visualizations from our data, use appropriate chart types.
- Time estimate 4 hrs

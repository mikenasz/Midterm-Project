drop schema if exists idb_data cascade;
create schema idb_data;
set search_path to idb_data;

create table country(
	country_id serial PRIMARY KEY,
	country_name varchar(100) NOT NULL
);

CREATE table population_metric(
	metric_pop_id serial PRIMARY KEY,
	total_population bigint NOT NULL,
	year int NOT NULL,
	population_density decimal(10,2) NOT NULL,
	growth_rate decimal(5,2) NOT NULL,
	country_id int NOT NULL,
	FOREIGN key(country_id)
		references country(country_id)
		
);

CREATE TABLE health_metric(
	metric_health_id serial PRIMARY KEY,
	fertility_rate decimal(5,2) NOT NULL,
	life_expectancy decimal(5,2) NOT NULL,
	year int NOT null,
	country_id int NOT NULL,
	FOREIGN key(country_id)
		references country(country_id)
);
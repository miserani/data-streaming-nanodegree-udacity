#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER guest;
	CREATE DATABASE guest;
	CREATE DATABASE cta;
	GRANT ALL PRIVILEGES ON DATABASE cta TO guest;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname cta <<-EOSQL
  ALTER USER guest WITH PASSWORD 'guest';
  ALTER ROLE guest WITH SUPERUSER;
EOSQL

psql -v ON_ERROR_STOP=1 --username guest --dbname cta <<-EOSQL
  CREATE TABLE stations (stop_id INTEGER PRIMARY KEY, direction_id VARCHAR(1) NOT NULL, stop_name VARCHAR(70) NOT NULL, station_name VARCHAR(70) NOT NULL, station_descriptive_name VARCHAR(200) NOT NULL, station_id INTEGER NOT NULL, "order" INTEGER, red BOOLEAN NOT NULL, blue BOOLEAN NOT NULL, green BOOLEAN NOT NULL);
  COPY stations(stop_id, direction_id,stop_name,station_name,station_descriptive_name,station_id,"order",red,blue,green) FROM '/tmp/cta_stations.csv' DELIMITER ',' CSV HEADER;
EOSQL

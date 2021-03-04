-- Name: Steven Fairchild
-- File: wxdata.sql
-- Date: Feb 14, 2021

.echo on
.headers on

DROP TABLE IF EXISTS weather;

CREATE TABLE IF NOT EXISTS weather(
SampleDateTimeStationID TEXT PRIMARY KEY,
TemperatureC NUMERIC NOT NULL,
Pressure NUMERIC NOT NULL,
Humidity NUMERIC NOT NULL,
AirQuality NUMERIC
);
-- User configurable variables
-- Steven Fairchild 20210408
CREATE TABLE IF NOT EXISTS weather.sensors (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    stationid VARCHAR(10),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ambient_temperature DECIMAL(6,3) NOT NULL,
    wind_direction DECIMAL(6,3),
    wind_speed DECIMAL(6,3),
    wind_gust_speed DECIMAL(6,3),
    humidity DECIMAL(6,3) NOT NULL,
    rainfall DECIMAL(6,3),
    air_pressure DECIMAL(6,3) NOT NULL,
    PM35 DECIMAL(6,3),
    PM10 DECIMAL(6,3)
);
CREATE TABLE IF NOT EXISTS weather.packets(
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    packet VARCHAR(100) NOT NULL,
    transmitted BOOL NOT NULL
);
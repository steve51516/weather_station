-- User configurable variables
-- Steven Fairchild 20210408
CREATE TABLE IF NOT EXISTS weather.sensors(
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    stationid VARCHAR(10),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ambient_temperature DECIMAL(6,2) NOT NULL,
    wind_direction DECIMAL(6,2),
    wind_speed DECIMAL(6,2),
    wind_gust_speed DECIMAL(6,2),
    humidity DECIMAL(6,2) NOT NULL,
    rainfall DECIMAL(6,2),
    air_pressure DECIMAL(6,2) NOT NULL,
    PM25 DECIMAL(6,2),
    PM10 DECIMAL(6,2)
);
CREATE TABLE IF NOT EXISTS weather.packets(
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    packet VARCHAR(82) NOT NULL, -- Packets sent should not be longer than 82 characters on this end, without the comment field.
    transmitted BOOL NOT NULL
);
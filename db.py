import mariadb as db
import sys

def create_db():
    db_init = """ CREATE DATABASE IF NOT EXISTS weather;"""
    weather_table_init = """ USE weather;
                CREATE TABLE IF NOT EXISTS sensors (
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
                );"""
    packet_table_init = """ USE weather;
                            CREATE TABLE IF NOT EXISTS packets(
                            ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                            packet VARCHAR(100) NOT NULL,
                            transmitted BOOL NOT NULL
                            );"""

    try:
        conn = db.connect(
            user="wxstation",
            password="password1",
            host="127.0.0.1",
            port=3306
        )
        cur = conn.cursor()
        cur.execute(db_init); conn.commit()
        cur.execute(weather_table_init); conn.commit()
        cur.execute(packet_table_init); conn.commit()
        conn.close()
    except db.Error as e:
        print(f"Error connecting to MariaDB Server: {e}")
        sys.exit(1)

def db_connect():
    try:
        conn = db.connect(
            user="wxstation",
            password="password1",
            host="127.0.0.1",
            port=3306,
            database="weather"
        )
        return conn.cursor()
    except db.Error as e:
        print(f"Error connecting to MariaDB Server: {e}")
        sys.exit(1)

def read_save_sensors(data):
    weather_insert = """INSERT INTO weather(stationid, ambient_temperature, wind_direction, wind_speed, wind_gust_speed, humidity, air_pressure, rainfall, pm25, pm10) 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data_tuple = (data['callsign'], data['temperature'], data['pressure'], data['humidity'], data['pm25'], data['pm10'])
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(weather_insert, data_tuple)
    conn.commit(); conn.close()

def read_save_packet(data):
    packet_insert = """INSERT INTO packets(packet, Sent) 
    VALUES(?, ?);"""
    data_tuple = (data['packet'], data['sent'])
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(packet_insert, data_tuple)
    conn.commit(); conn.close()
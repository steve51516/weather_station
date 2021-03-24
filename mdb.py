import mariadb
import sys

def create_db():
    db_init = """ CREATE DATABASE IF NOT EXISTS weather;"""
    weather_table_init = """ USE weather;
                CREATE TABLE IF NOT EXISTS sensors (
                ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                SampleTimeStamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                StationID VARCHAR(10),
                TemperatureF FLOAT NOT NULL,
                Pressure FLOAT NOT NULL,
                Humidity FLOAT NOT NULL,
                PM25 FLOAT,
                PM10 FLOAT
                );"""
    packet_table_init = """ CREATE TABLE IF NOT EXISTS packets(
                            ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            SampleTimeStamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                            packet VARCHAR(100) NOT NULL,
                            Sent BOOL NOT NULL
                            );"""

    try:
        conn = mariadb.connect(
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
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Server: {e}")
        sys.exit(1)

def db_connect():
    try:
        conn = mariadb.connect(
            user="wxstation",
            password="password1",
            host="127.0.0.1",
            port=3306,
            database="weather"
        )
        return conn.cursor()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Server: {e}")
        sys.exit(1)

def read_save_sensors(data):
    weather_insert = """INSERT INTO weather(StationID, TemperatureF, Pressure, Humidity, pm25, pm10) 
    VALUES(?, ?, ?, ?, ?, ?);"""
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
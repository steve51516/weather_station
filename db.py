import mariadb as db
from time import sleep

def create_db():
    db_init = """ CREATE DATABASE IF NOT EXISTS weather;"""
    weather_table_init = """CREATE TABLE IF NOT EXISTS sensors (
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
    packet_table_init = """CREATE TABLE IF NOT EXISTS packets(
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
            database="weather",
            port=3306
        )
        cur = conn.cursor()
        cur.execute(db_init); conn.commit()
        cur.execute(weather_table_init); conn.commit()
        cur.execute(packet_table_init); conn.commit()
        conn.close()
    except db.Error as e:
        print(f"Error connecting to MariaDB Server: {e}")
        #sys.exit(1)

def db_connect():
    for i in range(1, 4): # Retry 3 times increasing delay by 10 seconds each time
        delay = i * 10
        try:
            conn = db.connect(
                user="wxstation",
                password="P@ssw0rd",
                host="127.0.0.1",
                port=3306,
                database="weather"
            )
            return conn
        except db.Error as e:
            print(f"Error connecting to MariaDB Server: {e}\n\t Retry number {i}\n\t Retrying in {delay} seconds...")
            #sys.exit(1)
            sleep(delay)
            continue

def read_save_sensors(data):
    sensors_insert = """INSERT INTO sensors(stationid, ambient_temperature, wind_direction, wind_speed, wind_gust_speed, humidity, air_pressure, rainfall, pm25, pm10) 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data_tuple = (data['callsign'], data['temperature'], data['wdir'], data['wspeed'], data['wgusts'], data['humidity'], data['pressure'], data['rainfall'], data['pm25'], data['pm10'])
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(sensors_insert, data_tuple)
    conn.commit(); conn.close()

def read_save_packet(data):
    packet_insert = """INSERT INTO packets(packet, transmitted) 
    VALUES(?, ?);"""
    data_tuple = (data['packet'], data['sent'])
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(packet_insert, data_tuple)
    conn.commit(); conn.close()

def format_rain(rain):
    if rain[0] is None:
        return "000"
    else:
        rain1avg = str(round(float(rain[0]), 2))
        return rain1avg.replace('.', '')

def rain_avg(hours): # valid arguements are 00 for since midnight, 1 for past hour, 24 for past 24 hours
    if hours == 00: # Queries average rainfall between now and 00:00 of today
        query = """SELECT AVG(rainfall) FROM sensors where created between CURRENT_DATE() AND NOW();"""
    elif hours == 1 or 24: # Queries average ranfall for the past hour or 24 hours
        query = f"SELECT AVG(rainfall) FROM sensors WHERE created >= now() - INTERVAL {hours} HOUR;"

    conn = db_connect(); cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    return format_rain(row)    
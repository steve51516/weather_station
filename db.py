import sqlite3
from datetime import date, datetime, time
from logger import log

connect_mes = "Successfully Connected to SQLite database wxdata.db"
insert_mes = "Record inserted successfully into"

def make_table():
    try:
        sqliteConnection = sqlite3.connect('wxdata.db')
        cursor = sqliteConnection.cursor()
        log(connect_mes)
        sqlite_insert_query1 = """ CREATE TABLE IF NOT EXISTS weather(
                                    ID INTEGER PRIMARY KEY,
                                    SampleDateTime TEXT NOT NULL,
                                    StationID TEXT,
                                    TemperatureF NUMERIC NOT NULL,
                                    Pressure NUMERIC NOT NULL,
                                    Humidity NUMERIC NOT NULL,
                                    PM25 NUMERIC,
                                    PM10 NUMERIC,
                                    AQI
                                );"""
        sqlite_insert_query2 = """ CREATE TABLE IF NOT EXISTS packets(
                                    ID INTEGER PRIMARY KEY,
                                    SampleDate TEXT NOT NULL,
                                    packet TEXT,
                                    Sent INTEGER
                                );"""
        cursor.execute(sqlite_insert_query1)
        sqliteConnection.commit()
        cursor.execute(sqlite_insert_query2)
        sqliteConnection.commit()
        log(f"Weather table successfully created {cursor.rowcount}", level="debug")                                                                        
    except sqlite3.Error as error:
            log(f"Failed to create weather table: {error}", level="critical")
            print("Failed to create weather table ", error)
    finally:
            if (sqliteConnection):
                sqliteConnection.close()
                log("The SQLite connection is closed", level="debug")


def read_save(data):
  try:
      dt,d = datetime.now(), datetime.date()
      sqliteConnection = sqlite3.connect('wxdata.db')
      cursor = sqliteConnection.cursor()
      log(connect_mes, level="debug")
      weather_insert = """INSERT INTO weather(SampleDateTime, StationID, TemperatureF, Pressure, Humidity, pm25, pm10) 
      VALUES(?, ?, ?, ?, ?, ?, ?);"""
      data_tuple = (dt, data['callsign'], data['temperature'], data['pressure'], data['humidity'], data['pm25'], data['pm10'])
      cursor.execute(weather_insert, data_tuple)
      sqliteConnection.commit()
      log(f"{insert_mes} weather table {cursor.rowcount}", level="debug")
      packet_insert = """INSERT INTO weather(SampleDate, packet, Sent) 
      VALUES(?, ?, ?);"""
      data_tuple = (d, data['packet'], data['sent'])
      cursor.execute(packet_insert, data_tuple)
      sqliteConnection.commit()
      log(f"{insert_mes} packet table {cursor.rowcount}", level="debug")
      cursor.close()
  except sqlite3.Error as error:
          log(f"Failed to insert data into sqlite table: {error}", level="critical")
  finally:
          if (sqliteConnection):
              sqliteConnection.close()
              log("The SQLite connection is closed", level="debug")
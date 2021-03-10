import sqlite3
from datetime import datetime
from logger import log

def make_table():
    try:
        sqliteConnection = sqlite3.connect('wxdata.db')
        cursor = sqliteConnection.cursor()
        log("Successfully Connected to SQLite")
        #sqlite_insert_query = """ DROP TABLE IF EXISTS weather; """
        #cursor.execute(sqlite_insert_query)
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
                                    SampleDateTime TEXT NOT NULL,
                                    packet TEXT
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
      sqliteConnection = sqlite3.connect('wxdata.db')
      cursor = sqliteConnection.cursor()
      log("Successfully Connected to SQLite", level="debug")
      sqlite_insert_query = """INSERT INTO weather(SampleDateTime, StationID, TemperatureF, Pressure, Humidity, pm25, pm10) 
      VALUES(?, ?, ?, ?, ?, ?, ?);"""
      data_tuple = (datetime.now(), data['callsign'], data['temperature'], data['pressure'], data['humidity'], data['pm25'], data['pm10'])
      cursor.execute(sqlite_insert_query, data_tuple)
      sqliteConnection.commit()
      log(f"Record inserted successfully into weather table {cursor.rowcount}", level="debug")
      cursor.close()
  except sqlite3.Error as error:
          log(f"Failed to insert data into sqlite table: {error}", level="critical")
  finally:
          if (sqliteConnection):
              sqliteConnection.close()
              log("The SQLite connection is closed", level="debug")
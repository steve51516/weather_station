from bme280 import *
from datetime import datetime
import sqlite3, time
from sds011 import *
from aprs import send_data

def make_table():
    try:
        sqliteConnection = sqlite3.connect('wxdata.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        #sqlite_insert_query = """ DROP TABLE IF EXISTS weather; """
        #cursor.execute(sqlite_insert_query)
        sqlite_insert_query = """ CREATE TABLE IF NOT EXISTS weather(
                                ID INTEGER PRIMARY KEY,
                                SampleDateTime TEXT NOT NULL,
                                StationID TEXT,
                                TemperatureF NUMERIC NOT NULL,
                                Pressure NUMERIC NOT NULL,
                                Humidity NUMERIC NOT NULL,
                                PM25 NUMERIC,
                                PM10 NUMERIC,
                                AQI
                                ); """
        cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Weather table successfully created ", cursor.rowcount)                                                                        
    except sqlite3.Error as error:
            print("Failed to create weather table ", error)
    finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")


def read_save():
  temperature,pressure,humidity = readBME280All()
  temperatureF = temperature * 1.8 + 32
  pm25, pm10 = read_sds011()
  ztime,StationID = time.strftime('%H%M%S', time.gmtime()),"FW9281"
  try:
      sqliteConnection = sqlite3.connect('wxdata.db')
      cursor = sqliteConnection.cursor()
      print("Successfully Connected to SQLite")
      sqlite_insert_query = """INSERT INTO weather(SampleDateTime, StationID, TemperatureF, Pressure, Humidity, pm25, pm10) 
      VALUES(?, ?, ?, ?, ?, ?, ?);"""
      data_tuple = (ztime, StationID, temperatureF, pressure, humidity, pm25, pm10)
      cursor.execute(sqlite_insert_query, data_tuple)
      sqliteConnection.commit()
      print("Record inserted successfully into weather table ", cursor.rowcount)
      cursor.close()
  except sqlite3.Error as error:
          print("Failed to insert data into sqlite table", error)
  finally:
          if (sqliteConnection):
              sqliteConnection.close()
              print("The SQLite connection is closed")

if __name__=="__main__":
    make_table()
    while True:
        ztime = time.strftime('%H%M%S', time.gmtime())
        temperature,pressure,humidity = readBME280All()
        temperatureF = temperature * 1.8 + 32
        read_save(); packet = send_data(ztime, temperatureF, pressure, humidity)
        print(f"APRS-IS packet: {packet}")
        show_values(temperature, pressure, humidity)
        show_air_values()
        time.sleep(300)
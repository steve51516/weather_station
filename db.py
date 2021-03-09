import sqlite3

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
                                );"""
        cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Weather table successfully created ", cursor.rowcount)                                                                        
    except sqlite3.Error as error:
            print("Failed to create weather table ", error)
    finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")


def read_save(data):
  try:
      sqliteConnection = sqlite3.connect('wxdata.db')
      cursor = sqliteConnection.cursor()
      print("Successfully Connected to SQLite")
      sqlite_insert_query = """INSERT INTO weather(SampleDateTime, StationID, TemperatureF, Pressure, Humidity, pm25, pm10) 
      VALUES(?, ?, ?, ?, ?, ?, ?);"""
      data_tuple = (data['now'], data['call'], data['temperature'], data['pressure'], data['humidity'], data['pm25'], data['pm10'])
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
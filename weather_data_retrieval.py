import requests
import pandas as pd
import sqlite3
from datetime import datetime

database_name = 'weather_database.db'

def database_connection(database_name: str) -> sqlite3.Connection:
    ''' This function connects to an existing SQLite database, if the database does not exist,
        it implicitly creates a new one.

        Args:
        database_name (str): It represents the database name

        Return:
        Object (sqlite3.Connection): returns a connection object
    '''
    if not isinstance(database_name, str):
        raise TypeError(f'The database name (e.g., {database_name}) should be of type string')

    try:
        connection = sqlite3.connect(database_name, timeout=10)
        return connection
    except sqlite3.OperationalError as op_error:
        raise sqlite3.OperationalError(f'Operational error occured: {op_error}')
    except sqlite3.DatabaseError as db_error:
        raise sqlite3.DatabaseError(f'Database error occured: {db_error}')
    except sqlite3.Error as erroe:
        raise sqlite3.Error(f'An error happened while connection to the database: {error}')
    except Exception as e:
        raise Exception(f'An unexpected error occured: {e}')
    
def save_to_database(data: pd.DataFrame, database_connection: sqlite3.Connection)->None:
    ''' This function saves json-based weather data into the database

        Args:
            data (): It represents the data to be saved in the database
            database_connection (sqlite3.Connection): It represents the database connection object

        Return:
            None
    '''
    if not isinstance(database_connection, sqlite3.Connection):
        raise TypeError(f'The database connection (e.g., {database_connection}) should be a connection object type')

    cursor = database_connection.cursor()

    timestamp = datetime.now()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Weather (
            Timestamp TEXT,
            Country TEXT,
            City TEXT,
            Temperature REAL,
            Humidity INTEGER,
            Low_Temperature REAL,
            High_Temperature REAL,
            Weather_Category TEXT,
            Wind_Speed REAL
        )
        """)

    # Insert each row of parsed_data into the database
    for _, row in data.iterrows():
        cursor.execute("""
        INSERT INTO Weather (Timestamp, Country, City, Temperature, Humidity, Low_Temperature, High_Temperature, Weather_Category, Wind_Speed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp,
              row['Country'],
              row['City'],
              row['Temperature'],
              row['Humidity'],
              row['Low Temperature'],
              row['High Temperature'],
              row['Weather Category'],
              row['Wind Speed']))

    database_connection.commit()
    
    res = cursor.execute('SELECT * FROM Weather')
    rows = res.fetchall()
    for row in rows:
        print(row)
        
    cursor.close()

def fetch_weather_data(city: str,
                       country=None,
                       state=None,
                       units=None):
    ''' This function fetches weather data

        Args:
            city (str): the city you want to get the weather at
            country (str): it represents two letter abbreviations, by default US
            state (str): the state of the city, only two letter abbreviations
            units (str): it nay one of {metric, imperial, standard}, bu defauly metric

        Return:
            The function returns json-based weather data or None
    '''
    if not city:
        raise ValueError(f'The city parameter (e.g., {city}) is required')
    
    if not country:
        country = 'US'
    
    if not units:
        units = "metric"
    
    if units not in {"metric", "imperial", "standard"}:
        raise ValueError(f"The units paramter (e.g., {units}) must be one of: 'metric', 'imperial', or 'standard'")
    
    if not all(isinstance(param, str) for param in (city, country, state, units)):
        raise TypeError(f"The provided parameters (city, country, state, units) (e.g., {city, country, state, units}) should be of type string")
    
    api_url = "https://weather.talkpython.fm/api/weather"
    params = {
        "city": city,
        "country": country,
        "state": state,
        "units": units,
    }

    try:
        response = requests.get(api_url, params=params, headers=None)
        print(f'The url is {response.url}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the given URL: {e}")
        return None
    
def parse_json(data: dict)-> pd.DataFrame:
    ''' This function parses the json-formatted data

        Args:
            data (dict): It represents weather raw data

        Return:
            parsed_data(pd.DataFrame): It represents the data to be saved in the database
    '''
    country = data['location']['country']
    city = data['location']['city']
    temp = data['forecast']['temp']
    humidity = data['forecast']['humidity']
    low_temp = data['forecast']['low']
    high_temp = data['forecast']['high']
    weather_category = data['weather']['category']
    wind_speed = data['wind']['speed']

    # Create a dictionary for the DataFrame
    weather_dict = {
        "Country": [country],
        "City": [city],
        "Temperature": [temp],
        "Humidity": [humidity],
        "Low Temperature": [low_temp],
        "High Temperature": [high_temp],
        "Weather Category": [weather_category],
        "Wind Speed": [wind_speed],
    }

    dataframe = pd.DataFrame(weather_dict)
    return dataframe


#weather_data = fetch_weather_data(city='portland', state='OR',units='imperial')
#parsed_weather_data_df = parse_json(weather_data)
#print(parsed_weather_data_df)
#database_connection = database_connection(database_name)
#save_to_database(parsed_weather_data_df,database_connection)
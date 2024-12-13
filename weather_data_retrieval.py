import requests
import pandas as pd

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

weather_data = fetch_weather_data(city='portland', state='OR',units='imperial')
print(weather_data)
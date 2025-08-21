"""
module1.py

A simple module to read and display weather data from a CSV file.

Functions:
    load_weather_data(file_path: str): Loads CSV weather data
"""

import pandas as pd

def load_weather_data(file_path: str) -> pd.DataFrame:
    """
    Loads weather data from a CSV file and print first 5 rows.

    Parameters:
    file_path (str): The path to the CSV file containing weather data.

    Returns:
    pd.DataFrame: A Pandas DataFrame containing the weather data.
    """
    df = pd.read_csv(data_path)
    print(df.head())
    return df


if __name__ == "__main__":
    data_path = 'data/Weather Test Data.csv'
    load_weather_data(data_path)
 
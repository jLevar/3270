"""
weather_hero.py

A simple module to read and display weather data from a CSV file.

Functions:
    load_weather_data(file_path: str): Loads CSV weather data
    describe_weather_data(df: pd.DataFrame): Prints summary statistics of the weather data
"""

import os
import pandas as pd

def load_weather_data(file_path: str) -> pd.DataFrame:
    """
    Loads weather data from a CSV file and print first 5 rows.

    Parameters:
    file_path (str): The path to the CSV file containing weather data.

    Returns:
    df (pd.DataFrame): A Pandas DataFrame containing the weather data.
    """
    df = pd.read_csv(file_path)
    print(df.head())
    return df

def describe_weather_data(df: pd.DataFrame) -> None:
    """
    Prints summary statistics of the weather data.

    Parameters:
    df (pd.DataFrame): The DataFrame containing weather data.

    Returns:
    numerical_stats (pd.DataFrame): The summary statistics for numerical columns.
    categorical_stats (pd.DataFrame): The summary statistics for categorical columns.
    """
    numerical_columns = df.select_dtypes(include=['number']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    numerical_stats = pd.DataFrame({
                'mean': df[numerical_columns].mean(), 
                'median': df[numerical_columns].median(), 
                'mode': df[numerical_columns].mode().iloc[0],
                'range': df[numerical_columns].max() - df[numerical_columns].min()
            })
    categorical_stats = df[categorical_columns].describe()
    print(numerical_stats, "\n--------------------\n")
    print(categorical_stats)
    return numerical_stats, categorical_stats
    

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # AI Written
    data_path = os.path.join(base_dir, 'data', 'Weather Test Data.csv') # AI Written
    data = load_weather_data(data_path)
    describe_weather_data(data)
 
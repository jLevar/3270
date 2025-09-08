"""
weather_hero.py

A simple module to read and display weather data from a CSV file.

Functions:
    load_weather_data(file_path: str): Loads CSV weather data
    describe_weather_data(df: pd.DataFrame): Prints summary statistics of the weather data
"""

import os
import pandas as pd

class WeatherLoader:
    """
    Loads weather data from a CSV file into Pandas DataFrame.
    """
    def __init__(self, default_path: str):
        self.default_path = default_path

    def load_weather_data(self, file_path) -> pd.DataFrame:
        """
        Loads weather data from a CSV file into Pandas DataFrame.

        Parameters:
        file_path (str): The path to the CSV file containing weather data.

        Returns:
        df (pd.DataFrame): A Pandas DataFrame containing the weather data.
        """
        file_path = file_path or self.default_path
        df = pd.read_csv(file_path)
        self.df = df
        return df
    
class WeatherAnalyzer:
    """
    Analyzes weather data from a Pandas DataFrame
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate_summary_statistics(self) -> dict:
        """
        Generates and returns summary statistics of the weather data.

        Returns:
        summary_statistics (dict): A dictionary containing summary statistics for numerical and categorical columns.
        """
        df = self.df
        numerical_columns = df.select_dtypes(include=['number']).columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        numerical_stats = pd.DataFrame({
                    'mean': df[numerical_columns].mean(), 
                    'median': df[numerical_columns].median(), 
                    'mode': df[numerical_columns].mode().iloc[0],
                    'range': df[numerical_columns].max() - df[numerical_columns].min()
                })
        categorical_stats = df[categorical_columns].describe()
        summary_statistics = {"numerical": numerical_stats, "categorical": categorical_stats}
        return summary_statistics
    
class WeatherSaver:
    def __init__(self, output_file: str):
        self.output_file = output_file

    def save_summary(self, summary_statistics: pd.DataFrame) -> None:
        """
        Saves the summary statistics to a CSV file.

        Parameters:
        summary_statistics (pd.DataFrame): The summary statistics to save.
        """
        with open(self.output_file, 'w') as f:
            f.write("Numerical Summary Statistics\n")
            summary_statistics["numerical"].to_csv(f)
            f.write("\nCategorical Summary Statistics\n")
            summary_statistics["categorical"].to_csv(f)
            print(f"Weather summary saved to {self.output_file}")
        

class WeatherHero:
    def __init__(self, data_filepath: str, output_file: str):
        self.data_loader = WeatherLoader(data_filepath)
        self.data_storage = WeatherSaver(output_file)
        self.data_analyzer = None 

    def process_weather_data(self) -> None:
        """
        Loads, analyzes, and saves weather data summary statistics.
        """
        df = self.data_loader.load_weather_data(self.data_loader.default_path)
        self.data_analyzer = WeatherAnalyzer(df)
        summary_statistics = self.data_analyzer.generate_summary_statistics()
        self.data_storage.save_summary(summary_statistics)
        

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # AI Written
    data_path = os.path.join(base_dir, 'data', 'Weather Test Data.csv') # AI Written
    output_path = os.path.join(base_dir, 'data', 'Weather Summary.csv')
    weather_hero = WeatherHero(data_path, output_path)
    weather_hero.process_weather_data()
    
    
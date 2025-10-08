"""
weather_hero.py

A simple module to load and analyze weather data from a CSV file.

Classes:
WeatherLoader - Loads weather data from a CSV file into a Pandas DataFrame.
WeatherAnalyzer - Analyzes weather data from a Pandas DataFrame
WeatherSaver - Saves weather analysis data to CSV
WeatherHero - Loads and analyzes weather data and saves summary statistics 
"""

import os
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s",
    filename="logs/weather_hero.log"
)

class WeatherLoader:
    """
    Loads weather data from a CSV file into a Pandas DataFrame.
    """
    def __init__(self, default_path: str):
        self.default_path = default_path

    def load_weather_data(self, file_path: str = None) -> pd.DataFrame:
        """
        Loads weather data from a CSV file into Pandas DataFrame.

        Parameters:
        file_path (str): The path to the CSV file containing weather data.

        Returns:
        df (pd.DataFrame): A Pandas DataFrame containing the weather data.

        >>> wl = WeatherLoader("data/basic-data.csv")
        >>> wl.load_weather_data().shape
        (100, 4)
        """
        file_path = file_path or self.default_path
        if not file_path.endswith(".csv"):
            raise ValueError(f"Unsupported file type: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            if len(df.axes[1]) == 1:
                raise pd.errors.ParserError
        except FileNotFoundError as e:
            logging.error(f"File Error: {e}")
            raise 
        except pd.errors.ParserError as e:
            logging.error(f"CSV Parsing Error: {e}")
            raise
        
        logging.info(f"Successfully read file from {file_path}")
        return df
    
    def iter_rows(self, file_path: str = None, chunk_size = 500):
        """
        Generator that yields chunks of a CSV file into Pandas DataFrame.

        Parameters:
        file_path (str): The path to the CSV file containing weather data.

        Yields:
        df (pd.DataFrame): A Pandas DataFrame containing a chunk of the weather data.

        >>> wl = WeatherLoader("data/basic-data.csv")
        >>> wl.iter_rows(chunk_size=22).__next__().shape
        (22, 4)
        """
        file_path = file_path or self.default_path
        if not file_path.endswith(".csv"):
            raise ValueError(f"Unsupported file type: {file_path}")

        try:
            with pd.read_csv(file_path, chunksize=chunk_size) as file:
                for chunk in file:
                    logging.info(f"Yielding {len(chunk)} rows from {file_path}")
                    if len(chunk.axes[1]) == 1:
                        raise pd.errors.ParserError
                    yield chunk
        except FileNotFoundError as e:
            logging.error(f"File Error: {e}")
            raise 
        except pd.errors.ParserError as e:
            logging.error(f"CSV Parsing Error: {e}")
            raise

    
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

        >>> wl = WeatherLoader("data/basic-data.csv")
        >>> wa = WeatherAnalyzer(wl.load_weather_data())
        >>> wa.generate_summary_statistics()["numerical"].values.tolist()
        [[44.53, 43.5, 32.0, 51.0]]
        """
        try:
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
            logging.info(f"Successfully generated summary statistics on numerical columns {numerical_columns} and " 
                        f"categorical columns {categorical_columns}")
            return summary_statistics
        except Exception as e:
            logging.error(f"Failed to generate summary statistics. Terminating program due to error {e}")
            raise
        
    
class WeatherSaver:
    """
    Saves weather analysis data to CSV
    """
    def __init__(self, output_file: str):
        self.output_file = output_file

    def save_summary(self, summary_statistics: pd.DataFrame) -> None:
        """
        Saves the summary statistics to a CSV file.

        Parameters:
        summary_statistics (pd.DataFrame): The summary statistics to save.
        """
        try:
            with open(self.output_file, 'w') as f:
                f.write("Numerical Summary Statistics\n")
                summary_statistics["numerical"].to_csv(f)
                f.write("\nCategorical Summary Statistics\n")
                summary_statistics["categorical"].to_csv(f)
                logging.info(f"Weather summary saved to {self.output_file}")
        except Exception as e:
            logging.error(f"Failed to save weather summary - Error {e}")
        

class WeatherHero:
    """
    Loads and analyzes weather data and saves summary statistics 
    """
    def __init__(self, data_filepath: str, output_file: str):
        self.data_loader = WeatherLoader(data_filepath)
        self.data_storage = WeatherSaver(output_file)
        self.data_analyzer = None 

    def process_weather_data(self) -> None:
        """
        Loads and analyzes weather data and saves summary statistics
        """
        try:
            df = pd.concat([chunk for chunk in self.data_loader.iter_rows(self.data_loader.default_path, chunk_size=2000)])
            self.data_analyzer = WeatherAnalyzer(df)
            summary_statistics = self.data_analyzer.generate_summary_statistics()
            self.data_storage.save_summary(summary_statistics)
        except Exception as e:
            logging.error(f"process_weather_data was terminated by the following error - {e}")    

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # AI Written
    data_path = os.path.join(base_dir, 'data', 'test.csv') # AI Written
    output_path = os.path.join(base_dir, 'data', 'summary.csv')
    weather_hero = WeatherHero(data_path, output_path)
    weather_hero.process_weather_data()
    
    
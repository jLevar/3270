"""
weather_hero.py

A simple module to load and analyze weather data from a CSV file.

Classes:
WeatherLoader - Loads weather data from a CSV file into a Pandas DataFrame.
WeatherAnalyzer - Analyzes weather data from a Pandas DataFrame
WeatherSaver - Saves weather analysis data to CSV
WeatherHero - Loads and analyzes weather data and saves summary statistics 
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import reduce
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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

    async def load_weather_data(self, file_path: str = None) -> pd.DataFrame:
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
            df = await asyncio.to_thread(pd.read_csv, file_path)
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

    def average_wind_speed_per_direction(self, output_path="static/plots/avg_windspeed.jpg"):
        records = self.df.to_dict('records')    
   
        wind_mapping = pd.DataFrame(list(map(lambda x: (x['WindGustDir'], x['WindGustSpeed']), records)),
                                    columns=['WindGustDir', 'WindGustSpeed'])
        
        wind_avg = wind_mapping.groupby('WindGustDir')['WindGustSpeed'].mean()

        plt.bar(wind_avg.index, wind_avg.values)
        plt.title('Average Wind Gust Speed by Direction')
        plt.xlabel('Direction')
        plt.ylabel('Speed (km/hr)')

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        return output_path
        
    def average_rainfall_hot_vs_cold(self, output_path="static/plots/avg_rainfall.jpg") -> None:
        records = self.df.to_dict('records')
 
        hot_days = pd.DataFrame(list(filter(lambda x: x['MaxTemp'] > 30, records)))
        cold_days = pd.DataFrame(list(filter(lambda x: x['MinTemp'] < 10, records)))

        avg_df = pd.concat([
            pd.Series({"type": "Hot Days", 'avg_rainfall': hot_days["Rainfall"].mean()}),
            pd.Series({"type": "Cold Days", 'avg_rainfall': cold_days["Rainfall"].mean()})            
        ])

        plt.bar(avg_df['type'], avg_df['avg_rainfall'])
        plt.title('Average Rainfall: Hot vs Cold Days')
        plt.xlabel('Type')
        plt.ylabel('Rainfall (mm)')

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        return output_path

    def total_rainfall(self) -> pd.Series:
        """
        Parallelizes total rainfall computation across stations.
        """
        def compute_location_totals(df_chunk: pd.DataFrame) -> pd.Series:
            """Compute rainfall totals for a subset of stations."""
            totals = df_chunk.groupby("Location")["rainfall"].sum()
            print(f"Processed {len(df_chunk)} rows")
            return totals
        
        # Split dataframe by station (one chunk per station)
        locations = [group for _, group in self.df.groupby("Location")]

        results = []
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(compute_location_totals, group) for group in locations]

            for future in as_completed(futures):
                result = future.result()
                results.append(result)

        # Combine the results into a single Series
        total_rainfall = pd.concat(results).groupby("Location").sum()

        print("\nFinal total rainfall by Location:")
        print(total_rainfall)
        return total_rainfall

    def total_rainfall(self, output_path="static/plots/total_rainfall.jpg") -> None:
        records = self.df.to_dict('records')  

        total_rainfall = reduce(lambda acc, x: acc + x['Rainfall'], records, 0)
        plt.bar([0], [total_rainfall])  # x-position and height
        plt.xticks([0], ["Rainfall"])  # optional label
        plt.ylabel("mm")
        plt.title("Total Rainfall on Record")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        return output_path


    
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
    

    async def start(self):
        await self._load_weather_data()
        self.data_analyzer = WeatherAnalyzer(self.df)


    async def _load_weather_data(self, mode:str = "full") -> None:
        if mode == "full":
            self.df = await self.data_loader.load_weather_data()
        elif mode == "batch":
            self.df = pd.concat([chunk for chunk in self.data_loader.iter_rows(self.data_loader.default_path, chunk_size=2000)])
        else:
            raise NotImplementedError(f"Mode {mode} not valid for WeatherHero _load_weather_data")

    def _clean_data(self) -> None:
        self.df['Rainfall'] = pd.to_numeric(self.df['Rainfall'], errors='coerce').fillna(0)

    def print_head(self) -> None:
        print(self.df.head())

    def process_weather_data(self) -> None:
        """
        Loads and analyzes weather data and saves summary statistics
        """
        try:
            self._clean_data()
            summary_statistics = self.data_analyzer.generate_summary_statistics()
            self.data_storage.save_summary(summary_statistics)
            
            figure_paths = [] 
            figure_paths.append(self.data_analyzer.average_wind_speed_per_direction())
            figure_paths.append(self.data_analyzer.total_rainfall())
            figure_paths.append(self.data_analyzer.average_rainfall_hot_vs_cold())

            return figure_paths

        except Exception as e:
            logging.error(f"process_weather_data was terminated by the following error - {e}")  
            return 0, 0  

async def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # AI Written
    data_path = os.path.join(base_dir, 'data', 'test.csv') # AI Written
    output_path = os.path.join(base_dir, 'data', 'summary.csv')
    weather_hero = WeatherHero(data_path, output_path)
    await weather_hero.start()
    weather_hero.process_weather_data()


if __name__ == "__main__":
    asyncio.run(main())
    
    
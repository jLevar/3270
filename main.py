from weather_hero import load_weather_data, describe_weather_data
import os

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "Weather Test Data.csv")

    df = load_weather_data(data_path)
    describe_weather_data(df)

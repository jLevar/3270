import asyncio
import os
import tempfile
import unittest
from weather_hero import WeatherLoader, WeatherSaver, WeatherAnalyzer, WeatherHero
import pandas as pd

class TestWeatherHero(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.test_file = os.path.join(base_dir, "data", "test.csv")
        self.loader = WeatherLoader(self.test_file)
    
    async def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            wl = WeatherLoader("data/fake.csv")
            await wl.load_weather_data()

    async def test_non_csv_file(self):
        with self.assertRaises(ValueError):
            wl = WeatherLoader("data/words.txt")
            await wl.load_weather_data()

    async def test_bad_csv_file(self):    
        with self.assertRaises(pd.errors.ParserError):
            wl = WeatherLoader("data/corrupt.csv")
            await wl.load_weather_data()

        with self.assertRaises(pd.errors.ParserError):
            wl = WeatherLoader("data/corrupt.csv")
            [row for row in wl.iter_rows()]

    def test_accurate_summary(self):
        df = pd.DataFrame({
            "temp": [10, 20, 30],        
            "humidity": [50, 50, 70],     
            "condition": ["sunny", "rainy", "sunny"],  
            "city": ["A", "B", "C"]       
        })
        wa = WeatherAnalyzer(df)
        summary_df = wa.generate_summary_statistics()

        self.assertEqual(summary_df["numerical"].loc["temp"]["mean"], 20)
        self.assertEqual(summary_df["numerical"].loc["humidity"]["median"], 50)
        self.assertEqual(summary_df["categorical"].loc["top"]["condition"], "sunny")
        self.assertEqual(summary_df["categorical"].loc["count"]["city"], 3)


    async def test_save(self):
        wl = WeatherLoader("data/test.csv")
        wa = WeatherAnalyzer(await wl.load_weather_data())
        summary_df = wa.generate_summary_statistics()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "summary.csv")
            ws = WeatherSaver(file_path)
            ws.save_summary(summary_df)
            assert os.path.exists(file_path)

    def test_total_rainfall(self):
        df = pd.DataFrame([
            {"MaxTemp": 35, "MinTemp": 15, "Rainfall": 5,  "WindGustDir": "N", "WindGustSpeed": 40},
            {"MaxTemp": 28, "MinTemp": 8,  "Rainfall": 10, "WindGustDir": "E", "WindGustSpeed": 30},
            {"MaxTemp": 33, "MinTemp": 20, "Rainfall": 0,  "WindGustDir": "N", "WindGustSpeed": 50},
            {"MaxTemp": 18, "MinTemp": 5,  "Rainfall": 20, "WindGustDir": "E", "WindGustSpeed": 40},
        ])
        wa = WeatherAnalyzer(df)
        records = wa.df.to_dict('records')
        
        from functools import reduce
        total = reduce(lambda acc, x: acc + x['Rainfall'], records, 0)
        self.assertEqual(total, 35)


    def test_average_rainfall_hot_vs_cold(self):
        df = pd.DataFrame([
            {"MaxTemp": 35, "MinTemp": 15, "Rainfall": 5},
            {"MaxTemp": 28, "MinTemp": 8,  "Rainfall": 10},
            {"MaxTemp": 33, "MinTemp": 20, "Rainfall": 0},
            {"MaxTemp": 18, "MinTemp": 5,  "Rainfall": 20},
        ])
        wa = WeatherAnalyzer(df)
        records = wa.df.to_dict('records')

        hot_days = list(filter(lambda x: x['MaxTemp'] > 30, records))
        cold_days = list(filter(lambda x: x['MinTemp'] < 10, records))

        hot_avg = pd.DataFrame(hot_days)["Rainfall"].mean()
        cold_avg = pd.DataFrame(cold_days)["Rainfall"].mean()

        self.assertEqual(hot_avg, 2.5)  # (5 + 0)/2
        self.assertEqual(cold_avg, 15)  # (10 + 20)/2


    def test_average_wind_speed_per_direction(self):
        df = pd.DataFrame([
            {"WindGustDir": "N", "WindGustSpeed": 40},
            {"WindGustDir": "E", "WindGustSpeed": 30},
            {"WindGustDir": "N", "WindGustSpeed": 50},
            {"WindGustDir": "E", "WindGustSpeed": 40},
        ])
        wa = WeatherAnalyzer(df)
        records = wa.df.to_dict('records')

        wind_mapping = pd.DataFrame(
            list(map(lambda x: (x['WindGustDir'], x['WindGustSpeed']), records)),
            columns=['WindGustDir', 'WindGustSpeed']
        )

        wind_avg = wind_mapping.groupby('WindGustDir')['WindGustSpeed'].mean().to_dict()
        self.assertEqual(wind_avg['N'], 45)
        self.assertEqual(wind_avg['E'], 35)


if __name__ == '__main__':
    print("Starting tests")
    asyncio.run(unittest.main())
# Weather Hero

## Description
Weather Hero is a python package that displays summary statistics derived from the Australian Weather Database.

## Usage


## Setup

### Module 1
This project has been setup with systems designed for a scalable and clean codebase.

Version Control - GitHub Repo
- Repository to save versions and share code across devices
- .gitignore: Insures that the data, venv, and other files are not put in the repo

Virtual Environment - venv
- Created a virtual environment that holds all necessary packages
- requirements.txt allows anyone to replicate my venv
  - pip install -r requirements.txt 
 
### Module 2
Added: describe_weather_data()
Put .py file into ./weather_hero/ subdirectory and added __init__.py file
 
### Module 3
Added WeatherLoader, WeatherAnalyzer, WeatherSaver, and WeatherHero classes to weather_hero.py 

- WeatherLoader
  - Loads weather data from a CSV file into Pandas DataFrame
- WeatherAnalyzer
  - Analyzes weather data from a Pandas DataFrame
- WeatherSaver
  - Saves the summary statistics to a CSV file.
- WeatherHero 
  - Loads, analyzes, and saves weather data summary statistics. (Using the above classes)
        
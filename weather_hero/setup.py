from setuptools import setup, find_packages

setup(
    name="weather-hero",                     
    version="0.1.0",                         
    author="Joshua LeVar",
    author_email="11073615@uvu.edu",
    description="A simple module to read and summarize weather data.",
    url="https://github.com/jLevar/3270",
    packages=find_packages(),                
    install_requires=[
        "pandas>=1.0.0",                     
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.10.12", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)

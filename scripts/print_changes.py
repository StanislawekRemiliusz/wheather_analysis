from pathlib import Path
import pandas as pd

df = pd.read_csv("output/weather_clean.csv", low_memory=False)

print(df.head())
print(df.info())
print(df.isna().sum())
print("duplikaty:", df.duplicated().sum())
print(df["data"].head())
print(df["O3"].describe())
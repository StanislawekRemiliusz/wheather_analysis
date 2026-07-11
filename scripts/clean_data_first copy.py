from pathlib import Path
import pandas as pd

#load file
project_folder = Path(__file__).resolve().parent.parent

input_file = project_folder/"output"/"weather_merged.csv"
output_file = project_folder/"output"/"weather_clean.csv"
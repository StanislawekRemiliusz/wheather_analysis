from pathlib import Path
import pandas as pd

#file with excel
data_folder = Path("data")

#list of files .xlsx
excel_files = data_folder.glob("*.xlsx")

#load to dataFrame
dataframes = [pd.read_excel(file) for file in excel_files]

#merge all data
merged_df = pd.concat(dataframes,ignore_index=True)

#save in output
output_folder = Path("output")
output_folder.mkdir(exist_ok=True)

merged_df.to_csv(output_folder/"weather_merged.csv",index=False)

print(f"merged {len(dataframes)} pliki.")
print(f"number of record: {len(merged_df)}")

print(merged_df.head())
print(merged_df.info())
print(merged_df.isna().sum())
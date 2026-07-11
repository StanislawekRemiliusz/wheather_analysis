from pathlib import Path
import pandas as pd


def clean_weather_data():
    project_folder = Path(__file__).resolve().parent.parent
    input_file = project_folder / "output" / "weather_merged.csv"
    output_file = project_folder / "output" / "weather_clean.csv"

    if not input_file.exists():
        raise FileNotFoundError(f"Brak pliku wejściowego: {input_file}")

    df = pd.read_csv(input_file, low_memory=False)
    df = df.copy()

    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    for col in ["miasto", "ulica", "kod", "dzielnica", "dostawca"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": pd.NA, "None": pd.NA})
            df[col] = df[col].replace(r"^\s*$", pd.NA, regex=True)

    if "O3" in df.columns:
        df["O3"] = (
            df["O3"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace(" ", "", regex=False)
            .str.replace("nan", "", regex=False)
        )
        df["O3"] = pd.to_numeric(df["O3"], errors="coerce")

    output_file.parent.mkdir(exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"Wczytano {len(df)} rekordów")
    print(f"Zapisano do: {output_file}")
    print("\nBrakujące wartości:")
    print(df.isna().sum())
    print(f"\nNieprawidłowe daty: {df['data'].isna().sum()}")
    print(f"Puste wartości O3 po czyszczeniu: {df['O3'].isna().sum()}")
    print(f"Duplikaty wierszy: {df.duplicated().sum()}")
    print("\nPrzykład po czyszczeniu:")
    print(df.head(3).to_string())


if __name__ == "__main__":
    clean_weather_data()


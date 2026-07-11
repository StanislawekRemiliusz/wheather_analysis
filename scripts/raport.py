from pathlib import Path
import pandas as pd


def generate_report():
    project_folder = Path(__file__).resolve().parent.parent
    input_file = project_folder / "output" / "weather_clean.csv"
    report_file = project_folder / "output" / "data_quality_report.txt"

    if not input_file.exists():
        input_file = project_folder / "output" / "weather_merged.csv"

    if not input_file.exists():
        raise FileNotFoundError(f"Brak pliku danych: {input_file}")

    df = pd.read_csv(input_file, low_memory=False)

    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    report_lines = []
    report_lines.append("Raport jakości danych")
    report_lines.append("=" * 40)
    report_lines.append(f"Źródło pliku: {input_file}")
    report_lines.append(f"Liczba wierszy: {len(df)}")
    report_lines.append(f"Liczba kolumn: {len(df.columns)}")
    report_lines.append("")
    report_lines.append("Typy kolumn:")
    for column, dtype in df.dtypes.items():
        report_lines.append(f"- {column}: {dtype}")
    report_lines.append("")
    report_lines.append("Braki danych:")
    missing = df.isna().sum()
    for column, count in missing.items():
        if count > 0:
            report_lines.append(f"- {column}: {count}")
    report_lines.append("")
    report_lines.append(f"Nieprawidłowe daty: {df['data'].isna().sum() if 'data' in df.columns else 'brak kolumny'}")
    report_lines.append(f"Puste wartości O3: {df['O3'].isna().sum() if 'O3' in df.columns else 'brak kolumny'}")
    report_lines.append(f"Duplikaty wierszy: {df.duplicated().sum()}")
    report_lines.append("")
    report_lines.append("Przykładowe rekordy:")
    report_lines.append(df.head(3).to_string(index=False))

    report_file.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Raport zapisano do: {report_file}")
    print("Raport gotowy.")


if __name__ == "__main__":
    generate_report()

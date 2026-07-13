from pathlib import Path
import csv

base_dir = Path(__file__).resolve().parents[1]
source_file = base_dir / "data" / "stationdata" / "s_d_375_2025.csv"
header_file = base_dir / "data" / "stationdata" / "s_d_t_nagłówek.csv"
output_file = base_dir / "output" / "s_d_375_2025_with_header.csv"

with header_file.open(newline="", encoding="utf-8-sig") as f:
    header = next(csv.reader(f))

with source_file.open(newline="", encoding="utf-8-sig") as f:
    rows = list(csv.reader(f))

if rows and rows[0] == header:
    print("Nagłówki są już obecne w pliku źródłowym. Nie tworzę nowego pliku.")
else:
    output_file.parent.mkdir(exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Zapisano plik z nagłówkami do: {output_file}")

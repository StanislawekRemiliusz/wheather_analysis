import argparse
import csv
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "output" / "weather_merged.csv"
OUTPUT_DIR = ROOT / "output2"
DEFAULT_PARTS = 3


def split_csv_into_parts(input_path: Path, output_dir: Path, parts: int = 3) -> list[Path]:
    output_dir.mkdir(exist_ok=True)

    for existing_file in output_dir.glob("weather_merged_part_*.csv"):
        existing_file.unlink()

    with input_path.open("r", encoding="utf-8-sig", newline="") as source_file:
        reader = csv.reader(source_file)
        header = next(reader, None)
        if header is None:
            raise ValueError("Plik wejściowy jest pusty.")

        rows = list(reader)

    output_paths: list[Path] = []

    if len(rows) == 0:
        for index in range(1, parts + 1):
            output_path = output_dir / f"weather_merged_part_{index}.csv"
            with output_path.open("w", encoding="utf-8", newline="") as out_file:
                writer = csv.writer(out_file)
                writer.writerow(header)
            output_paths.append(output_path)
        return output_paths

    chunk_size = (len(rows) + parts - 1) // parts

    for index in range(parts):
        start = index * chunk_size
        end = start + chunk_size
        part_rows = rows[start:end]
        output_path = output_dir / f"weather_merged_part_{index + 1}.csv"

        with output_path.open("w", encoding="utf-8", newline="") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(header)
            writer.writerows(part_rows)
        output_paths.append(output_path)

    return output_paths


def ask_for_parts(default: int = DEFAULT_PARTS) -> int:
    if not sys.stdin.isatty():
        return default

    while True:
        user_input = input(f"Ile części chcesz utworzyć? [{default}]: ").strip()
        if not user_input:
            return default

        try:
            parts = int(user_input)
        except ValueError:
            print("Wpisz liczbę całkowitą.")
            continue

        if parts > 0:
            return parts

        print("Liczba części musi być większa od zera.")


def calculate_parts_from_target_size(input_path: Path, target_size_mb: float) -> int:
    if target_size_mb <= 0:
        raise ValueError("Rozmiar pliku musi być większy od zera.")

    input_size_bytes = input_path.stat().st_size
    target_size_bytes = target_size_mb * 1024 * 1024
    return max(1, math.ceil(input_size_bytes / target_size_bytes))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Podziel plik weather_merged.csv na części.")
    parser.add_argument("parts", nargs="?", type=int, help="Liczba części do utworzenia")
    parser.add_argument(
        "--target-size-mb",
        type=float,
        help="Maksymalny rozmiar jednego pliku wyjściowego w MB",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.parts is not None and args.target_size_mb is not None:
        raise SystemExit("Podaj albo liczbę części, albo --target-size-mb, nie oba naraz.")

    if args.target_size_mb is not None:
        parts = calculate_parts_from_target_size(INPUT_FILE, args.target_size_mb)
        print(f"Ustawiono {parts} części dla rozmiaru ok. {args.target_size_mb:.2f} MB.")
    else:
        parts = args.parts if args.parts is not None else ask_for_parts()

    if parts is not None and parts <= 0:
        raise SystemExit("Liczba części musi być większa od zera.")

    output_paths = split_csv_into_parts(INPUT_FILE, OUTPUT_DIR, parts or DEFAULT_PARTS)

    for output_path in output_paths:
        size_bytes = output_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        print(f"{output_path.name}: {size_mb:.2f} MB")

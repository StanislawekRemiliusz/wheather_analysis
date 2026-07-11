from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


project_folder = Path(__file__).resolve().parent.parent
input_file = project_folder / "output" / "weather_clean.csv"
output_dir = project_folder / "output" / "report"
output_dir.mkdir(exist_ok=True)


def load_data():
    df = pd.read_csv(input_file, low_memory=False)
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df


def plot_time_series(df, col, title, ylabel, file_name):
    df_plot = df[["data", col]].copy()
    df_plot = df_plot.dropna(subset=["data", col])
    if df_plot.empty:
        print(f"Brak danych do wykresu {title}")
        return

    df_plot = df_plot.sort_values("data")
    df_plot = df_plot.set_index("data")
    df_plot = df_plot.resample("D").mean()

    plt.figure(figsize=(10, 4))
    plt.plot(df_plot.index, df_plot[col], color="#1f77b4", linewidth=1.2)
    plt.title(title)
    plt.xlabel("Data")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(output_dir / file_name, dpi=150)
    plt.close()


def plot_histogram(df, col, title, file_name):
    values = pd.to_numeric(df[col], errors="coerce").dropna()
    if values.empty:
        print(f"Brak danych do histogramu {title}")
        return

    plt.figure(figsize=(8, 4))
    plt.hist(values, bins=30, color="#2ca02c", alpha=0.8)
    plt.title(title)
    plt.xlabel(col)
    plt.ylabel("Liczba pomiarów")
    plt.tight_layout()
    plt.savefig(output_dir / file_name, dpi=150)
    plt.close()


def plot_boxplot(df, col, title, file_name):
    values = pd.to_numeric(df[col], errors="coerce").dropna()
    if values.empty:
        print(f"Brak danych do boxplota {title}")
        return

    plt.figure(figsize=(6, 4))
    plt.boxplot(values, vert=False)
    plt.title(title)
    plt.xlabel(col)
    plt.tight_layout()
    plt.savefig(output_dir / file_name, dpi=150)
    plt.close()


def create_summary(df):
    summary = []
    numeric_cols = ["PM25", "PM10", "NO2", "O3", "TA", "HA", "PA"]
    for col in numeric_cols:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce")
            summary.append((col, float(s.mean()), float(s.median()), float(s.std()), float(s.min()), float(s.max())))

    summary_df = pd.DataFrame(summary, columns=["kolumna", "średnia", "mediana", "odchylenie", "min", "max"])
    summary_path = output_dir / "summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    df = load_data()
    create_summary(df)

    for col, title, ylabel, file_name in [
        ("PM25", "PM2.5 w czasie", "PM2.5", "pm25_timeseries.png"),
        ("PM10", "PM10 w czasie", "PM10", "pm10_timeseries.png"),
        ("NO2", "NO2 w czasie", "NO2", "no2_timeseries.png"),
        ("O3", "O3 w czasie", "O3", "o3_timeseries.png"),
    ]:
        plot_time_series(df, col, title, ylabel, file_name)

    for col, title, file_name in [
        ("PM25", "Rozkład PM2.5", "pm25_hist.png"),
        ("PM10", "Rozkład PM10", "pm10_hist.png"),
        ("NO2", "Rozkład NO2", "no2_hist.png"),
        ("O3", "Rozkład O3", "o3_hist.png"),
    ]:
        plot_histogram(df, col, title, file_name)

    for col, title, file_name in [
        ("TA", "Rozkład temperatury", "temp_box.png"),
        ("HA", "Rozkład wilgotności", "humidity_box.png"),
        ("PA", "Rozkład ciśnienia", "pressure_box.png"),
    ]:
        plot_boxplot(df, col, title, file_name)

    print(f"Raport zapisano do: {output_dir}")

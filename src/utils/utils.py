import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def calculate_country_stats(df: pd.DataFrame, country: str) -> dict | None:
    data_filtered = df[df["Entity"] == country]

    if data_filtered.empty:
        return None

    metrics = [
        "Nitrogen oxide (NOx)",
        "Sulphur dioxide (SO2)",
        "Carbon monoxide (CO)",
        "Organic carbon (OC)",
        "Non-methane volatile organic compounds (NMVOC)",
        "Black carbon (BC)",
        "Ammonia (NH3)",
    ]
    results = {}

    for metric in metrics:
        values = data_filtered[metric].dropna()
        results[metric] = {
            "average": round(values.mean(), 2),
            "median": round(values.median(), 2),
            "std_dev": round(values.std(), 2),
        }

    return results

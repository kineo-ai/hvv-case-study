import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def calculate_country_stats(df: pd.DataFrame, country: str) -> dict | None:
    rounding_digits = 5
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
            "average": round(values.mean(), rounding_digits),
            "median": round(values.median(), rounding_digits),
            "std_dev": round(values.std(), rounding_digits),
        }

    return results

import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def calculate_country_stats(df: pd.DataFrame, country: str) -> dict | None:
    """
    Calculate the average, median, and standard deviation of air pollution metrics for a given country over the years.

    :param df: A pandas DataFrame containing the air pollution data.
    :param country: A string representing the country name.
    :return: A dictionary containing the average, median, and standard deviation of air pollution metrics for the given country or None if no data is found.
    """
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

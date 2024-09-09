import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def calculate_country_stats(df: pd.DataFrame, country: str) -> dict | None:
    """
    Calculate the average, median, and standard deviation of air pollution metrics for a given country over the years.

    :param df: A pandas DataFrame containing the air pollution data.
    :param country: A string representing the country name.
    :return: A dictionary containing the average, median, and standard deviation of air pollution metrics for the given country or `None` if no data is found.
    """
    data_filtered = df[df["Entity"] == country]

    results = get_stats(data_filtered)

    return results


def get_stats(df: pd.DataFrame) -> dict | None:
    rounding_digits = 5

    if df.empty:
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
    stats = {}

    for metric in metrics:
        values = df[metric].dropna()
        stats[metric] = {
            "average": round(values.mean(), rounding_digits),
            "median": round(values.median(), rounding_digits),
            "std_dev": round(values.std(), rounding_digits),
        }

    return stats

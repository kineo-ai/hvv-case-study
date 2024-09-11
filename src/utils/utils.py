import pandas as pd

PRECISION_DIGITS = 5


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the data from the CSV file and filter out the continents and income groups

    After  checking the data, we found some entities that are not countries, e.g. "Africa", "Asia", "Europe", "North America", "Oceania", "South America", "High-income countries", "Low-income countries", "Lower-middle-income countries", "Upper-middle-income countries", "World".
    We will filter out these entities to focus on the countries.

    :param filepath: A string representing the path to the CSV file.
    :return: A pandas DataFrame containing the air pollution data.
    """
    df = pd.read_csv(filepath)
    continents_income_filter = ~df["Entity"].isin(["Africa", "Asia", "Europe", "North America", "Oceania", "South America", "High-income countries", "Low-income countries", "Lower-middle-income countries", "Upper-middle-income countries", "World"])

    return df[continents_income_filter].copy()


def calculate_country_stats(df: pd.DataFrame, country: str) -> dict | None:
    """
    Get the average, median, and standard deviation of air pollution metrics for a given country over the years.

    :param df: A pandas DataFrame containing the air pollution data.
    :param country: A string representing the country name.
    :return: A dictionary containing the average, median, and standard deviation of air pollution metrics for the given country or `None` if no data is found.
    """
    data_filtered = df[df["Entity"] == country]

    return get_stats(data_filtered)


def calculate_year_stats(df: pd.DataFrame, year: int) -> dict | None:
    """
    Get the average, median, and standard deviation of air pollution metrics for all countries in a given year.

    :param df: A pandas DataFrame containing the air pollution data.
    :param year: An integer representing the year.
    :return: A dictionary containing the average, median, and standard deviation of air pollution metrics for all countries in the given year or `None` if no data is found.
    """
    data_filtered = df[df["Year"] == year]

    return get_stats(data_filtered)


def get_stats(df: pd.DataFrame) -> dict | None:
    """
    Calculate the average, median, and standard deviation of air pollution metrics

    :param df: A pandas DataFrame containing the air pollution data.
    :return: A dictionary containing the average, median, and standard deviation of air pollution metrics or `None` if the DataFrame is empty.
    """

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
        values = df[
            metric
        ].dropna()  # This would be better in a data preprocessing step
        stats[metric] = {
            "average": round(values.mean(), PRECISION_DIGITS),
            "median": round(values.median(), PRECISION_DIGITS),
            "std_dev": round(values.std(), PRECISION_DIGITS),
        }

    return stats

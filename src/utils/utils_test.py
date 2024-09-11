import pandas as pd
import numpy as np
import random
import string
from utils import calculate_country_stats

# The ERROR_TOLERANCE is rather high as the approximate distributions are not accurate unless numerous measurements/years are created.
ERROR_TOLERANCE = 1e-1
PRECISION_DIGITS = 5
NUM_ENTITIES = 10
NUM_YEARS = 10000
METRICS = [
    "Nitrogen oxide (NOx)",
    "Sulphur dioxide (SO2)",
    "Carbon monoxide (CO)",
    "Organic carbon (OC)",
    "Non-methane volatile organic compounds (NMVOC)",
    "Black carbon (BC)",
    "Ammonia (NH3)",
]
COLUMNS = ["Entity", "Code", "Year"].extend(METRICS)


def random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def random_years() -> int:
    return np.random.randint(1000, 9999, NUM_YEARS * NUM_ENTITIES)


def relative_error(expected, actual) -> float:
    if expected == actual:
        return 0
    return abs((expected - actual) / expected)


def _test_calculate_country_stats(
    metric_func, expected_avg, expected_median, expected_std
):
    """
    Generic helper function for calling the calculate_stats function.
    :param metric_func: A function that is used to generate the randomised values.
    :param expected_avg: A function that takes a column of records and returns the expected average of all measurements by country.
    :param expected_std: A function that takes a column of records and returns the expected std of all measurements by country.

    :asserts: if the expected average and expected standard deviation is within an relative error ERROR_TOLERANCE
    """
    # Arrange
    entities = [random_string(10) for _ in range(NUM_ENTITIES)] * NUM_YEARS
    codes = [random_string(3) for _ in range(NUM_ENTITIES)] * NUM_YEARS
    years = random_years()
    data = {
        "Entity": entities,
        "Code": codes,
        "Year": years,
    }
    for m in METRICS:
        data[m] = metric_func()
    df = pd.DataFrame(data, columns=COLUMNS)

    for entity in set(entities):
        # Act
        actual = calculate_country_stats(df, entity)
        for m in METRICS:
            metric_vector = df[df["Entity"] == entity][m]
            a_avg, e_avg = (
                actual[m]["average"],
                round(expected_avg(metric_vector), PRECISION_DIGITS),
            )
            a_median, e_median = (
                actual[m]["median"],
                round(expected_median(metric_vector), PRECISION_DIGITS),
            )
            a_std, e_std = (
                actual[m]["std_dev"],
                round(expected_std(metric_vector), PRECISION_DIGITS),
            )
            # Assert
            assert relative_error(a_avg, e_avg) < ERROR_TOLERANCE, (
                "Failed on Average a: %s, e: %s, re: %s"
                % (a_avg, str(e_avg), relative_error(a_avg, e_avg))
            )

            assert relative_error(a_median, e_median) < ERROR_TOLERANCE, (
                "Failed on Median a: %s, e: %s, re: %s"
                % (a_median, str(e_median), relative_error(a_median, e_median))
            )
            assert relative_error(a_std, e_std) < ERROR_TOLERANCE, (
                "Failed on Standard Deviation a: %s, e: %s, re: %s"
                % (a_std, str(e_std), relative_error(a_std, e_std))
            )


def test_calculate_country_stats_normal_dist():
    """
    This test-case fixes the parameters mu (mean) and sigma (stddev) to thereafter generate a normal distribution of values.
    The values will thereafter be used as the measurements for the calculation.
    """
    mu, sigma = random.random() * NUM_YEARS // 10, random.random() * NUM_YEARS // 1000

    def metric_func():
        return np.random.normal(mu, sigma, NUM_ENTITIES * NUM_YEARS)

    def expected_avg(vec):
        return mu

    def expected_median(vec):
        return vec.median()

    def expected_std(vec):
        return sigma

    _test_calculate_country_stats(
        metric_func, expected_avg, expected_median, expected_std
    )


def test_calculate_country_stats_uniform():
    """
    This test-case generates a uniformly pseudorandom distribution as measurements for the calculation.
    """

    def metric_func():
        return np.random.uniform(0, 10000, NUM_ENTITIES * NUM_YEARS)

    def expected_avg(vec):
        return vec.mean()

    def expected_median(vec):
        return vec.median()

    def expected_std(vec):
        return vec.std()

    _test_calculate_country_stats(
        metric_func, expected_avg, expected_median, expected_std
    )

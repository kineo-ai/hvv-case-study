import pytest
from app import app

EXPECTED_METRICS = [
    "Ammonia (NH3)",
    "Black carbon (BC)",
    "Carbon monoxide (CO)",
    "Nitrogen oxide (NOx)",
    "Non-methane volatile organic compounds (NMVOC)",
    "Organic carbon (OC)",
    "Sulphur dioxide (SO2)",
]


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_country_endpoint_valid(client):
    # Make a request to the /api/v1/country endpoint
    country = "Germany"
    response = client.get(f"/api/v1/country?name={country}")

    assert response.status_code == 200

    data = response.get_json()

    # Check the 'country' field
    assert "country" in data
    assert data["country"] == country

    # Check that 'statistics' field exists
    assert "statistics" in data

    for metric in EXPECTED_METRICS:
        assert metric in data["statistics"]

        # For each metric, check that the statistical keys are present
        for stat in ["average", "median", "std_dev"]:
            assert stat in data["statistics"][metric]

            # Check that the values are floats
            assert isinstance(data["statistics"][metric][stat], float)


def test_country_endpoint_invalid(client):
    response = client.get("/api/v1/country")
    assert response.status_code == 400

    response = client.get("/api/v1/country?name=InvalidCountry")
    assert response.status_code == 404


def test_year_endpoint_valid(client):
    year = 2000
    response = client.get(f"/api/v1/year?value={year}")

    assert response.status_code == 200

    data = response.get_json()

    # Check the 'year' field
    assert "year" in data
    assert data["year"] == year

    # Check that 'statistics' field exists
    assert "statistics" in data

    for metric in EXPECTED_METRICS:
        assert metric in data["statistics"]

        # For each metric, check that the statistical keys are present
        for stat in ["average", "median", "std_dev"]:
            assert stat in data["statistics"][metric]

            # Check that the values are floats
            assert isinstance(data["statistics"][metric][stat], float)


def test_year_endpoint_invalid(client):
    response = client.get("/api/v1/year")
    assert response.status_code == 400

    response = client.get("/api/v1/year?value=1000")
    assert response.status_code == 404

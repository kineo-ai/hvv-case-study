from flask import Flask, jsonify, request
from utils.utils import load_data, calculate_country_stats

app = Flask(__name__)


# Load dataset
df = load_data("./data/air-pollution.csv")


@app.route("/api/v1/country", methods=["GET"])
def get_country_pollution_stats():
    try:
        country = request.args.get("name").title()
    except AttributeError:
        country = None

    if not country:
        return jsonify({"error": "Could not parse country name"}), 400

    country_stats = calculate_country_stats(df, country)

    if country_stats is None:
        return jsonify({"error": f"No data found for {country}"}), 404

    return jsonify({"country": country, "statistics": country_stats})


@app.route("/", methods=["GET"])
def root():
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

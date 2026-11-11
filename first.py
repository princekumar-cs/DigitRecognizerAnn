
from flask import Flask, jsonify, request
from flask_cors import CORS

import recognize as r

app = Flask(__name__)

# Enable browser requests
CORS(app)


@app.route("/hello", methods=["GET"])
def hello():
    return "working"


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        matrix = data["matrix"]

        # print("Received matrix:", matrix)

        result = r.run(matrix)

        return jsonify({
            "prediction": str(result),
            "status": "success"
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

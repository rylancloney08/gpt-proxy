from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

POWER_AUTOMATE_WEBHOOK_URL = "https://prod-86.westus.logic.azure.com:443/workflows/b609333709a04df48973e6a8d173e415/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Z8jCtiHgohR8TPhNBjphKL2FupO2lbOHNgXtagQ2k4k"

@app.route("/", methods=["POST"])
def forward_to_power_automate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        response = requests.post(
            POWER_AUTOMATE_WEBHOOK_URL,
            json=data,
            headers={"Content-Type": "application/json"}
        )

        return jsonify({
            "forwarded": True,
            "status_code": response.status_code,
            "response_text": response.text
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)


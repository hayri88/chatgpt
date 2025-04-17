from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# Jira instellingen uit environment variables
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")

auth = base64.b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()

headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

@app.route("/maak-taak", methods=["POST"])
def maak_taak():
    data = request.json
    summary = data.get("titel")
    beschrijving = data.get("beschrijving", "")
    assignee = data.get("toewijzen_aan", None)
    issuetype = data.get("issuetype", "Task")  # standaard Task als niet opgegeven

    payload = {
        "fields": {
            "project": {"key": "GND"},
            "summary": summary,
            "description": beschrijving,
            "issuetype": {"name": issuetype}
        }
    }

    if assignee:
        payload["fields"]["assignee"] = {"name": assignee}

    response = requests.post(
        f"{JIRA_DOMAIN}/rest/api/3/issue",
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        return jsonify({"message": "Taak aangemaakt!", "key": response.json()["key"]}), 201
    else:
        return jsonify({"error": response.text}), response.status_code

@app.route("/", methods=["GET"])
def index():
    return "ChatGPT → Jira API werkt ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template, request
import requests
import os  # Added for environment variables

app = Flask(__name__)

# Get API key from environment variable (set in Render)
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
MODEL_NAME = "mistral-tiny"  # Or "mistral-small"

def get_mistral_response(prompt):
    """Gets a response from the Mistral API."""
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except KeyError:
        return "An unexpected error occurred with the API response."

@app.route("/", methods=["GET", "POST"])
def index():
    """Handles the main page and chatbot interactions."""
    user_input = None
    mistral_response = None

    if request.method == "POST":
        user_input = request.form["user_input"]
        mistral_response = get_mistral_response(user_input)

    return render_template("index.html", user_input=user_input, mistral_response=mistral_response)

if __name__ == "__main__":
    # Production configuration
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 4000)),  # Get port from Render
        debug=False  # Disable debug mode in production
    )
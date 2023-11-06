from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
import logging
import json



app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
@app.route('/')
@app.route('/api', methods=['POST'])
def api():
    max_tokens = int(os.getenv("MAXTOKENS"))
    load_dotenv()

    url = f"{os.getenv('ENDPOINT')}/openai/deployments/gpt3516k/chat/completions?api-version=2023-05-15"
    headers = {
        "Content-Type": "application/json",
        "api-key": os.getenv("KEY")
    }

    for i in range(int(os.getenv("ITERATIONS"))):
        data = {"max_tokens": max_tokens, "messages":[{"role": "system", "content": ""},{"role": "user", "content": "Hi"}]}
        logging.info(json.dumps(data, indent=4))
        try:
            response = requests.post(url, headers=headers, json=data)
            status = response.status_code
            if (status != 200):
                return jsonify(response.json()), status
            return jsonify({"message": f"Finished call with status: {status}"})
        except Exception as e:
            return jsonify({"error": f"Call failed with exception: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
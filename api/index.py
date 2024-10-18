from flask import Flask, jsonify
import threading
import time
import requests

app = Flask(__name__)

# URL to call
website_url = "https://hulkbuster-flask-test.hf.space"

# To store the last response from the website
website_data = {}

# Function to call the website every 10 seconds
def call_website_periodically():
    global website_data
    while True:
        try:
            # Make a request to the website
            response = requests.get(website_url)
            website_data['status_code'] = response.status_code
            website_data['content'] = response.text
            print(f"Called {website_url}, Status: {response.status_code}")
        except Exception as e:
            website_data['error'] = str(e)
            print(f"Error calling {website_url}: {e}")
        
        # Wait for 10 seconds before calling the website again
        time.sleep(10)

# Start the background thread
def start_background_task():
    thread = threading.Thread(target=call_website_periodically)
    thread.daemon = True  # Daemonize thread to stop with the main program
    thread.start()

# API to fetch the latest website data
@app.route('/get_website_data', methods=['GET'])
def get_website_data():
    return jsonify(website_data)

if __name__ == '__main__':
    start_background_task()
    app.run(debug=True)

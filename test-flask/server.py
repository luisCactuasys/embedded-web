from flask import Flask, request, jsonify, render_template_string
import os
import datetime
import time

# Define the log file path
log_file = "/home/luiscarlos/workspace/tux100/BBB_web/embedded-web/test-flask/from-rasp.log"


app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    # Simple HTML page with JavaScript to fetch the duty cycle
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Duty Cycle Monitor</title>
        <script>
            // Function to periodically fetch the duty cycle
            function fetchDutyCycle() {
                fetch('/get-duty-cycle')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('dutyCycle').innerText = data.duty_cycle;
                    })
                    .catch(error => console.error('Error fetching duty cycle:', error));
            }
            
            // Refresh the value every 2 seconds
            setInterval(fetchDutyCycle, 2000);
        </script>
    </head>
    <body>
        <h1>Duty Cycle Monitor</h1>
        <p>Current Duty Cycle: <strong id="dutyCycle">Loading...</strong></p>
    </body>
    </html>
    """
    return render_template_string(html_content)


# Define your API key
API_KEY = "my-secret-api-key"

# Function to log events
def log_event(setting):
    with open(log_file, "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} - Setting changed to: {setting}\n")

# Route to get the duty cycle from the log file
@app.route('/get-duty-cycle')
def get_duty_cycle():
    try:
        # Read the duty cycle value from the log file
        with open('from-rasp.log', 'r') as file:
            duty_cycle = file.read().strip()
        return jsonify({"duty_cycle": duty_cycle})
    except FileNotFoundError:
        return jsonify({"duty_cycle": "File not found"}), 404
    except Exception as e:
        return jsonify({"duty_cycle": str(e)}), 500


# This route will handle POST requests with duty cycle data
@app.route('/notify', methods=['POST'])
def notify():

    # Check for the API key in headers
    #api_key = request.headers.get('x-api-key')
    #if api_key != API_KEY:
    #    return jsonify({"message": "Unauthorized"}), 403

    # Get the JSON data from the POST request
    data = request.get_json()
    
    if data and 'duty_cycle' in data:
        duty_cycle = data['duty_cycle']
        print(f"Received duty cycle update: {duty_cycle}")

        # Log or process the received duty cycle as needed
        log_event(f"Received duty cycle update: {duty_cycle}")
        # For example, you can save it to a file or take other actions
        
        # Send a response back to the client (the board)
        return jsonify({"message": "Duty cycle received", "duty_cycle": duty_cycle}), 200
    else:
        # Handle cases where the data is missing or incorrect
        return jsonify({"message": "Invalid data"}), 400

# Start the server on port 5000 (accessible from any IP)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))


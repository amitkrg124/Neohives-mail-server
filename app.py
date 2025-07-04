from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (for development)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.form or request.json or {}
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        # You can add more fields as needed

        # Placeholder for email sending logic
        # For now, just log/print the data
        print(f"Received contact form: Name={name}, Email={email}, Message={message}")

        # Respond with JSON (as expected by frontend)
        return jsonify({'success': True, 'message': 'Mail sent successfully!'}), 200
    except Exception as e:
        print(f"Error in webhook: {e}")
        return jsonify({'success': False, 'message': 'Failed to send mail.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
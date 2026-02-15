"""
Keep-alive service to prevent Render free tier from sleeping.
This creates a simple web server that can be pinged by external services.
"""
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!", 200

@app.route('/health')
def health():
    return {"status": "healthy", "service": "telegram-bot"}, 200

def run():
    """Run the Flask app on the port specified by Render."""
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def keep_alive():
    """Start the web server in a background thread."""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print(f"Keep-alive server started on port {os.environ.get('PORT', 8080)}")

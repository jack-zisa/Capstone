from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from routes.auth import auth_blueprint
from routes.fitbit import fitbit_blueprint
from routes.analysis import analysis_blueprint
from utils.cloud_utils import access_secret
import redis
import os

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(auth_blueprint)
app.register_blueprint(fitbit_blueprint)
app.register_blueprint(analysis_blueprint)
app.secret_key = access_secret('app_secret_key')

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # Optional for session signing
app.config['SESSION_KEY_PREFIX'] = 'flask:'
app.config['SESSION_REDIS'] = redis.from_url(f'redis://:{access_secret("redis_secret_key")}@redis-15604.c1.us-central1-2.gce.redns.redis-cloud.com:15604')
Session(app)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/genuine-flight-397402-20e701a5e711.json"

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)

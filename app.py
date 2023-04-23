import os
import sys
import json
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, redirect, request

sys.path.append('./sources')
from weatherAPI import get_weather

# Loading env vars
load_dotenv()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

API_KEY=os.getenv('API_KEY')

# Make sure API key is set
if API_KEY == None:
  raise RuntimeError("API_KEY not set!")

@app.route("/")
def index():
  # Should be passed to layout:
  # List of regions
  # Time of last refresh the predictions
  return render_template("index.html")


# Endpoint to make fresh predictions and store them in the file or db
@app.route("/api/predictions/refresh", methods=["POST"])
def api_refresh_predictions():
  # Check the API_KEY
  print('API_KEY passed!' if 'token' in request.json is not None else 'API_KEY NOT passed!')

  # Refresh predictions file of db
  return jsonify(status="OK")


# The same as above but for client
@app.route("/predictions/refresh", methods=["POST"])
def refresh_predictions():
  return redirect("/")


# Endpoint to get predictions for all regions
@app.route("/api/predictions", methods=["POST"])
def api_get_predictions():
  # Check the API_KEY
  print('API_KEY passed!' if 'token' in request.json is not None else 'API_KEY NOT passed!')

  # Return predictions file of db data
  return jsonify(status="OK")


# The same as above but for client
@app.route("/predictions", methods=["POST"])
def get_predictions():
  # Create a separate UI block for predictions
  return redirect("/")

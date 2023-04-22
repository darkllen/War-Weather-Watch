import os
import sys
import json
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, redirect

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

# Temporary var for distinguishing fresh/not fresh predictions in the file or db
is_fresh = False

@app.route("/")
def index():
  # TODO: Check the latest prediction and decide if it is considered as fresh
  # Time along with fresh can be passed to the layout
  # List of regions also should be passed to the layout
  return render_template("index.html", is_fresh_prediction=is_fresh)


# Endpoint to make fresh predictions and store them in the file or db
@app.route("/api/predictions/refresh", methods=["POST"])
def api_refresh_predictions():
  # Check the API_KEY
  # Refresh predictions file of db
  return jsonify(status="OK")


# The same as above but for client
@app.route("/predictions/refresh", methods=["POST"])
def refresh_predictions():
  global is_fresh
  is_fresh = True
  return redirect("/")


# Endpoint to get predictions for all regions
@app.route("/api/predictions", methods=["POST"])
def api_get_predictions():
  # Check the API_KEY
  # Return predictions file of db data
  # Figure out a way to make predictions for just one region
  return jsonify(status="OK")


# The same as above but for client
@app.route("/predictions", methods=["POST"])
def get_predictions():
  return redirect("/")

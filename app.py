import os
import sys
import json
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, jsonify, render_template, redirect, request

sys.path.append('./')
from sources.weatherAPI import get_weather
from ml.make_prediction import REGIONS, update_prediction_for_next_12_hours
from db.predictions import save_predictions, get_predictions

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

region = None
predictions = None

@app.route("/")
def index():
  print(region)
  print(predictions)
  
  regions = REGIONS.keys()
  sorted_regions = sorted(regions)
  return render_template("index.html", regions=sorted_regions, region=region, predictions=predictions)


# Endpoint to make fresh predictions and store them in the file or db
@app.route("/api/predictions/refresh", methods=["POST"])
def api_refresh_predictions():
  # Check the API_KEY
  if 'token' in request.json and request.json['token'] == API_KEY:
    # Update predictions and store that data in the db
    data = update_prediction_for_next_12_hours()
    data_vals = data.values.tolist()
    save_predictions(data_vals)

    return jsonify(status="OK")
  else:
    raise RuntimeError("API_KEY is incorrect!")


# The same as above but for a client
@app.route("/predictions/refresh", methods=["POST"])
def client_refresh_predictions():
  data = update_prediction_for_next_12_hours()
  data_vals = data.values.tolist()
  save_predictions(data_vals)

  return redirect("/")


# Endpoint to get predictions for all regions
@app.route("/api/predictions", methods=["POST"])
def api_get_predictions():
  # Check the API_KEY
  if 'token' in request.json and request.json['token'] == API_KEY:
    regions = request.json['regions'] if 'regions' in request.json else []

    # Get predictions and return them
    predictions = get_predictions(regions, start_datetime=datetime.now())
    return predictions
  else:
    raise RuntimeError("API_KEY is incorrect!")


# The same as above but for a client
@app.route("/predictions", methods=["POST"])
def client_get_predictions():
  global region
  region = request.form.get('region')
  regions = [] if region == 'All' else [region]

  global predictions
  # Get predictions and return them
  predictions = get_predictions(regions, start_datetime=datetime.now())
  return redirect("/")

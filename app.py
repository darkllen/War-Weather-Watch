import os
import sys
import json
from dotenv import load_dotenv
from flask import Flask, render_template

sys.path.append('./sources')
from weatherAPI import get_weather

# Loading env vars
load_dotenv()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
  default_weather = get_weather()
  return render_template("index.html", default_weather = json.dumps(default_weather))
  # return render_template("index.html")

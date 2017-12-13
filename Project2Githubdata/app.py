from flask import Flask, jsonify, render_template
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc, extract, select, Table
from collections import defaultdict
# from dateutil.relativedelta import relativedelta
        

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return "InternationalUniversities"        


if __name__ == "__main__":
    app.run(debug=True)
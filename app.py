# Importing Dependencies

import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

# Database Setup

engine = create_engine("sqlite:///metroridership.sqlite")

# Relect the existing database into a new model.

Base = automap_base()

# Reflect the table.

Base.prepare(engine, reflect=True)

# Save a reference to the metro_ridership table as "Ridership".

Ridership = Base.classes.metro_ridership

# Save a reference to the metro_timeperiod table as "TimePeriod".

Timeperiod = Base.classes.metro_timeperiod_ridership

# Create our session link from Python to the database.

session = Session(engine)

# Flask set up.

app = Flask(__name__)

# Flask Routes

@app.route("/")
def index():
	# Return the homepage.
	return render_template("index.html")

@app.route("/top25stationsaverage")
def top25stations():
    average_top_25 = session.query(Ridership.STATION, func.avg(Ridership.RIDERS_PER_WEEKDAY)).group_by(Ridership.STATION).\
    order_by(func.avg(Ridership.RIDERS_PER_WEEKDAY).desc()).limit(25).all()

    average_top_25_dict = dict(average_top_25)
    
    top_25_stations = []
    top_25_averages = []

    for key, value in average_top_25_dict.items():
        top_25_stations.append(key)
        top_25_averages.append(value)

    return jsonify(top_25_stations, top_25_averages)
    
@app.route("/bottom25stationsaverage")
def bottom25stations():
    average_bottom_25 = session.query(Ridership.STATION, func.avg(Ridership.RIDERS_PER_WEEKDAY)).group_by(Ridership.STATION).\
    order_by(func.avg(Ridership.RIDERS_PER_WEEKDAY).asc()).limit(25).all()

    average_bottom_25_dict = dict(average_bottom_25)

    bottom_25_stations = []
    bottom_25_averages = []

    for key, value in average_bottom_25_dict.items():
        bottom_25_stations.append(key)
        bottom_25_averages.append(value)

    return jsonify(bottom_25_stations, bottom_25_averages)

@app.route("/top25stationstotal")
def totaltop25stations():
    top_25_total = session.query(Ridership.STATION, func.sum(Ridership.RIDERS_PER_WEEKDAY)).group_by(Ridership.STATION).\
    order_by(func.sum(Ridership.RIDERS_PER_WEEKDAY).desc()).limit(25).all()

    top_25_total_ridership_dict = dict(top_25_total)
    
    top_25_total_stations = []
    top_25_total_ridership = []

    for key, value in top_25_total_ridership_dict.items():
        top_25_total_stations.append(key)
        top_25_total_ridership.append(value)

    return jsonify(top_25_total_stations, top_25_total_ridership)

@app.route("/bottom25stationstotal")
def totalbottom25stations():

    bottom_25_total = session.query(Ridership.STATION, func.sum(Ridership.RIDERS_PER_WEEKDAY)).group_by(Ridership.STATION).\
    order_by(func.sum(Ridership.RIDERS_PER_WEEKDAY).asc()).limit(25).all()

    bottom_25_total_ridership_dict = dict(bottom_25_total)

    bottom_25_total_stations = []
    bottom_25_total_ridership = []

    for key, value in bottom_25_total_ridership_dict.items():
        bottom_25_total_stations.append(key)
        bottom_25_total_ridership.append(value)

    return jsonify(bottom_25_total_stations, bottom_25_total_ridership)

@app.route("/timeperiodaverage")
def timeperiod_average_ridership():
    timeperiod_average = session.query(Timeperiod.PERIOD, func.avg(Timeperiod.RIDERS_PER_WEEKDAY)).\
    group_by(Timeperiod.PERIOD).all()

    timeperiod_average_ridership = dict(timeperiod_average)

    time_periods = []
    time_period_averages = []

    for key, value in timeperiod_average_ridership.items():
        time_periods.append(key)
        time_period_averages.append(value)

    return jsonify(time_periods, time_period_averages)

@app.route("/timeperiodridershiptotal")
def timeperiodtotalridership():
    timeperiod_total =  session.query(Timeperiod.PERIOD, func.sum(Timeperiod.RIDERS_PER_WEEKDAY)).\
    group_by(Timeperiod.PERIOD).all()

    timeperiod_total_ridership = dict(timeperiod_total)

    time_periods_total = []
    time_period_total_ridership = []

    for key, value in timeperiod_total_ridership.items():
        time_periods_total.append(key)
        time_period_total_ridership.append(value)

    return jsonify(time_periods_total, time_period_total_ridership)

# initiate the app.py.

if __name__ == '__main__':
    app.run()






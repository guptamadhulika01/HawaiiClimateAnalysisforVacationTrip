# 1. import dependencies
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# 2. Create an app
app = Flask(__name__)

# 3. set route

# 1: define all available routes 
@app.route("/")
def welcome():
    return (
        f"<h1>Welcome to the Hawaii Weather Analysis!<\h1><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/Home Page<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/starDate/<start><br/>"
        f"/api/v1.0/startAndendDate<start>/<end>"
       
    )
#2 * `/api/v1.0/precipitation`

  #* Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

 # * Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def names():
    """Return a list of precipitation results """
    # Query all Measurement class
    session = Session(engine)
    results = (session.query(Measurement.prcp, Measurement.date).\
                       filter(Measurement.date > '2016-08-03').\
                        order_by(Measurement.date).all())

    # Convert list of tuples into normal list
    PrecipitationResults = list(np.ravel(results))

    return jsonify(PrecipitationResults)

#* `/api/v1.0/stations`

 # * Return a JSON list of stations from the dataset.


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations class
    session = Session(engine)
    results = session.query(Station.station, Station.name).distinct().all()

    # Create a dictionary from the row data and append to a list of station_names

    station_names = []
    for name, station in results:
        station_dict = {}
        station_dict["name"] = name
        station_dict["station"] = station
       
        station_names.append(station_dict)

    return jsonify(station_names)

#* `/api/v1.0/tobs`
#  * query for the dates and temperature observations from a year from the last data point.
    #last data point(last date of observations recorded)""
@app.route("/api/v1.0/tobs")


def Temp_obs():
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    return jsonify(results)
    

   

#  * Return a JSON list of Temperature Observations (tobs) for the previous year.
    #def temp_obs()




# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/starDate/<start>")
@app.route("/api/v1.0/startAndendDate<start>/<end>")

def dates(start = None, end = None):
    session = Session(engine)
    select = [func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    
    if not end:
        results = session.query(*select).filter(Measurement.date >=start).all()
        return jsonify(results)

    results = session.query(*select).filter(Measurement.date >=start).filter(Measurement.date <=end).all()
    return jsonify(results)
    

if __name__ == "__main__":
       app.run(debug=True) 

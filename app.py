#Import Flask, SqlAlchemy, Numpy
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

########################
#Database Time
########################

#Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect the Existing Database
Base = automap_base()

#Reflect The Tables
Base.prepare(engine, reflect = True)

#Save References
Stations = Base.classes.station
Measurements = Base.classes.measurement


#Create the App
app=Flask(__name__)

# 3. Define static routes


@app.route("/")
def index():
    """List the Routes"""
    return (
        f"Welcome to my homework. There are a few routes you can take here!"
        f"Precipitation: /api/v1.0/precipitation"
        f"Stations: /api/v1.0/stations"
        f"Temperature: /api/v1.0/tobs"
        f"Starting Point Data: /api/v1.0/<start>"
        f"A Range of Dates: /api/v1.0/<start>/<end>"
    )

#@app.route("/api/v1.0/precipitation")
#def precipitation():

@app.route("/api/v1.0/stations")
def stations():
    #Create The Session
    session = Session(engine)

    #Query the Stations
    results = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation)

    session.close()

    #Convert!
    All_stations = list(np.ravel(results))

    return jsonify(All_stations)

#@app.route("/api/v1.0/tobs")
#def temperature()

#@app.route("/api/v1.0/<start>")
#def start()

#@app.route("/api/v1.0/<start>/<end>")
#def range()

if __name__ == "__main__":
    app.run(debug=True)
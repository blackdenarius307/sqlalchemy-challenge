#Import Flask, SqlAlchemy, Numpy
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt

##############
#Database Time
##############

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

#Define routes


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

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create The Session
    session = Session(engine)

    #Query the Measurements
    resultprecip = session.query(Measurements.date, Measurements.prcp)

    session.close()

    #Convert!
    All_Precip = []
    for date, prcp in resultprecip:
        Prcp_dict = {}
        Prcp_dict['date']= date
        Prcp_dict['precipitation']= prcp
        All_Precip.append(Prcp_dict)
    
    return jsonify(All_Precip)


@app.route("/api/v1.0/stations")
def stations():
    #Create The Session
    session = Session(engine)

    #Query the Stations
    resultstation = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation)

    session.close()

    #Convert!
    All_stations = []
    for station, name, latitude, longitude, elevation in resultstation:
        stations_dict = {}
        stations_dict['station'] = station
        stations_dict['name'] = name
        stations_dict['latitude']= latitude
        stations_dict['longitude']= longitude
        stations_dict['elevation']= elevation
        All_stations.append(stations_dict)

    return jsonify(All_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    #Create The Session
    session = Session(engine)
    
    #Latest Date Stuff
    Latestdate = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    #Year ago
    Year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(weeks=52)
    #Dates, temps, station
    resulttemp = session.query(Measurements.date, Measurements.tobs, Measurements.station).\
    filter(Measurements.date >= Year_ago).\
    filter(Measurements.station == 'USC00519281')

    session.close()

    #Convert!
    All_temps = []
    for date, tobs, station in resulttemp:
        temp_dict = {}
        temp_dict['date']= date
        temp_dict['temperature'] = tobs
        temp_dict['station'] = station
        All_temps.append(temp_dict)

    return jsonify(All_temps)




#@app.route("/api/v1.0/<start>")
#def start()

#@app.route("/api/v1.0/<start>/<end>")
#def range()

if __name__ == "__main__":
    app.run(debug=True)
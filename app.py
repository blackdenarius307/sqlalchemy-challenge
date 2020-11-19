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
    return (
        """Welcome to my homework. There are a few routes you can take here!<br>
        Precipitation: /api/v1.0/precipitation<br>
        Stations: /api/v1.0/stations<br>
        Temperature: /api/v1.0/tobs<br>
        Starting Point Data: /api/v1.0/start date Format Start Date as YYYY-MM-DD<br> 
        A Range of Dates: /api/v1.0/start date/end date Format Start and End Date as YYYY-MM-DD"""
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


@app.route("/api/v1.0/<start>")
def temp_by_start(start):
    #Create the Session
    session = Session(engine)

    #Filtering Queries
    lowesttemp = session.query(func.min(Measurements.tobs)).\
        filter(Measurements.date >= f'{start}').all()[0][0]
    highesttemp = session.query(func.max(Measurements.tobs)).\
        filter(Measurements.date >= f'{start}').all()[0][0]
    avgtemp = session.query(func.avg(Measurements.tobs)).\
        filter(Measurements.date >= f'{start}').all()[0][0]
    
    session.close()

    #Convert
    Allsummary = []
    Start_dict = {}
    Start_dict['Minimum'] = lowesttemp
    Start_dict['Maximum'] = highesttemp
    Start_dict['Average'] = avgtemp
    Allsummary.append(Start_dict)

    return jsonify(Allsummary)

@app.route("/api/v1.0/<start>/<end>")
def range_between_dates(start, end):
    #Create the Session
    session = Session(engine)

    #Filtering Queries
    lowesttemp = session.query(func.min(Measurements.tobs)).\
        filter(Measurements.date >= f'{start}').\
        filter(Measurements.date <= f'{end}').all()[0][0]
    highesttemp = session.query(func.max(Measurements.tobs)).\
        filter(Measurements.date >= f'{start}').\
        filter(Measurements.date <= f'{end}').all()[0][0]
    avgtemp = session.query(func.avg(Measurements.tobs)).\
        filter(Measurements.date >= f'{start}').\
        filter(Measurements.date <= f'{end}').all()[0][0]

    session.close()

    #Convert
    Rangesummary = []
    Range_dict = {}
    Range_dict['Minimum'] = lowesttemp
    Range_dict['Maximum'] = highesttemp
    Range_dict['Average'] = avgtemp
    Rangesummary.append(Range_dict)

    return jsonify(Rangesummary)

if __name__ == "__main__":
    app.run(debug=True)
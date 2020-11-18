#Import Flask
from flask import Flask

#Create the App
app=Flask(__name__)

# 3. Define static routes


@app.route("/")
def index():
    return """Welcome to my homework. There are a few routes you can take here! 
    Precipitation: /api/v1.0/precipitation
    Stations: /api/v1.0/stations
    Temperature: /api/v1.0/tobs
    Starting Point Data: /api/v1.0/<start>
    A Range of Dates: /api/v1.0/<start>/<end>"""


#@app.route("/api/v1.0/precipitation")
#def precipitation():

#@app.route("/api/v1.0/stations")
#def stations()

#@app.route("/api/v1.0/tobs")
#def temperature()

#@app.route("/api/v1.0/<start>")
#def start()

#@app.route("/api/v1.0/<start>/<end>")
#def range()

if __name__ == "__main__":
    app.run(debug=True)
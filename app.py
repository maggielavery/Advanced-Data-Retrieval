import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def Home():
   
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/tobs")
def tobs():
    
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date)

    last_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = tobs
        last_tobs.append(tobs_dict)

    return jsonify(last_tobs)

@app.route("/api/v1.0/<start>")
def start(start=None):  
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    temps = list(np.ravel(results))
  
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
  
    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)

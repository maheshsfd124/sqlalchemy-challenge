import numpy as np
from numpy.core.arrayprint import DatetimeFormat

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for date,prcp in results:
        prcp_dict={}
        prcp_dict["date"]= date
        prcp_dict["prcp"]= prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.station).distinct().all()

    session.close()
    all_names = list(np.ravel(results))
  
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    temp_results = (
    session.query(Measurement.date, Measurement.tobs)
    .filter(Measurement.date > '2016-08-23')
    .filter(Measurement.station == 'USC00519281')
    .order_by(Measurement.date)
    .all() )       

    session.close()
    all_prcp_prev = []
    for date,tobs in temp_results:
        prcp_dict_prev={}
        prcp_dict_prev["date"]= date
        prcp_dict_prev["tobs"]= tobs
        all_prcp_prev.append(prcp_dict_prev)
    
    return jsonify(all_prcp_prev)

if __name__ == '__main__':
    app.run(debug=True)
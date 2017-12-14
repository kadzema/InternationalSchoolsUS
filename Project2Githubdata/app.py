from flask import Flask, jsonify, render_template
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc, extract, select, Table
from collections import defaultdict
from flask import Flask, jsonify
from sqlalchemy import extract  
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
#################################################
# Database Setup
#################################################
engine=create_engine("sqlite:///iie.sqlite",echo=False)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

  # print(Base.classes.keys())
# Save reference to the table
Student_city=Base.classes.studentcity
University_states=Base.classes.universitystates
UniversityStats = Base.classes.UniversityStats
# Create our session (link) from Python to the DB
session = Session(engine)
        

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return ( 
        f"/university-students/&lt;year&gt;<br/>"
        f"/state-universities/&lt;year&gt;<end>"
        
    )
@app.route("/university-students/<year>")   
def students(year):
    all_students=session.query(UniversityStats.Place,UniversityStats.StudentsCount,UniversityStats.Lng,UniversityStats.Lat,UniversityStats.Year).filter(UniversityStats.Year==year).all()
    student_list = []
    for s in all_students:
        student_dict={}
        student_dict["Place"]=s[0]
        student_dict["StudentsCount"]=s[1]
        student_dict["Lng"]=s[2]
        student_dict["Lat"]=s[3]
        student_dict["Year"]=s[4]
        student_list.append(student_dict)
    # all_names = list(np.ravel( all_students ))
    
    return jsonify( student_list)
@app.route("/state-universities/<year>")   
def states(year):
    
    #all_states=session.query(University_states.State,University_states.Count).all()            
    all_states = session.query(UniversityStats.State, func.count(UniversityStats.State)).filter(UniversityStats.Year==year).group_by(UniversityStats.State).all()
    state_list=[]
    for state  in all_states:
        state_dict={}
        state_dict["State"]=state[0]
        state_dict["Count"]=state[1]
        state_list.append(state_dict)
    
    return jsonify( state_list)    

if __name__ == "__main__":
    app.run(debug=True)

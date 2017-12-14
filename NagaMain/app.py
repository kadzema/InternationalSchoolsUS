#import dependencies
import pandas as pd
import json
from flask import Flask, render_template,jsonify

# Imports the method used for connecting to DBs
from sqlalchemy import create_engine

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.declarative import declarative_base

# Allow us to declare column types
from sqlalchemy import Column, Integer, String, Float ,Date

from sqlalchemy.orm import Session

from sqlalchemy import inspect
from sqlalchemy.ext.automap import automap_base

from sqlalchemy import create_engine, inspect, func, desc, extract, select, Table
from collections import defaultdict

# ===========================Database Connection========================

# Create Database Connection
engine = create_engine("sqlite:///censusdata.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)
conn = engine.connect()

query = "select CountyID,CountyName,TotalPopulation,Year, Over149999 as Over150000, Over200000, 'AIAN' as Race from census_aian union "
query += "select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Asian' as Race from census_asian where race = 'Asian' union "
query += "select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Black' as Race from census_black union "
query += "select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Hispanic' as Race from census_hispanic union "
query += "select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Mixed' as Race from census_mixed union "            
query += "select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Other' as Race from census_other union "                           
query += "select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Whites' as Race from census_whites order by CountyName, Year"                           
df_all = pd.read_sql_query(query, conn)

df_all['CountyPopulation'] = df_all['TotalPopulation'].groupby([df_all['CountyName'],df_all['Year']]).transform('sum')
df_all['TotalPercentage'] = (df_all["TotalPopulation"]/df_all['CountyPopulation'])*100
df_all['Over150Population'] = df_all['Over150000'].groupby([df_all['CountyName'],df_all['Year']]).transform('sum')
df_all['Over150Percentage'] = (df_all["Over150000"]/df_all['Over150Population'])*100
df_all['Over200Population'] = df_all['Over200000'].groupby([df_all['CountyName'],df_all['Year']]).transform('sum')
df_all['Over200Percentage'] = (df_all["Over200000"]/df_all['Over200Population'])*100

# ===========================Flask Connection==========================
app = Flask(__name__)

@app.route('/')
# Return the dashboard homepage.
def index():
    return render_template('index.html')

@app.route('/county/<cname>')
def countyTotal(cname):
    county_data=df_all.loc[df_all["CountyName"]==cname]
    finalresult = county_data.to_dict(orient='records')
    return jsonify(finalresult)

@app.route('/selectcounty/<cname>')
# select the county population
def choosecounty(cname):

    county_data=merged_new.loc[merged_new["CountyName"]== cname]
    finalresult=county_data.to_dict(orient='records')
    return jsonify(finalresult)

@app.route('/highincomeover200000/<cname>')
# select the county population
def highincome(cname):

    high_data=high_income.loc[high_income["CountyName"]== cname]
    high_value=high_data.to_dict(orient='records')
    return jsonify(high_value)

@app.route('/highincomeover150000/<cname>')
# select the county population
def lowincome(cname):

    low_data=low_income.loc[low_income["CountyName"]== cname]
    low_value=low_data.to_dict(orient='records')
    return jsonify(low_value)

@app.route("/origin")
#publish the student origin
def origin():
    engine = create_engine("sqlite:///iie.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    origin = Base.classes.origin

    originResult = session.query(origin.Origin, origin.studentcount, origin.year).all()

    e = defaultdict(list)
    for element in originResult:
        e["origins"].append({'origin': str(element[0]), 'studentcount': element[1], 'year': element[2]})

    return jsonify(e)


@app.route("/univCounty")
#publish the international student placement
def univCounty():
    engine = create_engine("sqlite:///iie.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    univ = Base.classes.university_county

    univResult = session.query(univ.PlaceofDestination, univ.City, univ.State, univ.Students, univ.Year, univ.County).all()

    e = defaultdict(list)
    for element in univResult:
        e["universities"].append({'university': str(element[0]), 'city': element[1], 'state': element[2], 'students': element[3], 'year': element[4], 'county':element[5]})
    return jsonify(e)

@app.route("/university-students/<year>")   
def students(year):
    engine = create_engine("sqlite:///iie.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    UniversityStats = Base.classes.UniversityStats
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
    engine = create_engine("sqlite:///iie.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    UniversityStats = Base.classes.UniversityStats  
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

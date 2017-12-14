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

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/univRanking")
#publish university world rankings
def univRanking():
    engine = create_engine("sqlite:///iie.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    rank = Base.classes.university_ranking

    rankResult = session.query(rank.world_rank, univ.university_name, rank.country, rank.international_students,
rank.year).all()

    e = defaultdict(list)
    for element in rankResult:
        e["rankings"].append({'world rank': str(element[0]), 'university': str(element[1]), 'country': element[2], '% international students': element[10], 'year': element[11]})
    return jsonify(e)

if __name__ == "__main__":
    app.run(debug=True)    

@app.route("/k12Scores")
#publish university world rankings
def univRanking():
    engine = create_engine("sqlite:///iie.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    k12 = Base.classes.k12_scores

    k12Result = session.query(k12.country, k12.subject, k12.sex, k12.year,k12.value).all()

    e = defaultdict(list)
    for element in k12Result:
        e["k12 Scores"].append({'country': str(element[0]), 'subject': str(element[1]), 'sex': element[2], 'year': element[5], 'value': element[6]})
    return jsonify(e)

if __name__ == "__main__":
    app.run(debug=True) 
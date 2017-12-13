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
#Base.metadata.create_all(conn)
session = Session(bind=engine)

#Base defination
aian = Base.classes.census_aian
asian = Base.classes.census_asian
black = Base.classes.census_black
hispanic = Base.classes.census_hispanic
mixed = Base.classes.census_mixed
other = Base.classes.census_other
whites = Base.classes.census_whites

# # ===========================Dataframe Creation==========================

# # the queries and create dataframe
# df_aian = pd.read_sql_query("select CountyID,CountyName,TotalPopulation,Year, Over149999, Over200000, 'AIAN' as Race from census_aian;", conn)
# df_aian["ID"]=df_aian["CountyID"]+df_aian["Year"]
# # df_aian=df_aian.rename(columns={'TotalPopulation': 'aian_population'})


# df_asian = pd.read_sql_query("select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Asian' as Race from census_asian;", conn)
# df_asian["ID"]=df_asian["CountyID"]+df_asian["Year"]
# # df_asian = df_asian.rename(columns={'TotalPopulation': 'asian_population'})

# df_black = pd.read_sql_query("select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Black' as Race from census_black;", conn)
# df_black["ID"]=df_black["CountyID"]+df_black["Year"]
# # df_black=df_black.rename(columns={'TotalPopulation': 'black_population'})

# df_hispanic = pd.read_sql_query("select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Hispanic' as Race from census_hispanic;", conn)
# df_hispanic["ID"]=df_hispanic["CountyID"]+df_hispanic["Year"]
# # df_hispanic=df_hispanic.rename(columns={'TotalPopulation': 'hispanic_population'})

# df_mixed = pd.read_sql_query("select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Mixed' as Race from census_mixed;", conn)
# df_mixed["ID"]=df_mixed["CountyID"]+df_mixed["Year"]
# # df_mixed=df_mixed.rename(columns={'TotalPopulation': 'mixed_population'})

# df_other = pd.read_sql_query("select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Other' as Race from census_other;", conn)
# df_other["ID"]=df_other["CountyID"]+df_other["Year"]
# # df_other=df_other.rename(columns={'TotalPopulation': 'other_population'})

# df_whites = pd.read_sql_query("select CountyID,CountyName,TotalPopulation,Year, Over150000, Over200000, 'Whites' as Race from census_whites;", conn)
# df_whites["ID"]=df_whites["CountyID"]+df_whites["Year"]
# # df_whites=df_whites.rename(columns={'TotalPopulation': 'whites_population'})

# # Merge the dataframe
# result=pd.merge((pd.merge((pd.merge((pd.merge((pd.merge(pd.merge(df_whites,df_other,on='ID', how='outer'),df_mixed,on='ID', how='outer')),df_hispanic,on='ID', how='outer')),df_black,on='ID', how='outer')),df_asian,on='ID', how='outer')),df_aian,on='ID', how='outer')
# merged_data=result.drop(['CountyID_y','CountyName_y','Year_y','CountyID_x','CountyName_x','Year_x'], axis=1)
# merged_data = merged_data.fillna(0)
# merged_data=merged_data.drop_duplicates()
# merged_new=merged_data[merged_data.Year != 0]

# #create new percentage dataframe

# merged_new['Total']=merged_new['other_population']+merged_new['mixed_population']+merged_new['hispanic_population']+merged_new['black_population'] + merged_new['asian_population']+merged_new['aian_population']+merged_new['whites_population']
# merged_new['%white']=(merged_new['whites_population']/merged_new['Total'])*100
# merged_new['%black']=(merged_new['black_population']/merged_new['Total'])*100
# merged_new['%mixed']=(merged_new['mixed_population']/merged_new['Total'])*100
# merged_new['%others']=(merged_new['other_population']/merged_new['Total'])*100
# merged_new['%asian']=(merged_new['asian_population']/merged_new['Total'])*100
# merged_new['%aian']=(merged_new['aian_population']/merged_new['Total'])*100
# merged_new['%hispanic']=(merged_new['hispanic_population']/merged_new['Total'])*100
# # merged_new=merged_new.drop(['Total','other_population','mixed_population','hispanic_population','black_population','asian_population','aian_population','whites_population'], axis=1)
# merged_new=merged_new.round(2)

# #========================================================================================================
# # the queries for high income over 200000
# df_aian_high = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_aian;", conn)
# df_aian_high["ID"]=df_aian_high["CountyID"]+df_aian_high["Year"]
# df_aian_high=df_aian_high.rename(columns={'Over200000': 'aian_high'})

# df_asian_high = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_asian;", conn)
# df_asian_high["ID"]=df_asian_high["CountyID"]+df_asian_high["Year"]
# df_asian_high = df_asian_high.rename(columns={'Over200000': 'asian_high'})

# df_black_high = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_black;", conn)
# df_black_high["ID"]=df_black_high["CountyID"]+df_black_high["Year"]
# df_black_high=df_black_high.rename(columns={'Over200000': 'black_high'})

# df_hispanic_high = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_hispanic;", conn)
# df_hispanic_high["ID"]=df_hispanic_high["CountyID"]+df_hispanic_high["Year"]
# df_hispanic_high=df_hispanic_high.rename(columns={'Over200000': 'hispanic_high'})

# df_mixed_high = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_mixed;", conn)
# df_mixed_high["ID"]=df_mixed_high["CountyID"]+df_mixed_high["Year"]
# df_mixed_high=df_mixed_high.rename(columns={'Over200000': 'mixed_high'})

# df_other_high = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_other;", conn)
# df_other_high["ID"]=df_other_high["CountyID"]+df_other_high["Year"]
# df_other_high=df_other_high.rename(columns={'Over200000': 'other_high'})

# df_whites_high = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_whites;", conn)
# df_whites_high["ID"]=df_whites_high["CountyID"]+df_whites_high["Year"]
# df_whites_high=df_whites_high.rename(columns={'Over200000': 'whites_high'})

# #Merge the dataframe
# result_high=pd.merge((pd.merge((pd.merge((pd.merge((pd.merge(pd.merge(df_whites_high,df_other_high,on='ID', how='outer'),df_mixed_high,on='ID', how='outer')),df_hispanic_high,on='ID', how='outer')),df_black_high,on='ID', how='outer')),df_asian_high,on='ID', how='outer')),df_aian_high,on='ID', how='outer')

# merge_data_high=result_high.drop(['CountyID_y','CountyName_y','Year_y','CountyID_x','CountyName_x','Year_x'], axis=1)

# #Create the highincome dataframe
# merge_data_high = merge_data_high.fillna(0)
# merge_data_high=merge_data_high.drop_duplicates()
# high_income=merge_data_high[merge_data_high.Year != 0]

# #========================================================================================================
# # the queries for low income over 150000
# df_aian_low = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_aian;", conn)
# df_aian_low["ID"]=df_aian_low["CountyID"]+df_aian_low["Year"]
# df_aian_low=df_aian_low.rename(columns={'Over200000': 'aian_low'})

# df_asian_low = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_asian;", conn)
# df_asian_low["ID"]=df_asian_low["CountyID"]+df_asian_low["Year"]
# df_asian_low = df_asian_low.rename(columns={'Over200000': 'asian_low'})

# df_black_low = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_black;", conn)
# df_black_low["ID"]=df_black_low["CountyID"]+df_black_low["Year"]
# df_black_low=df_black_low.rename(columns={'Over200000': 'black_low'})

# df_hispanic_low = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_hispanic;", conn)
# df_hispanic_low["ID"]=df_hispanic_low["CountyID"]+df_hispanic_low["Year"]
# df_hispanic_low=df_hispanic_low.rename(columns={'Over200000': 'hispanic_low'})

# df_mixed_low = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_mixed;", conn)
# df_mixed_low["ID"]=df_mixed_low["CountyID"]+df_mixed_low["Year"]
# df_mixed_low=df_mixed_low.rename(columns={'Over200000': 'mixed_low'})

# df_other_low = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_other;", conn)
# df_other_low["ID"]=df_other_low["CountyID"]+df_other_low["Year"]
# df_other_low=df_other_low.rename(columns={'Over200000': 'other_low'})

# df_whites_low = pd.read_sql_query("select CountyID,CountyName,Over200000,Year from census_whites;", conn)
# df_whites_low["ID"]=df_whites_low["CountyID"]+df_whites_low["Year"]
# df_whites_low=df_whites_low.rename(columns={'Over200000': 'whites_low'})

# #Merge the dataframe
# result_low=pd.merge((pd.merge((pd.merge((pd.merge((pd.merge(pd.merge(df_whites_low,df_other_low,on='ID', how='outer'),df_mixed_low,on='ID', how='outer')),df_hispanic_low,on='ID', how='outer')),df_black_low,on='ID', how='outer')),df_asian_low,on='ID', how='outer')),df_aian_low,on='ID', how='outer')

# merge_data_low=result_low.drop(['CountyID_y','CountyName_y','Year_y','CountyID_x','CountyName_x','Year_x'], axis=1)

# #Create the lowincome dataframe
# merge_data_low = merge_data_low.fillna(0)
# merge_data_low=merge_data_low.drop_duplicates()
# low_income=merge_data_low[merge_data_low.Year != 0]


query = "select CountyID,CountyName,TotalPopulation,Year, Over149999, Over200000, 'AIAN' as Race from census_aian union "
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
#publish the internation student placement
def univCounty():
    engine = create_engine("sqlite:///iie.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    univ = Base.classes.university_county

    univResult = session.query(univ.PlaceofDestination, univ.City, univ.State, univ.Students, univ.Year, univ.County).all()

    print(univResult)


    e = defaultdict(list)
    for element in univResult:
        e["universities"].append({'university': str(element[0]), 'city': element[1], 'state': element[2], 'students': element[3], 'year': element[4], 'county':element[5]})
    return jsonify(e)


if __name__ == "__main__":
    app.run(debug=True)

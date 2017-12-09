from flask import Flask, jsonify, render_template
import json
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc, extract, select
from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR
from sqlalchemy.types import NVARCHAR,BIGINT
from flask import Flask, jsonify
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, Table
# from dateutil.relativedelta import relativedelta
#################################################
# Flask Setup
#################################################

#################################################
# Flask Routes
#################################################
# engine = create_engine("sqlite:///AIAN5F.sqlite", echo=False)
# Base = automap_base()
# Base.prepare(engine, reflect=True)


# session = Session(engine)        
# aian = Base.classes.Data
# Base = automap_base(metadata=metadata)
app = Flask(__name__)

files =["2000_AIAN_cleaned.csv",
        "2005_AIAN_cleaned.csv",
        "2008_AIAN_cleaned.csv",
        "2010_AIAN_cleaned.csv",
        "2013_AIAN_cleaned.csv",
        "2016_AIAN_cleaned.csv"]
fileDFList = []
for file in files:
    # Import the census data into a pandas DataFrame-
    file_df = pd.read_csv(file)
    fileDFList.append(file_df)
totlalDF = pd.concat(fileDFList,ignore_index=True)
totlalDF.columns=totlalDF.columns.str.replace('$','I_')
totlalDF.columns=totlalDF.columns.str.replace(',','')
totlalDF.columns=totlalDF.columns.str.replace(' ','_')
#totlalDF.insert(0, 'Id', range(1, len(totlalDF)+1))
#totlalDF.set_index("Id",inplace=True)

Base = automap_base()
engine = create_engine('sqlite:///MyAIAN.sqlite')
totlalDF.to_sql(con=engine, name="AIAN_Data",index=True, if_exists='replace')

metadata = MetaData()
metadata.reflect(engine)
mytable = Table('AIAN_Data', metadata, Column('index',Integer, primary_key=True),
                Column('CountyName', String),
                Column('Race', String),
                autoload=True, extend_existing=True, autoload_with=engine,)

Base = automap_base(metadata=metadata)
Base.prepare()
aian = Base.classes.AIAN_Data
#session = Session(engine)
a=Base.classes.keys()
print(a)
aian = Base.classes.AIAN_Data
print(aian)
aian = Base.classes.AIAN_Data
session = Session(engine)

# a=session.query(Base.classes.Data.Over150000).all()
# print(a)
aian = Base.classes.AIAN_Data
session = Session(engine)
rows=session.query(aian.CountyName,aian.Race,aian.Year,aian.Over150000, aian.TotalPopulation).order_by(aian.CountyName,aian.Race).all()

aian = Base.classes.AIAN_Data
session = Session(engine)
rows = session.query(aian.CountyName,aian.Race,aian.Year,aian.Over150000, aian.I_200000_or_more,aian.TotalPopulation).order_by(aian.CountyName,aian.Race).all()

prevRaceName =""
d_census ={}
for i in range(len(rows)):
    row = rows[i]
    prevRow =rows[i-1]
    
     #check current county with prev county
    if(row[0] !=prevRow[0]): 
         # if(i!=0) 
         #      d_census.push({prevRow[0]= d_county})
        d_county ={}

    #check current county with prev county or current race with prev race
    if(row[0] !=prevRow[0] or row[1] !=prevRow[1]): 
        # Add previous object to Array
        # if(i!=0) 
        #      d_county.push({prevRow[0]= d_race})
        #Initialize new object
        d_race ={}
    
    #check current county with prev county or current race with prev race or current year with prev year
    if(row[0] !=prevRow[0] or row[1] !=prevRow[1] or row[1] !=prevRow[1]): 
        d_Over15000 = {}
        d_Over20000 = {}
        d_highincome ={}
        d_population ={}
        for x in [2000,2005,2008,2010,2013,2016]:
                d_Over15000[x] =0
                d_Over20000[x] =0
                d_highincome[x] =0
                d_population[x] =0
        
    d_Over15000[row[2]]= row[3]
    d_Over20000[row[2]]= row[4]
    d_highincome[row[2]]= row[3]+row[4]
    d_population[row[2]]=row[5]
    
    d_race["Over150000"]= d_Over15000
    d_race["Over200000"]= d_Over20000
    d_race["HighIncome"]= d_highincome
    d_race["TotalPopulation"] =d_population
        
    d_county[row[1]] =d_race
    d_census[row[0]]= d_county

#d_county.push({prevRow[0]= d_race})
#d_census.push({prevRow[0]= d_county})

#d_census
print(d_census)        



@app.route("/aian")
def mysamples():
    return jsonify(d_census) 

       
if __name__ == "__main__":
    app.run(debug=True)
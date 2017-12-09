from flask import Flask, jsonify, render_template
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc, extract, select
# from dateutil.relativedelta import relativedelta
        

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

engine = create_engine("sqlite:///censusdata.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)

session = Session(engine)


aian = Base.classes.census_aian
asian = Base.classes.census_asian

totalDict = {}
# aianTotals = session.query(aian.CountyName, aian.TotalPopulation, aian['$150000to$199999'], aian['$200000ormore'],aian.Year, aian.Race).all()
aianTotals = session.query(aian.CountyName, aian.TotalPopulation,aian.Year, aian.Race).all()
# asianTotals = session.query(asian.CountyName, asian.TotalPopulation, asian.Year, asian.Race).all()

print(aianTotals)

censusDict = {}
h2000_150 = 0
h2005_150 = 0
h2008_150 = 0
h2010_150 = 0
h2013_150 = 0
h2016_150 = 0

h2000_200 = 0
h2005_200 = 0
h2008_200 = 0
h2010_200 = 0
h2013_200 = 0
h2016_200 = 0

h2000_total = 0
h2005_total = 0
h2008_total = 0
h2010_total = 0
h2013_total = 0
h2016_total = 0

h2000_hi = 0
h2005_hi = 0
h2008_hi = 0
h2010_hi = 0
h2013_hi = 0
h2016_hi = 0

# [('Los Angeles County, California', 14517, '2000', 'AIAN'), ('Los Angeles County, California', 16970, '2005', 'AIAN'), ('Los Angeles County, California', 17773, '2008', 'AIAN'), ('Los Angeles County, California', 14517, '2010', 'AIAN'), ('Los Angeles County, California', 20090, '2013', 'AIAN'), ('Los Angeles County, California', 20578, '2016', 'AIAN')]

lastCounty = ""

for aianTotal in aianTotals:

    thisCounty = aianTotal[0]
    if thisCounty == lastCounty and lastCounty != "":

        if aianTotal[4] == '2000':
            h2000_150 =  aianTotal[2]
            h2000_200 =  aianTotal[3]
            h2000_total = aianTotal[1]
            h2000_hi = h2000_150 + h2000_200

        if aianTotal[4] == '2005':
            h2005_150 =  aianTotal[2]
            h2005_200 =  aianTotal[3]
            h2005_total = aianTotal[1]
            h2005_hi = h2005_150 + h2005_200

        if aianTotal[4] == '2008':
            h2008_150 =  aianTotal[2]
            h2008_200 =  aianTotal[3]
            h2008_total = aianTotal[1]
            h2008_hi = h2008_150 + h2008_200

        if aianTotal[4] == '2010':
            h2010_150 =  aianTotal[2]
            h2010_200 =  aianTotal[3]
            h2010_total = aianTotal[1]
            h2010_hi = h2010_150 + h2010_200

        if aianTotal[4] == '2013':
            h2013_150 =  aianTotal[2]
            h2013_200 =  aianTotal[3]
            h2013_total = aianTotal[1]
            h2013_hi = h2013_150 + h2013_200

        if aianTotal[4] == '2016':
            h2016_150 =  aianTotal[2]
            h2016_200 =  aianTotal[3]
            h2016_total = aianTotal[1]
            h2016_hi = h2016_150 + h2016_200

    else:
        # write to the county list
        aian150List = [h2000_150, h2005_150, h2008_150, h2010_150, h2013_150, h2016_150]
        aian200List = [h2000_200, h2005_200, h2008_200, h2010_200, h2013_200, h2016_200]
        aiantotalList = [h2000_total, h2005_total, h2008_total, h2010_total, h2013_total, h2016_total]
        aianhiList = [h2000_hi, h2005_hi, h2008_hi, h2010_hi, h2013_hi, h2016_hi]
        censusDict[lastCounty] = {"AIAN",[{"over150",aian150List},{"over200",aian200List},{"total",aianTotalList},{"hi",aianhiList}]}

    lastCounty = thisCounty

print(censusDict)



@app.route("/")
def welcome():
    """Return all census data"""
    # return render_template("index.html")
    return jsonify(censusDict)




@app.route("/totalPopulation/<countyID>")
def populations(countyID):
    print(countyID)
    engine = create_engine("sqlite:///censusdata.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    
    session = Session(engine)
    # raceList = [census_aian, census_asian, census_whites, census_black, census_hispanic, census_mixed, census_other]
    
    # x = census_aian

    # table = Base.classes.x
    # print(table)

    # aian = Base.classes.census_aian
    # , asian, whites, black, hispanic, mixed, other  = Base.classes.census_aian, Base.classes.census_asian, Base.classes.census_whites, Base.classes.census_black, Base.classes.census_hispanic, Base.classes.census_mixed, Base.classes.census_other

# u1 = User(addresses=[Address(email="foo@bar.com")])

    # a = aian(countyID=countyID)
    # a2 = session.query(aian.CountyName, aian.TotalPopulation, aian.Year, aian.Race).filter_by(CountyID=countyID).all()
    # print(a2)

    # for race in raceList:
    #     table = Base.classes.race
    #     print(table)
    #     totalDict = {}
    #     raceTotals = session.query(table.CountyName, table.TotalPopulation, table.Year, table.Race).filter_by(CountyID=countyID).all()
    #     popDict = {}

    #     for pops in raceTotals:
    #         popDict[pops[2]]=pops[1]

    #     totalDict[race] = popDict

    # return jsonify(totalDict)
    # return "test"
    
    

    aian = Base.classes.census_aian
    asian = Base.classes.census_asian

    totalDict = {}
    aianTotals = session.query(aian.CountyName, aian.TotalPopulation, aian.Year, aian.Race).filter_by(CountyID=countyID).all()
    asianTotals = session.query(asian.CountyName, asian.TotalPopulation, asian.Year, asian.Race).filter_by(CountyID=countyID).all()


    
    popDict = {}
    
    for aianTotal in aianTotals:
        popDict[aianTotal[2]]=aianTotal[1]

    print(popDict)
    totalDict["AIAN"] = popDict

    popDict = {}
    
    for asianTotal in asianTotals:
        popDict[asianTotal[2]]=asianTotal[1]

    print(popDict)
    totalDict["ASIAN"] = popDict


    return jsonify(totalDict)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, render_template
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc, extract, select, Table
from collections import defaultdict
# from dateutil.relativedelta import relativedelta
        

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

# this will hold all the data in the form we want
censusDict = {}

# a function to reset all the bucket values in case there is no data, the value will be 0
def resetVars():
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


# a function that takes the results from each table and adds them to the object to be returned
def dataToObject(raceTotals,raceGroup):
    lastCounty = ""
    global h2000_150
    global h2005_150
    global h2008_150
    global h2010_150
    global h2013_150
    global h2016_150

    global h2000_200
    global h2005_200
    global h2008_200
    global h2010_200
    global h2013_200
    global h2016_200

    global h2000_total
    global h2005_total
    global h2008_total
    global h2010_total
    global h2013_total
    global h2016_total

    global h2000_hi
    global h2005_hi
    global h2008_hi
    global h2010_hi
    global h2013_hi
    global h2016_hi

    resetVars()
    for aianTotal in raceTotals:

        thisCounty = aianTotal[0]

        if thisCounty != lastCounty and lastCounty != "":
            # print("new county - create the object for the previous county")
            # write to the county list
            aian150List = [h2000_150, h2005_150, h2008_150, h2010_150, h2013_150, h2016_150]
            aian200List = [h2000_200, h2005_200, h2008_200, h2010_200, h2013_200, h2016_200]
            aiantotalList = [h2000_total, h2005_total, h2008_total, h2010_total, h2013_total, h2016_total]
            aianhiList = [h2000_hi, h2005_hi, h2008_hi, h2010_hi, h2013_hi, h2016_hi]
            if lastCounty in censusDict:
                censusDict[lastCounty].append([{raceGroup:[{"over150":aian150List},{"over200":aian200List},{"total":aiantotalList},{"hi":aianhiList}]}])
            else:
                censusDict[lastCounty] = [{raceGroup:[{"over150":aian150List},{"over200":aian200List},{"total":aiantotalList},{"hi":aianhiList}]}]
            
            
            resetVars()

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

        lastCounty = thisCounty

    # when done looping through, add the last county to the object
    aian150List = [h2000_150, h2005_150, h2008_150, h2010_150, h2013_150, h2016_150]
    aian200List = [h2000_200, h2005_200, h2008_200, h2010_200, h2013_200, h2016_200]
    aiantotalList = [h2000_total, h2005_total, h2008_total, h2010_total, h2013_total, h2016_total]
    aianhiList = [h2000_hi, h2005_hi, h2008_hi, h2010_hi, h2013_hi, h2016_hi]

    if lastCounty in censusDict:
        censusDict[lastCounty].append({raceGroup:[{"over150":aian150List},{"over200":aian200List},{"total":aiantotalList},{"hi":aianhiList}]})
    else:
        censusDict[lastCounty] = [{raceGroup:[{"over150":aian150List},{"over200":aian200List},{"total":aiantotalList},{"hi":aianhiList}]}]


# dataToObject(aianTotals,"AIAN")
# dataToObject(blackTotals,"BLACK")
# dataToObject(asianTotals,"ASIAN")
# dataToObject(hispanicTotals,"HISPANIC")
# dataToObject(mixedTotals,"MIXED")
# dataToObject(otherTotals,"OTHER")
# dataToObject(whitesTotals,"WHITES")

# print(censusDict)


@app.route("/")
def welcome():
    """The home page"""
    return render_template("index.html")


@app.route("/test")
def test():
    """Return all census data"""
    # return render_template("index.html")
    # return "test"
    return jsonify(censusDict)

@app.route("/test2/<countyName>")
def countySelect(countyName):

    engine = create_engine("sqlite:///censusdata.sqlite", echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    aian = Base.classes.census_aian
    asian = Base.classes.census_asian
    black = Base.classes.census_black
    hispanic = Base.classes.census_hispanic
    mixed = Base.classes.census_mixed
    other = Base.classes.census_other
    whites = Base.classes.census_whites

    # the queries
    aianTotals = session.query(aian.CountyName, aian.TotalPopulation, aian.Over149999, aian.Over200000,aian.Year, aian.Race).filter_by(CountyName=countyName).order_by(aian.CountyName).all()
    asianTotals = session.query(asian.CountyName, asian.TotalPopulation, asian.Over150000, asian.Over200000,asian.Year, asian.Race).filter_by(CountyName=countyName).filter_by(Race='Asian').order_by(asian.CountyName).all()
    blackTotals = session.query(black.CountyName, black.TotalPopulation, black.Over150000, black.Over200000,black.Year, black.Race).filter_by(CountyName=countyName).order_by(black.CountyName).all()
    hispanicTotals = session.query(hispanic.CountyName, hispanic.TotalPopulation, hispanic.Over150000, hispanic.Over200000,hispanic.Year, hispanic.Race).filter_by(CountyName=countyName).order_by(hispanic.CountyName).all()
    mixedTotals = session.query(mixed.CountyName, mixed.TotalPopulation, mixed.Over150000, mixed.Over200000,mixed.Year, mixed.Race).filter_by(CountyName=countyName).order_by(mixed.CountyName).all()
    otherTotals = session.query(other.CountyName, other.TotalPopulation, other.Over150000, other.Over200000,other.Year, other.Race).filter_by(CountyName=countyName).order_by(other.CountyName).all()
    whitesTotals = session.query(whites.CountyName, whites.TotalPopulation, whites.Over150000, whites.Over200000,whites.Year, whites.Race).filter_by(CountyName=countyName).order_by(whites.CountyName).all()


    # clear out the object so we don't keep adding to it everytime we refresh
    censusDict.clear()

    dataToObject(aianTotals,"AIAN")
    dataToObject(blackTotals,"BLACK")
    dataToObject(asianTotals,"ASIAN")
    dataToObject(hispanicTotals,"HISPANIC")
    dataToObject(mixedTotals,"MIXED")
    dataToObject(otherTotals,"OTHER")
    dataToObject(whitesTotals,"WHITES")

    return jsonify(censusDict)
    # return "test"

@app.route("/origin")
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
def univCounty():
    print("yes")
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

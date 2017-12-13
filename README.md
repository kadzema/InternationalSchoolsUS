# InternationalSchoolsUS

## goals
- change in race composition
- change in income level by race

## races
- Asian
- Black
- Hispanic
- mixed (2 or more)
- white
	- alaska native alaskan
	- american indian
	- native hawaiian and pacific islander
- some other race

## years
2000
2005
2008
2010
2013
2016

## to do 
- census data availability - craig
- clean data (csvs)
- apis
- build db (sqlite)
- html/viz/js/d3
- deploy
- presentation
- select top 10 counties (use tablaeu 2016 visualization to decide)


## visualization options
- map which plots selected top 10 counties?
- click on a county and show visualization (increase in percentage of minority population in high income bracket)
- scroll through county text to load different visualization  (https://www.bloomberg.com/graphics/2015-auto-sales/)
- digital whiteboard (https://www.bloomberg.com/graphics/2015-nfl-super-bowl-salary/)
- bubble size relates to population ratio (over $200k)
- bubble color represents race
- determine counties
- list of international schools k-12 baccalaureate
- cpi-w (to plot against inflation)

select year, county id, population race where income > 150k, total population of that race (all incomes)

2000  1   1900000,    Asian, 	2000000000
2000  1    900000,    White,	5000000
2000  1    900000,    Black,	3000000
2000  1    100000,    Hispanic,	40000
2000  1     10000,    Other,	55555

get the ratio of population instead of count

year, county id, population, race, ratio of population

2000  1   1900000,    Asian,   .50
2000  1    900000,    White    .35
2000  1    900000,    Black    .35
2000  1    100000,    Hispanic .1
2000  1     10000,    Other    .05

2005  1   1900000,    Asian,   .50
2005  1    900000,    White    .35
2005  1    900000,    Black    .35
2005  1    100000,    Hispanic .1
2005  1     10000,    Other    .05







// Step 0: Set up our chart
//= ================================
var svgWidth = 960;
var svgHeight = 400;

var margin = { top: 20, right: 40, bottom: 80, left: 100 };

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

var colors = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d']

var circleRadius = 5;
var opacityPercentage = .8;
// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3
.select(".totalpopulation")
.append("svg")
.attr("width", svgWidth)
.attr("height", svgHeight)
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var hisvg = d3
.select(".hipopulation")
.append("svg")
.attr("width", svgWidth)
.attr("height", svgHeight)
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");


// do this inside the csv call so we can utilize the data to dynamically create one for each race?
var aian = svg.append("g");
var asian = svg.append("g");
// var total = svg.append("g");
var black = svg.append("g");
var hispanic = svg.append("g");
var mixed = svg.append("g");
var other = svg.append("g");
var whites = svg.append("g")

//this will be selected from dropdown
var countyName = "Los Angeles County, California"

d3.json("../test2/"+countyName, function(err,data){
  if (err) throw err;

   console.log(data);

   xList = ['2000','2005', '2008', '2010', '2013', '2016']


  //  don't think we should have to be using indexes!
  // perhaps API should only return one list per race (like total or high income...)
   aianData = data[countyName][0]["AIAN"][2]["total"]
   blackData = data[countyName][1]["BLACK"][2]["total"]
   asianData = data[countyName][2]["ASIAN"][2]["total"]
   hispanicData = data[countyName][3]["HISPANIC"][2]["total"]
   mixedData = data[countyName][4]["MIXED"][2]["total"]
   otherData = data[countyName][5]["OTHER"][2]["total"]
   whitesData = data[countyName][6]["WHITES"][2]["total"]

   aianHIData = data[countyName][0]["AIAN"][3]["hi"]
   blackHIData = data[countyName][1]["BLACK"][3]["hi"]
   asianHIData = data[countyName][2]["ASIAN"][3]["hi"]
   hispanicHIData = data[countyName][3]["HISPANIC"][3]["hi"]
   mixedHIData = data[countyName][4]["MIXED"][3]["hi"]
   otherHIData = data[countyName][5]["OTHER"][3]["hi"]
   whitesHIData = data[countyName][6]["WHITES"][3]["hi"]

  testThing = data[countyName]

  console.log("kxatest: ",testThing)
  for(i=0;i<testThing.length;i++){
    console.log("looping",testThing[i])
    // each one is a race

  }

   console.log("aianData",aianData)
   console.log("blackData", blackData)
   console.log("asianData",asianData)
   console.log("hispanicData",hispanicData)
   console.log("mixedData",mixedData)
   console.log("otherData",otherData)
   console.log("whitesData",whitesData)

    // Create scale functions
    var yLinearScale = d3.scaleLinear().range([height, 0]);
  
    var xLinearScale = d3.scaleLinear().range([0, width]);
  
    // Create axis functions
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);
  
    // These variables store the minimum and maximum values in a column in data.csv
    var xMin;
    var xMax;
    var yMin;
    var yMax;

    allData = aianData.concat(blackData).concat(asianData).concat(hispanicData).concat(mixedData).concat(otherData).concat(whitesData)
    console.log("allData",allData);
    yMin = d3.min(allData) * .8;
    yMax = d3.max(allData);
    console.log("yMin",yMin)
    console.log("yMax",yMax)
    // This function identifies the minimum and maximum values for all of the data for the Y Axis
    // and assign them to yMin and yMax variables, which will define the axis domain
    // it will need to be run for all races
    // function findMinAndMax() {
    //   yMin = d3.min(data, function(data) {
    //     // return data[dataColumnY].filter(function(d){return d.income_bucket == "$10,000 to $14,999";}) //this will be total
    //     // return +data[dataColumnY] * .8; //make it a little less so the first data point is not at the bottom
    //     return (data.AsianOver200 < data.BlackOver200) ? (data.AsianOver200 * .8) : (data.BlackOver200 * .8);
    //   });
  
    //   yMax = d3.max(morePlayData, function(data) {
    //     // return +data[dataColumnY] * 1.1;  // make it a little more so the last data point is not at the top
    //     return (data.AsianOver200 < data.BlackOver200) ? (data.BlackOver200 * 1.1) : (data.AsianOver200 * 1.1);
    //   });
    // }
  
    // The default x-axis is 'year'
    // Another axis can be assigned to the variable during an onclick event.
    // This variable is key to the ability to change axis/data column
    var currentAxisLabelX = "Year";
    var currentAxisLabelY = "Total";
  
    // Call findMinAndMax() with 'year' as default
    // findMinAndMax(); //if these calls weren't wrapped in a function, would we run the risk of not having values?
    // the function is not returning anything - it's only making calls
  
    // Set the domain of an axis to extend from the min to the max value of the data column
    // let's hard code min and max x values to match years
    xMin = 1999;
    xMax = 2017;
    // yMax = 30000;
    // yMin = 10000;
    xLinearScale.domain([xMin, xMax]);

    // how to get the yMin and yMax?
    // combine all list and get max and min?

    yLinearScale.domain([yMin, yMax]);
    // console.log("max y", yMax);
  
    console.log("kxatest: ",testThing)
    for(i=0;i<testThing.length;i++){
      console.log(testThing[i])
      // each one is a race
      var value = Object.keys(testThing[i])
      console.log("race?",value)
       
      // figure out how to do this dynamically
      
    }

    console.log("kxa keys",Object.keys(testThing))


    // try this later
    // Initialize tooltip
    var toolTip = d3
      .tip()
      .attr("class", "tooltip")
      // Define position
      .offset([80, -60])
      // The html() method allows us to mix JavaScript with HTML in the callback function
      .html(function(data) {   //how does this know it is looking at the csv data?
        // var race = data.race; //don't have this in this file
        
        // var numHits = +data.num_hits;
        // var population = +data[currentAxisLabelY];
        var population = data;
        // var bandString;
        // // Tooltip text depends on which axis is active/has been clicked
        // if (currentAxisLabelX === "hair_length") {
        //   bandString = "Hair length: ";
        // }
        // else {
        //   bandString = "Number of albums: ";
        // }
        return "Population: " + population + "<br>Race: " + Object.keys(data);
        // return bandName +
        //   "<br>" +
        //   bandString +
        //   bandInfo +
        //   "<br> Population: " +
        //   population;
      });
  
    // Create tooltip
    svg.call(toolTip);
  
    // // make circles for the race population but all in the lower left corner
    aian
      .selectAll("circle")
      .data(aianData)
      .enter()
      .append("circle")
      .attr("cx", function(data, index) {
        // return xLinearScale(index+2000);
        return 0;
      })
      .attr("cy", function(data, index) {
        // return yLinearScale(data);
        return 300;
      })
      .attr("r", circleRadius)
      // .attr("r",function(data,index){
      //   // return data/1000;
      //   return 10;
      // })
      // .attr("fill", "#E75480")
      .attr("fill",colors[0])
      .attr("opacity",opacityPercentage)
      // display tooltip on click
      .on("click", function(data) {
        toolTip.show(data);
      })
      // display tooltip on click
      .on("mouseon", function(data) {
        toolTip.show(data);
      })
      // hide tooltip on mouseout
      .on("mouseout", function(data, index) {
        toolTip.hide(data);
      });

      // now animate the circles
      aian
      .selectAll("circle")
      .transition()
      .duration(1000)
      .attr("cx", function(data, index) {
        // return index * svgWidth / 20;
        // return xLinearScale(+data[currentAxisLabelX]);
        return xLinearScale(xList[index]);
      })
      // .attr("cx", 2005)
      .attr("cy", function(data, index) {
        // return 600 - data * svgHeight / 80;
        // return data;
        return yLinearScale(data);
      });


         // // make circles for the race population but all in the lower left corner
    black
    .selectAll("circle")
    .data(blackData)
    .enter()
    .append("circle")
    .attr("cx", function(data, index) {
      // return xLinearScale(+data[currentAxisLabelX]);
      return 0;
    })
    .attr("cy", function(data, index) {
      // return yLinearScale(data.AsianOver200);
      return 300;
    })
    .attr("r", circleRadius)
    // .attr("r",function(data,index){
    //   // return data/10000;
    //   return 10;
    // })
    // .attr("fill", "#000000")
    .attr("fill",colors[1])
    .attr("opacity",opacityPercentage)
    // display tooltip on click
    .on("click", function(data) {
      toolTip.show(data);
    })
    // hide tooltip on mouseout
    .on("mouseout", function(data, index) {
      toolTip.hide(data);
    });

    // now animate the circles
    black
    .selectAll("circle")
    .transition()
    .duration(1000)
    .attr("cx", function(data, index) {
      // return index * svgWidth / 20;
      return xLinearScale(+xList[index]);
    })
    .attr("cy", function(data, index) {
      // return 600 - data * svgHeight / 80;
      return yLinearScale(data);
    }); 


    asian
    .selectAll("circle")
    .data(asianData)
    .enter()
    .append("circle")
    .attr("cx", function(data, index) {
      return 0;
    })
    .attr("cy", function(data, index) {
      return 300;
    })
    .attr("r", circleRadius)
    // .attr("r",function(data,index){
    //   return 10;
    // })
    // .attr("fill", "#00FF00")
    .attr("fill", colors[2])
    .attr("opacity",opacityPercentage)
    // display tooltip on click
    .on("click", function(data) {
      toolTip.show(data);
    })
    // hide tooltip on mouseout
    .on("mouseout", function(data, index) {
      toolTip.hide(data);
    });

    // now animate the circles
    asian
    .selectAll("circle")
    .transition()
    .duration(1000)
    .attr("cx", function(data, index) {
      return xLinearScale(+xList[index]);
    })
    .attr("cy", function(data, index) {
      return yLinearScale(data);
    });

    hispanic
    .selectAll("circle")
    .data(hispanicData)
    .enter()
    .append("circle")
    .attr("cx", function(data, index) {
      return 0;
    })
    .attr("cy", function(data, index) {
      return 300;
    })
    .attr("r", circleRadius)
    // .attr("r",function(data,index){
    //   return 10;
    // })
    // .attr("fill", "#0000FF")
    .attr("fill", colors[3])
    .attr("opacity",opacityPercentage)
    // display tooltip on click
    .on("click", function(data) {
      toolTip.show(data);
    })
    // hide tooltip on mouseout
    .on("mouseout", function(data, index) {
      toolTip.hide(data);
    });

    // now animate the circles
    hispanic
    .selectAll("circle")
    .transition()
    .duration(1000)
    .attr("cx", function(data, index) {
      return xLinearScale(+xList[index]);
    })
    .attr("cy", function(data, index) {
      return yLinearScale(data);
    });

    mixed
    .selectAll("circle")
    .data(mixedData)
    .enter()
    .append("circle")
    .attr("cx", function(data, index) {
      return 0;
    })
    .attr("cy", function(data, index) {
      return 300;
    })
    .attr("r", circleRadius)
    // .attr("r",function(data,index){
    //   return 10;
    // })
    // .attr("fill", "#FF7700")
    .attr("fill",colors[4])
    .attr("opacity",opacityPercentage)
    // display tooltip on click
    .on("click", function(data) {
      toolTip.show(data);
    })
    // hide tooltip on mouseout
    .on("mouseout", function(data, index) {
      toolTip.hide(data);
    });

    // now animate the circles
    mixed
    .selectAll("circle")
    .transition()
    .duration(1000)
    .attr("cx", function(data, index) {
      return xLinearScale(+xList[index]);
    })
    .attr("cy", function(data, index) {
      return yLinearScale(data);
    });

  
    other
    .selectAll("circle")
    .data(otherData)
    .enter()
    .append("circle")
    .attr("cx", function(data, index) {
      return 0;
    })
    .attr("cy", function(data, index) {
      return 300;
    })
    .attr("r", circleRadius)
    // .attr("r",function(data,index){
    //   return 10;
    // })
    // .attr("fill", "#0077FF")
    .attr("fill", colors[5])
    .attr("opacity",opacityPercentage)
    // display tooltip on click
    .on("click", function(data) {
      toolTip.show(data);
    })
    // hide tooltip on mouseout
    .on("mouseout", function(data, index) {
      toolTip.hide(data);
    });

    // now animate the circles
    other
    .selectAll("circle")
    .transition()
    .duration(1000)
    .attr("cx", function(data, index) {
      return xLinearScale(+xList[index]);
    })
    .attr("cy", function(data, index) {
      return yLinearScale(data);
    });

    whites
    .selectAll("circle")
    .data(whitesData)
    .enter()
    .append("circle")
    .attr("cx", function(data, index) {
      return 0;
    })
    .attr("cy", function(data, index) {
      return 300;
    })
    .attr("r", circleRadius)
    // .attr("r",function(data,index){
    //   return 10;
    // })
    // .attr("fill", "#0077FF")
    .attr("fill", colors[6])
    .attr("opacity",opacityPercentage)
    // display tooltip on click
    .on("click", function(data) {
      toolTip.show(data);
    })
    // hide tooltip on mouseout
    .on("mouseout", function(data, index) {
      toolTip.hide(data);
    });

    // now animate the circles
    whites
    .selectAll("circle")
    .transition()
    .duration(1000)
    .attr("cx", function(data, index) {
      return xLinearScale(+xList[index]);
    })
    .attr("cy", function(data, index) {
      return yLinearScale(data);
    });



  
    // Append an SVG group for the x-axis, then display the x-axis
    aian
      .append("g")
      .attr("transform", "translate(0," + height + ")")
      // The class name assigned here will be used for transition effects
      .attr("class", "x-axis")
      .call(bottomAxis);
  
    // Append a group for y-axis, then display it
    aian.append("g").call(leftAxis);
  
    // Append y-axis label
    aian
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 40)
      .attr("x", 0 - height / 2)
      .attr("dy", "1em")
      .attr("class", "axis-text")
      .attr("data-axis-name", "population")
      .text("Population");
  
    // Append x-axis labels
    aian
      .append("text")
      .attr(
        "transform",
        "translate(" + width / 2 + " ," + (height + margin.top + 20) + ")"
      )
      // This axis label is active by default
      .attr("class", "axis-text active")
      .attr("data-axis-name", "year")
      .text("Year");

});

// the origins chart-----------------------------------------------------------------------------------------------
var originSvg = dimple.newSvg(".originChart", 690, 400);
d3.json("/origin", function (data) {
  // Latest period only
  // var filteredData = dimple.filterData(data, "Date", "01/12/2012");

  console.log("data",data.origins[0]);


  // Create the chart
  var myChart = new dimple.chart(originSvg, data.origins);
  myChart.setBounds(60, 30, 510, 330)

  // Create a standard bubble of studentCount by year
  // We are coloring by Origin as that will be the key in the legend
  x = myChart.addTimeAxis("x", "year", "%Y", "%Y");
  y = myChart.addMeasureAxis("y", "studentcount");
  myChart.addSeries(["year","origin"], dimple.plot.bubble);
  // myChart.addSeries("origin", dimple.plot.line);
  var myLegend = myChart.addLegend(630, 45, 75, 300, "Right");
  myChart.draw();

  // This is a critical step.  By doing this we orphan the legend. This
  // means it will not respond to graph updates.  Without this the legend
  // will redraw when the chart refreshes removing the unchecked item and
  // also dropping the events we define below.
  myChart.legends = [];

  // This block simply adds the legend title. I put it into a d3 data
  // object to split it onto 2 lines.  This technique works with any
  // number of lines, it isn't dimple specific.
  originSvg.selectAll("title_text")
    .data(["Click legend to","show/hide origins:"])
    .enter()
    .append("text")
      .attr("x", 585)
      .attr("y", function (d, i) { return 40 + i * 14; })
      .style("font-family", "sans-serif")
      .style("font-size", "10px")
      .style("color", "Black")
      .text(function (d) { return d; });

  // Get a unique list of Owner values to use when filtering
  var filterValues = dimple.getUniqueValues(data.origins, "origin");
  // Get all the rectangles from our now orphaned legend
  myLegend.shapes.selectAll("rect")
    // Add a click event to each rectangle
    .on("click", function (e) {
      // This indicates whether the item is already visible or not
      var hide = false;
      var newFilters = [];
      // If the filters contain the clicked shape hide it
      filterValues.forEach(function (f) {
        if (f === e.aggField.slice(-1)[0]) {
          hide = true;
        } else {
          newFilters.push(f);
        }
      });
      // Hide the shape or show it
      if (hide) {
        d3.select(this).style("opacity", 0.2);
      } else {
        newFilters.push(e.aggField.slice(-1)[0]);
        d3.select(this).style("opacity", 0.8);
      }
      // Update the filters
      filterValues = newFilters;
      // Filter the data
      myChart.data = dimple.filterData(data.origins, "origin", filterValues);
      // Passing a duration parameter makes the chart animate. Without
      // it there is no transition
      myChart.draw(800);
    });
});

// the unviersity chart------------------------------------------------------------------------------------------------
var univSvg = dimple.newSvg(".universityCounty", 690, 400);
d3.json("/univCounty", function (data) {
  // Latest period only
  // var filteredData = dimple.filterData(data, "Date", "01/12/2012");

  console.log("data",data.universities[0]);


  // Create the chart
  var myChart = new dimple.chart(univSvg, data.universities);
  myChart.setBounds(60, 30, 510, 330)

  // Create a standard bubble of studentCount by year
  // We are coloring by county as that will be the key in the legend
  x = myChart.addTimeAxis("x", "year", "%Y", "%Y");
  y = myChart.addMeasureAxis("y", "students");
  myChart.addSeries(["year","university", "county"], dimple.plot.bubble);
  var myLegend = myChart.addLegend(620, 45, 155, 400, "Right");
  myChart.draw();

  // This is a critical step.  By doing this we orphan the legend. This
  // means it will not respond to graph updates.  Without this the legend
  // will redraw when the chart refreshes removing the unchecked item and
  // also dropping the events we define below.
  myChart.legends = [];

  // This block simply adds the legend title. I put it into a d3 data
  // object to split it onto 2 lines.  This technique works with any
  // number of lines, it isn't dimple specific.
  univSvg.selectAll("title_text")
    .data(["Click legend to","show/hide counties:"])
    .enter()
    .append("text")
      .attr("x", 585)
      .attr("y", function (d, i) { return 40 + i * 14; })
      .style("font-family", "sans-serif")
      .style("font-size", "10px")
      .style("color", "Black")
      .text(function (d) { return d; });

  // Get a unique list of Owner values to use when filtering
  var filterValues = dimple.getUniqueValues(data.universities, "county");
  // Get all the rectangles from our now orphaned legend
  myLegend.shapes.selectAll("rect")
    // Add a click event to each rectangle
    .on("click", function (e) {
      // This indicates whether the item is already visible or not
      var hide = false;
      var newFilters = [];
      // If the filters contain the clicked shape hide it
      filterValues.forEach(function (f) {
        if (f === e.aggField.slice(-1)[0]) {
          hide = true;
        } else {
          newFilters.push(f);
        }
      });
      // Hide the shape or show it
      if (hide) {
        d3.select(this).style("opacity", 0.2);
      } else {
        newFilters.push(e.aggField.slice(-1)[0]);
        d3.select(this).style("opacity", 0.8);
      }
      // Update the filters
      filterValues = newFilters;
      // Filter the data
      myChart.data = dimple.filterData(data.universities, "county", filterValues);
      // Passing a duration parameter makes the chart animate. Without
      // it there is no transition
      myChart.draw(800);
    });
});


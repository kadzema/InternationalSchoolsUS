// Step 0: Set up our chart
//= ================================
var svgWidth = 960;
var svgHeight = 400;

var margin = { top: 20, right: 40, bottom: 80, left: 100 };

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;


// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3
.select(".population")
.append("svg")
.attr("width", svgWidth)
.attr("height", svgHeight)
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");


// do this inside the csv call so we can utilize the data to dynamically create one for each race?
var asian = svg.append("g");
// // let's come back to this
var total = svg.append("g");
var black = svg.append("g")

//this will be selected from dropdown
var countyID = 6037

d3.json("/totalPopulation/"+countyID, function(err,data){
  if (err) throw err;
   console.log(data);
  
  // //this creates a list for all of the data points?
  //   data.forEach(function(data) {
  //     data.asian_population = +data.AsianOver200;
  //     data.total_population = +data.TotalOver200;
  //     data.black_population = +data.BlackOver200;
  //     // data.population = +data.Over200;
  //     // data.income_level = data.income_level;
  //   });

    // console.log("data.race_population",data.race_population);
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
  
    // This function identifies the minimum and maximum values for all of the data for the Y Axis
    // and assign them to yMin and yMax variables, which will define the axis domain
    // it will need to be run for all races
    function findMinAndMax() {
      yMin = d3.min(data, function(data) {
        // return data[dataColumnY].filter(function(d){return d.income_bucket == "$10,000 to $14,999";}) //this will be total
        // return +data[dataColumnY] * .8; //make it a little less so the first data point is not at the bottom
        return (data.AsianOver200 < data.BlackOver200) ? (data.AsianOver200 * .8) : (data.BlackOver200 * .8);
      });
  
      yMax = d3.max(morePlayData, function(data) {
        // return +data[dataColumnY] * 1.1;  // make it a little more so the last data point is not at the top
        return (data.AsianOver200 < data.BlackOver200) ? (data.BlackOver200 * 1.1) : (data.AsianOver200 * 1.1);
      });
    }
  
    // The default x-axis is 'year'
    // Another axis can be assigned to the variable during an onclick event.
    // This variable is key to the ability to change axis/data column
    var currentAxisLabelX = "Year";
    var currentAxisLabelY = "AsianOver200";
  
    // Call findMinAndMax() with 'year' as default
    findMinAndMax(); //if these calls weren't wrapped in a function, would we run the risk of not having values?
    // the function is not returning anything - it's only making calls
  
    // Set the domain of an axis to extend from the min to the max value of the data column
    // let's hard code min and max x values to match years
    xMin = 1999;
    xMax = 2017;
    // yMax = 30000;
    xLinearScale.domain([xMin, xMax]);
    yLinearScale.domain([yMin, yMax]);
    // console.log("max y", yMax);
  
    // try this later
    // Initialize tooltip
    var toolTip = d3
      .tip()
      .attr("class", "tooltip")
      // Define position
      .offset([80, -60])
      // The html() method allows us to mix JavaScript with HTML in the callback function
      .html(function(data) {   //how does this know it is looking at the csv data?
        var race = data.race; //don't have this in this file
        // var numHits = +data.num_hits;
        var population = +data[currentAxisLabelY];
        // var bandString;
        // // Tooltip text depends on which axis is active/has been clicked
        // if (currentAxisLabelX === "hair_length") {
        //   bandString = "Hair length: ";
        // }
        // else {
        //   bandString = "Number of albums: ";
        // }
        return "Population: " + population;
        // return bandName +
        //   "<br>" +
        //   bandString +
        //   bandInfo +
        //   "<br> Population: " +
        //   population;
      });
  
    // Create tooltip
    svg.call(toolTip);


    // total
    // .selectAll("circle")
    // .data(morePlayData)
    // .enter()
    // .append("circle")
    // .attr("cx", function(data, index) {
    //   return xLinearScale(+data[currentAxisLabelX]);
    // })
    // .attr("cy", function(data, index) {
    //   return yLinearScale(+data.AsianOver200);
    // })
    // // .attr("r", "5")
    // .attr("r",function(data,index){
    //   return data.total_population/1000;
    // })
    // .attr("fill", "#22AA88")
    // .attr("opacity",.5)
  
    // // make circles for the race population but all in the lower left corner
    asian
      .selectAll("circle")
      .data(morePlayData)
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
      // .attr("r", "5")
      .attr("r",function(data,index){
        return data.asian_population/1000;
      })
      .attr("fill", "#E75480")
      .attr("opacity",.3)
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
        // return index * svgWidth / 20;
        return xLinearScale(+data[currentAxisLabelX]);
      })
      .attr("cy", function(data, index) {
        // return 600 - data * svgHeight / 80;
        return yLinearScale(data.AsianOver200);
      });


         // // make circles for the race population but all in the lower left corner
    black
    .selectAll("circle")
    .data(morePlayData)
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
    // .attr("r", "5")
    .attr("r",function(data,index){
      return data.black_population/1000;
    })
    .attr("fill", "#000000")
    .attr("opacity",.3)
    // // display tooltip on click
    // .on("click", function(data) {
    //   toolTip.show(data);
    // })
    // // hide tooltip on mouseout
    // .on("mouseout", function(data, index) {
    //   toolTip.hide(data);
    // });

    // now animate the circles
    black
    .selectAll("circle")
    .transition()
    .duration(1000)
    .attr("cx", function(data, index) {
      // return index * svgWidth / 20;
      return xLinearScale(+data[currentAxisLabelX]);
    })
    .attr("cy", function(data, index) {
      // return 600 - data * svgHeight / 80;
      return yLinearScale(data.BlackOver200);
    }); 
  
    // Append an SVG group for the x-axis, then display the x-axis
    asian
      .append("g")
      .attr("transform", "translate(0," + height + ")")
      // The class name assigned here will be used for transition effects
      .attr("class", "x-axis")
      .call(bottomAxis);
  
    // Append a group for y-axis, then display it
    asian.append("g").call(leftAxis);
  
    // Append y-axis label
    asian
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 40)
      .attr("x", 0 - height / 2)
      .attr("dy", "1em")
      .attr("class", "axis-text")
      .attr("data-axis-name", "population")
      .text("Population");
  
    // Append x-axis labels
    asian
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


// // ----------------------------------- black --------------------------------------------------

// var svg2 = d3
// .select(".black")
// .append("svg")
// .attr("width", svgWidth)
// .attr("height", svgHeight)
// .append("g")
// .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// var black = svg2.append("g");
// var total2 = svg2.append("g");

// d3.csv("All200.csv", function(err,morePlayData){
//   if (err) throw err;
  
//     //this creates a list for all of the data points?
//     morePlayData.forEach(function(data) {
//       data.race_population = +data.BlackOver200;
//       data.total_population = +data.TotalOver200;
//       // data.population = +data.Over200;
//       // data.income_level = data.income_level;
//     });

//       // Create scale functions
//   var yLinearScale = d3.scaleLinear().range([height, 0]);
  
//     var xLinearScale = d3.scaleLinear().range([0, width]);
  
//     // Create axis functions
//     var bottomAxis = d3.axisBottom(xLinearScale);
//     var leftAxis = d3.axisLeft(yLinearScale);
  
//     // These variables store the minimum and maximum values in a column in data.csv
//     var xMin;
//     var xMax;
//     var yMin;
//     var yMax;
  
//     // This function identifies the minimum and maximum values in a column in playData.csv
//     // and assign them to xMin and xMax variables, which will define the axis domain
//     // it also obtains the max y value
//     function findMinAndMax(dataColumnY) {
//       yMin = d3.min(morePlayData, function(data) {
//         return +data[dataColumnY] * .8;
//       });
  
//       yMax = d3.max(morePlayData, function(data) {
//         return +data[dataColumnY] * 1.1;
//       });
//     }
  
//     // The default x-axis is 'year'
//     // Another axis can be assigned to the variable during an onclick event.
//     // This variable is key to the ability to change axis/data column
//     var currentAxisLabelX = "Year";
//     var currentAxisLabelY = "BlackOver200";
  
//     // Call findMinAndMax() with 'year' as default
//     findMinAndMax(currentAxisLabelY); //if these calls weren't wrapped in a function, would we run the risk of not having values?
//     // the function is not returning anything - it's only making calls
  
//     // Set the domain of an axis to extend from the min to the max value of the data column
//     // let's hard code min and max x values to match years
//     xMin = 1999;
//     xMax = 2017;
//     // yMax = 30000;
//     xLinearScale.domain([xMin, xMax]);
//     yLinearScale.domain([yMin, yMax]);
//     // console.log("max y", yMax);
  
//     // // try this later
//     // // Initialize tooltip
//     // var toolTip = d3
//     //   .tip()
//     //   .attr("class", "tooltip")
//     //   // Define position
//     //   .offset([80, -60])
//     //   // The html() method allows us to mix JavaScript with HTML in the callback function
//     //   .html(function(data) {   //how does this know it is looking at the csv data?
//     //     var bandName = data.rockband;
//     //     var numHits = +data.num_hits;
//     //     var bandInfo = +data[currentAxisLabelX];
//     //     var bandString;
//     //     // Tooltip text depends on which axis is active/has been clicked
//     //     if (currentAxisLabelX === "hair_length") {
//     //       bandString = "Hair length: ";
//     //     }
//     //     else {
//     //       bandString = "Number of albums: ";
//     //     }
//     //     return bandName +
//     //       "<br>" +
//     //       bandString +
//     //       bandInfo +
//     //       "<br> Hits: " +
//     //       numHits;
//     //   });
  
//     // // Create tooltip
//     // chart.call(toolTip);

//     // make circles for the total population
//     total2
//     .selectAll("circle")
//     .data(morePlayData)
//     .enter()
//     .append("circle")
//     .attr("cx", function(data, index) {
//       return xLinearScale(+data[currentAxisLabelX]);
//     })
//     .attr("cy", function(data, index) {
//       return yLinearScale(data.BlackOver200);
//     })
//     // .attr("r", "5")
//     .attr("r",function(data,index){
//       return data.total_population/1000;
//     })
//     .attr("fill", "#22AA88")
//     .attr("opacity",.5)
  
//     // make circles for the race population
//     black
//       .selectAll("circle")
//       .data(morePlayData)
//       .enter()
//       .append("circle")
//       .attr("cx", function(data, index) {
//         return xLinearScale(+data[currentAxisLabelX]);
//       })
//       .attr("cy", function(data, index) {
//         return yLinearScale(data.BlackOver200);
//       })
//       // .attr("r", "5")
//       .attr("r",function(data,index){
//         return data.race_population/1100;
//       })
//       .attr("fill", "#E75480")
//       // // display tooltip on click
//       // .on("click", function(data) {
//       //   toolTip.show(data);
//       // })
//       // // hide tooltip on mouseout
//       // .on("mouseout", function(data, index) {
//       //   toolTip.hide(data);
//       // });
  
//     // Append an SVG group for the x-axis, then display the x-axis
//     black
//       .append("g")
//       .attr("transform", "translate(0," + height + ")")
//       // The class name assigned here will be used for transition effects
//       .attr("class", "x-axis")
//       .call(bottomAxis);
  
//     // Append a group for y-axis, then display it
//     black.append("g").call(leftAxis);
  
//     // Append y-axis label
//     black
//       .append("text")
//       .attr("transform", "rotate(-90)")
//       .attr("y", 0 - margin.left + 40)
//       .attr("x", 0 - height / 2)
//       .attr("dy", "1em")
//       .attr("class", "axis-text")
//       .attr("data-axis-name", "population")
//       .text("Black Population Income Over $200k");
  
//     // Append x-axis labels
//     black
//       .append("text")
//       .attr(
//         "transform",
//         "translate(" + width / 2 + " ," + (height + margin.top + 20) + ")"
//       )
//       // This axis label is active by default
//       .attr("class", "axis-text active")
//       .attr("data-axis-name", "year")
//       .text("Year");

// });
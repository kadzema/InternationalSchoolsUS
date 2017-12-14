//this will be selected from dropdown
// var countyName = "Los Angeles County, California"
var countyName = "New York County, New York"

d3.json("/county/"+ countyName, function (data) {
  console.log("data",data);

  // the total population chart------------------------------------------------------------------------------------------------
  var totalSvg = dimple.newSvg(".totalpop", 690, 400);  //width, height
  // Create the chart
  var totalChart = new dimple.chart(totalSvg, data);
  totalChart.setBounds(60, 30, 510, 330)   // x, y, width, height

  // Create a standard bubble of total race population by year
  // We are coloring by race as that will be the key in the legend
  x = totalChart.addTimeAxis("x", "Year", "%Y", "%Y");
  y = totalChart.addMeasureAxis("y", "TotalPopulation");
  totalChart.addSeries(["Year","TotalPopulation", "Race"], dimple.plot.bubble); //i swear i read that the last in the series is what shows in the legend, but i can't find that!
  var myLegend = totalChart.addLegend(570, 75, 100, 400, "Right");  // x, y, width, height, horizontal align
  totalChart.draw();

  // This is a critical step.  By doing this we orphan the legend. This
  // means it will not respond to graph updates.  Without this the legend
  // will redraw when the chart refreshes removing the unchecked item and
  // also dropping the events we define below.
  totalChart.legends = [];

  // This block simply adds the legend title. I put it into a d3 data
  // object to split it onto 2 lines.  This technique works with any
  // number of lines, it isn't dimple specific.
  totalSvg.selectAll("title_text")
    .data(["Click legend to","show/hide races:"])
    .enter()
    .append("text")
      .attr("x", 585)
      .attr("y", function (d, i) { return 40 + i * 14; })
      .style("font-family", "sans-serif")
      .style("font-size", "10px")
      .style("color", "Black")
      .text(function (d) { return d; });

  // Get a unique list of race values to use when filtering
  var filterValues = dimple.getUniqueValues(data, "Race");
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
      totalChart.data = dimple.filterData(data, "Race", filterValues);
      // Passing a duration parameter makes the chart animate. Without
      // it there is no transition
      totalChart.draw(800);
    });

    // the percentage ot total population chart------------------------------------------------------------------------------------------------
    var percentageSvg = dimple.newSvg(".totalPercentage", 690, 400);
    var perentageChart = new dimple.chart(percentageSvg, data);
    perentageChart.setBounds(60, 30, 510, 330)
    x = perentageChart.addTimeAxis("x", "Year", "%Y", "%Y");
    y = perentageChart.addMeasureAxis("y", "TotalPercentage");
    perentageChart.addSeries(["Year","TotalPercentage", "Race"], dimple.plot.bubble);
    var myLegend = perentageChart.addLegend(570, 75, 100, 400, "Right");
    perentageChart.draw();
    perentageChart.legends = [];

    percentageSvg.selectAll("title_text")
      .data(["Click legend to","show/hide races:"])
      .enter()
      .append("text")
        .attr("x", 585)
        .attr("y", function (d, i) { return 40 + i * 14; })
        .style("font-family", "sans-serif")
        .style("font-size", "10px")
        .style("color", "Black")
        .text(function (d) { return d; });

    var filterValues = dimple.getUniqueValues(data, "Race");

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
        perentageChart.data = dimple.filterData(data, "Race", filterValues);
        // Passing a duration parameter makes the chart animate. Without it there is no transition
        perentageChart.draw(800);
      });



    // the over 150 percentage chart------------------------------------------------------------------------------------------------
    var over150Svg = dimple.newSvg(".over150Percentage", 690, 400);
    var over150Chart = new dimple.chart(over150Svg, data);
    over150Chart.setBounds(60, 30, 510, 330)
    x = over150Chart.addTimeAxis("x", "Year", "%Y", "%Y");
    y = over150Chart.addMeasureAxis("y", "Over150Percentage");
    over150Chart.addSeries(["Year","Over150Percentage", "Race"], dimple.plot.bubble);
    var myLegend = over150Chart.addLegend(570, 75, 100, 400, "Right");
    over150Chart.draw();
    over150Chart.legends = [];
  
    over150Svg.selectAll("title_text")
      .data(["Click legend to","show/hide races:"])
      .enter()
      .append("text")
        .attr("x", 585)
        .attr("y", function (d, i) { return 40 + i * 14; })
        .style("font-family", "sans-serif")
        .style("font-size", "10px")
        .style("color", "Black")
        .text(function (d) { return d; });
  
    var filterValues = dimple.getUniqueValues(data, "Race");

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
        over150Chart.data = dimple.filterData(data, "Race", filterValues);
        // Passing a duration parameter makes the chart animate. Without it there is no transition
        over150Chart.draw(800);
      });

      // the over 200 percentage chart------------------------------------------------------------------------------------------------
  var over200Svg = dimple.newSvg(".over150Percentage", 690, 400);
  
    // Create the chart
    var over200Chart = new dimple.chart(over200Svg, data);
    over200Chart.setBounds(60, 30, 510, 330)
  
    // Create a standard bubble of studentCount by year
    // We are coloring by county as that will be the key in the legend
    x = over200Chart.addTimeAxis("x", "Year", "%Y", "%Y");
    y = over200Chart.addMeasureAxis("y", "Over200Percentage");
    over200Chart.addSeries(["Year","Over200Percentage", "Race"], dimple.plot.bubble);
    // myChart.addSeries("TotalPopulation", dimple.plot.bubble);
    var myLegend = over200Chart.addLegend(570, 75, 100, 400, "Right");
    over200Chart.draw();
    over200Chart.legends = [];
  
    over200Svg.selectAll("title_text")
      .data(["Click legend to","show/hide races:"])
      .enter()
      .append("text")
        .attr("x", 585)
        .attr("y", function (d, i) { return 40 + i * 14; })
        .style("font-family", "sans-serif")
        .style("font-size", "10px")
        .style("color", "Black")
        .text(function (d) { return d; });
  
    // Get a unique list of Race values to use when filtering
    var filterValues = dimple.getUniqueValues(data, "Race");
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
        over200Chart.data = dimple.filterData(data, "Race", filterValues);
        // Passing a duration parameter makes the chart animate. Without
        // it there is no transition
        over200Chart.draw(800);
      });

});


// new data set!
// the origins chart-----------------------------------------------------------------------------------------------
var originSvg = dimple.newSvg(".originChart", 690, 400);
d3.json("/origin", function (data) {

  // console.log("data",data.origins[0]);

  var myChart = new dimple.chart(originSvg, data.origins);
  myChart.setBounds(60, 30, 510, 330)

  x = myChart.addTimeAxis("x", "year", "%Y", "%Y");
  y = myChart.addMeasureAxis("y", "studentcount");
  myChart.addSeries(["year","origin"], dimple.plot.bubble);
  var myLegend = myChart.addLegend(630, 45, 75, 300, "Right");
  myChart.draw();

  myChart.legends = [];

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

// the university chart------------------------------------------------------------------------------------------------
var univSvg = dimple.newSvg(".universityCounty", 690, 400);
d3.json("/univCounty", function (data) {
  // console.log("data",data.universities[0]);

  var myChart = new dimple.chart(univSvg, data.universities);
  myChart.setBounds(60, 30, 510, 330)

  x = myChart.addTimeAxis("x", "year", "%Y", "%Y");
  y = myChart.addMeasureAxis("y", "students");
  myChart.addSeries(["year","university", "county"], dimple.plot.bubble);
  var myLegend = myChart.addLegend(620, 45, 155, 400, "Right");
  myChart.draw();

  myChart.legends = [];

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


// D3 Scatterplot Assignment

// Students:
// =========
// Follow your written instructions and create a scatter plot with D3.js.

var svgWidth = 960;
var svgHeight = 600;

var margin = {
  top: 40,
  right: 40,
  bottom: 40,
  left: 120
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3.select(".chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight)

var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Import Data
d3.csv("first_graph.csv", function (err, demoData) {
  if (err) throw err;

  // Step 1: Parse Data/Cast as numbers
   // ==============================
  demoData.forEach(function (data) {
    data.overFiveYears = +data.overFiveYears;
    data.firstMarriage = +data.firstMarriage;
  });

  // Step 2: Create scale functions
  // ==============================
  var xLinearScale = d3.scaleLinear()
    .domain([2, 13.5])
    .range([0, width]);

  var yLinearScale = d3.scaleLinear()
    .domain([25, 31])
    .range([height, 0]);

  // Step 3: Create axis functions
  // ==============================
  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  // Step 4: Append Axes to the chart
  // ==============================
  chartGroup.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

  chartGroup.append("g")
    .call(leftAxis);

   // Step 5: Create Circles
  // ==============================
  var circlesGroup = chartGroup.selectAll("circle")
  .data(demoData)
  .enter()
  .append("circle")
  .attr("cx", d => xLinearScale(d.overFiveYears))
  .attr("cy", d => yLinearScale(d.firstMarriage))
  .attr("r", "10")
  .attr("fill", "purple")
  .attr("opacity", ".6")
  .attr("label", d => d.stateAbbr)

  // Step 6: Initialize tool tip
  // ==============================
  var toolTip = d3.tip()
    .attr("class", "tooltip")
    .offset([80, -60])
    .html(d =>
      `${d.stateName}<br>5+ Yrs since Doctor : ${d.overFiveYears}%<br>Age at First Marriage: ${d.firstMarriage}`
    );

  // Step 7: Create tooltip in the chart
  // ==============================
  chartGroup.call(toolTip);

  // Step 8: Create event listeners to display and hide the tooltip
  // ==============================
  circlesGroup.on("mouseover", function (data) {
      toolTip.show(data);
    })
    // onmouseout event
    .on("mouseout", function (data, index) {
      toolTip.hide(data);
    });

  // Create axes labels
  chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 70)
    .attr("x", 0 - (height * 4/5))
    .attr("class", "axisText")
    .text("Median Age at First Marriage");

  chartGroup.append("text")
    .attr("transform", `translate(${width/5}, ${height + margin.top - 4})`)
    .attr("class", "axisText")
    .text("% of People who indicated 5+ Years Since Last Doctor Visit");
});

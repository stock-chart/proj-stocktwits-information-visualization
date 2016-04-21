
render_line_chart();

function render_line_chart() {

  line_data = d3.select("#line-chart");

  // Set the dimensions of the canvas / graph
  var margin_l = {top: 0, right: 20, bottom: 30, left: 25},
      width_l = 600 - margin_l.left - margin_l.right,
      height_l = 200 - margin_l.top - margin_l.bottom;

  // Parse the date  time
  var parseDate = d3.time.format("%d-%b-%y").parse;

  // Set the ranges
  var x = d3.time.scale().range([0, width_l]);
  var y = d3.scale.linear().range([height_l, 0]);

  // Define the axes
  var xAxis = d3.svg.axis().scale(x)
      .orient("bottom").ticks(3);

  var yAxis = d3.svg.axis().scale(y)
      .orient("left").ticks(3);

  // Define the line
  var valueline = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.sentiment); });
      
  // Adds the svg canvas
  var svg = d3.select("#line-chart")
      .append("svg")
          .attr("width", width_l + margin_l.left + margin_l.right)
          .attr("height", height_l + margin_l.top + margin_l.bottom)
      .append("g")
          .attr("transform", 
                "translate(" + margin_l.left + "," + margin_l.top + ")");

  // Get the data
  d3.json("../static/data/line_area_chart.json", function(error, data) {
      data.forEach(function(d) {
          d.date = parseDate(d.date);
          d.sentiment = +d.sentiment;
      });

      // Scale the range of the data
      x.domain(d3.extent(data, function(d) { return d.date; }));
      y.domain([0, d3.max(data, function(d) { return d.sentiment; })]);

      // Add the valueline path.
      svg.append("path")
          .attr("class", "line")
          .attr("d", valueline(data));

      // Add the X Axis
      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height_l + ")")
          .call(xAxis);

      // Add the Y Axis
      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis);

  });

}
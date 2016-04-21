
render_area_chart();

function render_area_chart() {

	area_data = d3.select("#area-chart");

	var margin = {top: 0, right: 20, bottom: 30, left: 25},
		width = 680 - margin.left - margin.right,
	    height = 90 - margin.top - margin.bottom;

	var parseDate = d3.time.format("%d-%b-%y").parse;

	var x = d3.time.scale()
	    .range([0, width]);

	var y = d3.scale.linear()
	    .range([height, 0]);

	// var xAxis = d3.svg.axis()
	//     .scale(x)
	//     .orient("bottom");

	// var yAxis = d3.svg.axis()
	//     .scale(y)
	//     .orient("left")
  var xAxis = d3.svg.axis().scale(x)
      .orient("bottom").ticks(3);

  var yAxis = d3.svg.axis().scale(y)
      .orient("left").ticks(2);

	var area = d3.svg.area()
	    .x(function(d) { return x(d.date); })
	    .y0(height)
	    .y1(function(d) { return y(d.sent); });

	var svg = d3.select("#area-chart")
		.append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	d3.tsv("../static/data/data.tsv", function(error, data) {
	  if (error) throw error;

	  data.forEach(function(d) {
	    d.date = parseDate(d.date);
	    d.sent = +d.sent;
	  });

	  x.domain(d3.extent(data, function(d) { return d.date; }));
	  y.domain([0, d3.max(data, function(d) { return d.sent; })]);

	  svg.append("path")
	      .datum(data)
	      .attr("class", "area")
	      .attr("d", area);

	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis);

	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("Volume")
	      .style({"font-size": 10, fill:"#000"});
	});
}
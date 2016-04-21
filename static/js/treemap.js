render_treemap();

function render_treemap() {

	tree_map = d3.select("#treemap");

	var margin = {top: 0, right: 0, bottom: 0, left: 0},
	    width = 600 - margin.left - margin.right,
	    height = 300 - margin.top - margin.bottom;

	// var color = d3.scale.category10();
	// var canvas = d3.select("body").append("svg")
	//    .attr("width", width + "px")
	//    .attr("height", height + "px");
	    
	var treemap = d3.layout.treemap()
	    .size([width, height])
	    .sticky(true)
	    .value(function(d) { return d.count; });

	var div = tree_map.append("div")
	    .style("position", "relative")
	    .style("width", (width + margin.left + margin.right) + "px")
	    .style("height", (height + margin.top + margin.bottom) + "px")
	    .style("left", margin.left + "px")
	    .style("top", margin.top + "px");

	d3.json("static/data/treemap_new.json", function(error, root) {
	  if (error) throw error;

	  var node = div.datum(root).selectAll(".node")
	      .data(treemap.nodes)
	    .enter().append("div")
	      .attr("class", "node")
	      .call(position)
	      .style("background", function(d) { return d.sentiment > 50 ? "#BCE0B9" : "#EAD5D5"; })
	      .text(function(d) { 
	      	if (d.count > 30) {
		      	return d.children ? null : ("$" + d.symbol); 
			}
	      })
	      .attr("align", "center");
	     // .attr("vertical", "middle");
	  
	});

	function position() {
	  this.style("left", function(d) { return d.x + "px"; })
	      .style("top", function(d) { return d.y + "px"; })
	      .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
	      .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
	}
}
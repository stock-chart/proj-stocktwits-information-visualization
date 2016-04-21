render_treemap();

function render_treemap() {

		tree_map = d3.select("#treemap");

	var margin = {top: 40, right: 20, bottom: 30, left: 25},
	    width = 710 - margin.left - margin.right,
	    height = 370 - margin.top - margin.bottom;

	//var color = d3.scale.category10();
	//var canvas = d3.select("body").append("svg")
	 //   .attr("width", width + "px")
	  //  .attr("height", height + "px");
	    
	var treemap = d3.layout.treemap()
	    .size([width, height])
	    .sticky(true)
	    .value(function(d) { return d.count; });

	var div = d3.select("#treemap").append("div")
	    .style("position", "relative")
	    .style("width", (width + margin.left + margin.right))
	    .style("height", (height + margin.top + margin.bottom))
	    .style("left", margin.left)
	    .style("top", margin.top);

	d3.json("../static/data/treemap_y.json", function(error, root) {
	  if (error) throw error;

	  var node = div.datum(root).selectAll(".node")
	      .data(treemap.nodes)
	    .enter().append("div")
	      .attr("class", "node")
	      .call(position)
	      .style("background", function(d) { return d.sentiment > 50 ? "#B9F6CA" : "#FF8A80"; })
	      .text(function(d) { return d.children ? null : d.title; })
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
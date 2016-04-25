render_treemap();

function render_treemap() {
    var margin = {top: 0, right: 0, bottom: 0, left: 0},
        w = 600 - margin.left - margin.right,
        h = 300 - margin.top - margin.bottom;

    var x = d3.scale.linear().range([0, w]),
        y = d3.scale.linear().range([0, h]),
        color = d3.scale.category20c(),
        root,
        node;

    var treemap = d3.layout.treemap()
        .round(false)
        .size([w, h])
        .sticky(true)
        .value(function(d) { return d.count; });

    var svg = d3.select("#treemap").append("div")
        .attr("class", "chart")
        .style("width", w + "px")
        .style("height", h + "px")
      .append("svg:svg")
        .attr("width", w)
        .attr("height", h)
      .append("svg:g")
        .attr("transform", "translate(.5,.5)");

    var svg2 = d3.select("#treemap").append("div")
        .attr("class", "chart2")
        .style("width", w + "px")
        .style("height", h + "px")
        .style("margin-top", -(h) + "px")
      .append("svg:svg")
        .attr("width", w)
        .attr("height", h)
      .append("svg:g")
        .attr("transform", "translate(.5,.5)");    

    d3.json("/static/data/treemap.json", function(data) {
      node = root = data;

      var nodes_parent = treemap.nodes(root)
          .filter(function(d) { return d.children && d.name != "treemap"; }); 

      var nodes_child = treemap.nodes(root)
          .filter(function(d) { return !d.children; });     

      var parent = svg.selectAll("g")
          .data(nodes_parent)
        .enter().append("svg:g")
          .attr("class", "parent")
          .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
          // .on("click", function(d) { return zoom(node == d.parent ? root : d.parent); })
          ;

      parent.append("svg:rect")
          .attr("width", function(d) { return d.dx - 1; })
          .attr("height", function(d) { return d.dy - 1; })
          .style("fill", function(d) { return "white" })
          .style("stroke", "black")
          // .style("opacity", "0.3")
          ;

      parent.append("svg:text")
          .attr("x", function(d) { return d.dx / 2; })
          .attr("y", function(d) { return d.dy / 2; })
          .attr("dy", ".35em")
          .attr("text-anchor", "middle")
          // .text(function(d) { return ("$" + d.name); })
          .style("font-size", "8px")
          .style("opacity", function(d) { d.w = this.getComputedTextLength(); return (d.dx > d.w) ? 1 : 0; });


      var child = svg2.selectAll("g")
          .data(nodes_child)
        .enter().append("svg:g")
          .attr("class", "child")
          .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
          .on("click", function(d) { $(".chart").addClass("opacityzero"); return zoom(node == d.parent ? root : d.parent); });

      child.append("svg:rect")
          .attr("width", function(d) { return d.dx - 1; })
          .attr("height", function(d) { return d.dy - 1; })
          .style("fill", function(d) { return d.sentiment > 50 ? "#BCE0B9" : "#EAD5D5"; })
          // .style("fill", function(d) { return color(d.parent.name) })
          ;

      child.append("svg:text")
          .attr("x", function(d) { return d.dx / 2; })
          .attr("y", function(d) { return d.dy / 2; })
          .attr("dy", ".35em")
          .attr("text-anchor", "middle")
          .text(function(d) { return ("$" + d.symbol); })
          .style("font-size", "8px")
          .style("opacity", function(d) { d.w = this.getComputedTextLength(); return (d.dx > d.w) ? 1 : 0; });

      d3.select(window).on("click", function() { $(".chart").removeClass("opacityzero"); zoom(root); });

      d3.select("select").on("change", function() {
        treemap.value(this.value == "size" ? size : count).nodes(root);
        zoom(node);
      });
    });

    function size(d) {
      return d.size;
    }

    function count(d) {
      return 1;
    }

    function zoom(d) {
      var kx = w / d.dx, ky = h / d.dy;
      x.domain([d.x, d.x + d.dx]);
      y.domain([d.y, d.y + d.dy]);

      var t = svg2.selectAll("g.child").transition()
          .duration(d3.event.altKey ? 7500 : 750)
          .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

      t.select("rect")
          .attr("width", function(d) { return kx * d.dx - 1; })
          .attr("height", function(d) { return ky * d.dy - 1; })

      t.select("text")
          .attr("x", function(d) { return kx * d.dx / 2; })
          .attr("y", function(d) { return ky * d.dy / 2; })
          .style("opacity", function(d) { return kx * d.dx > d.w ? 1 : 0; });

      node = d;
      d3.event.stopPropagation();
    }
}


render_idealist();

function render_idealist() {
    idealist = d3.select("#idealist");

    d3.json("static/latest_50_messages.json", function(error, result) {
    ideas = result;
    

    idealist_data = idealist.selectAll("div")
                            .data(ideas, function(d) {return d.body});
    
    idealist_data.enter()
                .append("div")
                .classed("list-group-item", true)
                .html(function(d) {

                	if (d.sentiment == "bull") {
                		return ('<span class="username">' + d.username + '</span><span class="sentiment bullidea">' + d.sentiment + "</span></br>" + d.body);
                	} else if (d.sentiment == "bear") {
                		return ('<span class="username">' + d.username + '</span><span class="sentiment bearidea">' + d.sentiment + "</span></br>" + d.body)
                	}
                	
                });
    })
}
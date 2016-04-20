idealist = d3.select("#idealist");

d3.json("http://data.consumerfinance.gov/api/views.json", function(error, result) {
    ideas = result;
    render_idealist();
})

function render_idealist() {
    idealist_data = idealist.selectAll("div")
                            .data(ideas, function(d) {return d.description});
    
    idealist_data.enter()
                .append("div")
                .classed("list-group-item", true)
                .html(function(d) {return ('<span class="username">' + d.id + "</span></br>" + d.description)});
}
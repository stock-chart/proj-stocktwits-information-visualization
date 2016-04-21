
render_stocklist();

function render_stocklist() {
    stocklist = d3.select("#stocklist");

    d3.json("static/data/top_50_list_new.json", function(error, result) {
    stocks = result["top_list"];
    

    stocklist_data = stocklist.selectAll("div")
                            .data(stocks, function(d) {return d.title});
    
    stocklist_data.enter()
                .append("div")
                .classed("list-group-item", true)
                .text(function(d) {return ("$" + d.title)});
    })
}


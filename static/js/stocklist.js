stocklist = d3.select("#stocklist");

d3.json("https://raw.githubusercontent.com/CristianFelix/infoviz/master/Week%203/newData.json", function(error, result) {
    stocks = result;
    render_stocklist();
})

function render_stocklist() {
    stocklist_data = stocklist.selectAll("div")
                            .data(stocks, function(d) {return d.name});
    
    stocklist_data.enter()
                .append("div")
                .classed("list-group-item", true)
                .text(function(d) {return ("$" + d.name)});
}





$("#searchbtn").click(function(){
	$.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: "1",
        b: "2"		
	}, function(data) {
		alert(data.result);
	});	
});

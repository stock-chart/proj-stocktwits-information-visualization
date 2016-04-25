
render_stocklist();

function render_stocklist() {
    stocklist = d3.select("#stocklist");

    d3.json("/static/data/top_50_list_new.json", function(error, result) {
    stocks = result["top_list"];

    top_count = 191;
    

    stocklist_data = stocklist.selectAll("div")
                            .data(stocks, function(d) {return d.title});
    
    stocklist_data.enter()
                .append("div")
                .classed("list-group-item", true)
                .html(function(d) {return ("<div class='stocklistitem' id='" + d.id + "'>$" + d.title + 
                                                "<div class='smallbar'>  \
                                                    <div class='smallbarcontainer'> \
                                                        <div class='smallbarbar' style='width:" + (d.count / top_count * 100) + "%'></div> \
                                                    </div> \
                                                    <span class='smallbarnum'>" + d.count + "</span> \
                                                <div> \
                                            <div>")})
                .on("mouseenter", function(d,i) {
                    $("#" + d.id).css("background", "grey");
                })
                .on("mouseleave", function(d,i) {
                    $(".stocklistitem").css("background", "initial");
                })                
                ;
    })
}



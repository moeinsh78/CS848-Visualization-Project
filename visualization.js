function draw_chart(data, field, time) {
    
    var min_id = d3.min(data, function (d){ return d.orig_id; });

    d3.select("#ranking-chart").selectAll("svg").remove();
    
    var margin = {top: 40, right: 60, bottom: 80, left: 200},
    width = 1000 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

    var svg = d3.select("#ranking-chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");

    

    var x = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.score)])
    .range([ 0, width]);
    svg.append("g")
    // change orientation to top
    .call(d3.axisTop(x))
    // change transform to translate to top
    .attr("transform", "translate(0," + margin.top - 40 + ")")
    .selectAll("text")
    .attr("transform", "translate(10,0)")
    .style("font-size", "15px")
    .style("text-anchor", "end");    


    // var x = d3.scaleLinear()
    // .domain([0, d3.max(data, d => d.score)])
    // .range([ 0, width]);
    // svg.append("g")
    // .attr("transform", "translate(0," + margin.top + ")")
    // .call(d3.axisTop(x))
    // .selectAll("text")
    // .attr("transform", "translate(-10,0)rotate(-45)")
    // .style("font-size", "15px")
    // .style("text-anchor", "end");
    

    var y = d3.scaleBand()
    .range([ 0, height ])
    .domain(data.map(d => d.university_name))
    .padding(.2);
    svg.append("g")
    .style("font-size", "15px")
    .call(d3.axisLeft(y))

    

    // var y = d3.scaleBand()
    // .range([ 0, height ])
    // .domain(data.map(d => d.university_name))
    // .padding(.2);
    // svg.append("g")
    // .style("font-size", "15px")
    // .call(d3.axisLeft(y))
    

    svg.selectAll("myRect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", x(0) )
    .attr("y", d => y(d.university_name))
    .attr('ry', 2) 
    .attr('stroke', "#69b3a2")
    .attr("width", d => x(d.score))
    .attr("height", y.bandwidth() )
    .attr("fill", "#69b3a2")
    .attr("value", d => (d.orig_id - min_id)) 
    
    
    
    var tooltip = d3.select("#tooltip");

    svg.selectAll("rect")
    .on("mouseover", function(event, d) {
        // Highlighting the selected bar
        d3.select(this)
        .attr("fill", "navy");

    
        tooltip.style("opacity", 1);

        tooltip.html(
            `
                <strong>${d.university_name} </strong><br>
                <p>
                Rank: ${d.ranking} <br>Score: ${d.score}
                </p>
                <img src=${d.image_url} width=${400} height=${230}>
            `
        )
        .style("font-style", "sans-serif")
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 10) + "px");
    })
    .on("mousemove", function(event, d) {
        tooltip.style("left", (event.pageX + 10) + "px")
           .style("top", (event.pageY - 10) + "px");
    })
    .on("mouseout", function(event, d) {
        d3.select(this)
            .attr("fill", "#69b3a2");
    
        svg.select("#detail").remove();

        tooltip.transition()
           .duration(200)
           .style("opacity", 0);
    });

}


function update_chart(selected_subfield, selected_time) {
    console.log(selected_subfield, selected_time)

    d3.csv("csranking_data.csv").then(function (data) {
        data.forEach((d) => {
            d.id_string = d[""];
            d.image_url = d.image_url;
            d.orig_id = +d.id_string;
            d.subfield = d.field;
            d.year = +d.time_period;
            d.rank = +d.ranking;
            d.university = d.university_name;
            d.score = +d.score;
            d.faculty = +d.faculty;
        });
        
        var filtered_data = data.filter(function (d) {
            return (d.subfield == selected_subfield) && (d.year == selected_time);
        });
        
        console.log(filtered_data.slice(0, 10))
        draw_chart(filtered_data.slice(0, 10), selected_subfield, selected_time)
    });
}


function main() {      
    document.getElementById("subfieldSelect")
    .addEventListener("change", function () {
        update_chart(this.value, document.getElementById("yearSelect").value);
    });

    document.getElementById("yearSelect")
    .addEventListener("change", function () {
        update_chart(document.getElementById("subfieldSelect").value, this.value);
    });

    update_chart("all", "2020");
}
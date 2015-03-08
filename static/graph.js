d3.select("#dest").on("input", function() {
  update_url();
});

d3.select("#day_select").on("input", function() {
  update_url();
});

d3.select("#station_select").on("input", function() {
  update_url();
});

d3.select("#day_select").on("input", function() {
  update_url();
});

d3.select("#time").on("input", function() {
  update_slider(+this.value);
  update_url();
});

function update_slider(time) {
  var dateObj = new Date();
  dateObj.setHours(Math.floor(time/60));
  dateObj.setMinutes(time % 60);
  d3.select("#prettyTime").text(dateObj.toTimeString().substring(0, 5));
}

var margin = {top: 20, right: 20, bottom: 100, left: 60};
var width = 600 - margin.left - margin.right;
var height = 400 - margin.top - margin.bottom;

// whitespace on either side of the bars in units of minutes
var binMargin = .1;

var x = d3.scale.linear()
    .range([0,  width])
    .domain([0, 25]);
var y = d3.scale.linear()
    .range([height, 0])
    .domain([0, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(6);
var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10);

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .text("ETD (minutes)")
      .attr("dy", "3em")
      .attr("text-align", "center")
      .attr("x", width / 2 - margin.right - margin.left);

svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
  .append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("dy", "-2em")
    .text("Count");

      function make_graph(url) {

        d3.csv(url, type, function(error, data) {
          y.domain([0, d3.max(data, function(d) { return d.count; })]);

          svg.selectAll("g.y.axis")
            .call(yAxis);

          var bars = svg.selectAll(".bar")
              .data(data, function(d) { return d.etd; });

          bars.transition(1000)
              .attr("y", function(d) { return  y(d.count); } )
              .attr("height", function(d) { return height - y(d.count); } );

          bars.enter().append("rect")
              .attr("class", "bar")
              .attr("x", function(d) { return x(d.etd); })
              .attr("width", x(1 - 2 * binMargin))
              .attr("y", height)
              .attr("height", 0)
              .transition(1000)
              .attr("y", function(d) { return y(d.count); })
              .attr("height", function(d) { return height - y(d.count); });

          bars.exit()
              .transition(1000)
              .attr("y", height)
              .attr("height", 0)
              .remove();
        });
      }


var URL_BASE = "http://localhost:5000/";

function update_url(dest) {
  dest = document.getElementById("dest").value;
  station = document.getElementById("station_select").value;
  day = document.getElementById("day_select").value;
  time = document.getElementById("time").value;
  url = URL_BASE +
        "?dest=" + dest +
        "&time=" + time +
        "&station=" + station +
        "&day=" + day;
  console.log(url)
  make_graph(url);
}

update_url();
update_slider(time);

function type(d) {
  d.etd = +d.etd;
  d.count = +d.count;
  return d;
}

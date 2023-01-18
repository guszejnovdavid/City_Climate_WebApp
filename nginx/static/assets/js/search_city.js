d3.csv("static/db/cities.csv").then(function (data) {
  var db = data;
  var button = d3.select("#button");
  var form = d3.select("#form");

  button.on("click", runEnter);
  form.on("submit", runEnter);

  function runEnter() {
    d3.select("tbody").html("")
    d3.selectAll("p").classed('noresults', true).html("")
    d3.event.preventDefault();
    // var inputElement = d3.select("#user-input");
    // var inputValue = inputElement.property("value").toLowerCase().trim();
    
    var city_name_Element = d3.select("#city_name_input");
    var city_name_Value = city_name_Element.property("value").toLowerCase().trim();
    var continent_Element = d3.select("#continent_input");
    var continent_Value = continent_Element.property("value")
    var exclusion_radius_Element = d3.select("#exclusion_radius_input");
    var exclusion_radius_Value = exclusion_radius_Element.property("value").toLowerCase().trim();

    if (city_name_Value.length < 3){
      d3.select("p").classed('noresults2', true).html("<p><strong>Please enter at least 3 characters!</strong></p>")
      city_name_Value = "Unknown City"
    }
    if (exclusion_radius_Value.length < 1){ //default no exclusion radius
      exclusion_radius_Value = "0"
    }
    //var filteredData = db.filter(db => db.City.toLowerCase().trim().includes(city_name_Value));
    var filteredData = db.filter(db => db.City.toLowerCase().trim().includes(city_name_Value));
    if (filteredData.length === 0 && city_name_Value !== "Unknown City"){
      d3.select("p").classed('noresults', true).html("<center><strong>No results. Please check your spelling!</strong>")
    }
    output = filteredData
    //output = _.sortBy(filteredData, 'City')

    for (var i = 0; i < filteredData.length; i++) {
      d3.select("tbody").insert("tr").html("<td>"+[i+1]+"</td>" + "<td>" +(output[i]['Key'])+"</td>" +"<td>" +("<a href=\""+output[i]['Key'].replace(/\//g, '_').replace(/ /g, '-')+"&"+continent_Value+"&"+exclusion_radius_Value+"\" class=\"button\">Set as reference city</a>")+"</td>") }
      
      
  };
  window.resizeTo(screen.width,screen.height)


});
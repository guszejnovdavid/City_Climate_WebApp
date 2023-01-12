d3.csv("../db/city_climate_dataframe.csv").then(function (data) {
  console.log(data);

  var db = data;

  var button = d3.select("#button");

  var form = d3.select("#form");

  button.on("click", runEnter);
  form.on("submit", runEnter);

  function runEnter() {
    d3.select("tbody").html("")
    d3.selectAll("p").classed('noresults', true).html("")
    d3.event.preventDefault();
    var inputElement = d3.select("#user-input");
    var inputValue = inputElement.property("value").toLowerCase().trim();

    if (inputValue.length < 3){
      d3.select("p").classed('noresults2', true).html("<p><strong>Please enter at least 3 characters!</strong></p>")
      inputValue = "Something to give no results"
    }
    var filteredData = db.filter(db => db.City.toLowerCase().trim().includes(inputValue));
    if (filteredData.length === 0 && inputValue !== "Something to give no results"){
      d3.select("p").classed('noresults', true).html("<center><strong>No results. Please check your spelling!</strong>")
    }
    output = filteredData
    //output = _.sortBy(filteredData, 'City')

    for (var i = 0; i < filteredData.length; i++) {
      d3.select("tbody").insert("tr").html("<td>"+[i+1]+"</td>" + "<td>" +(output[i]['Key'])+"</td>" +"<td>" +("<input type=\"button\" value=\"Set as reference city\" onclick=\"window.location.href = city/" +   output[i]['Key'].replace(/\//g, '_')  + "\";>")+"</td>") }
  };
  window.resizeTo(screen.width,screen.height)


});
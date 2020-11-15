var apiURL = "http://localhost:5000/Zachary%20Gilliom"

function requestAPI(url) {
	/*d3.json(url)
	.then(function(data) {
		return data
	})
	*/
	var data = d3.json(url)
		return data
}

var a = requestAPI(apiURL);


var d = document.getElementById("d");

d.textContext(a);

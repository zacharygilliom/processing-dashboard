
function requestAPI() {
	d3.json("http://localhost:5000/Zachary%20Gilliom")
	.then(function(data) {
		console.log(data)
	}
}

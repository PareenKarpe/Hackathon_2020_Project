$(document).ready(function () {
    url = "data/final_ouput.csv";

    $.ajax({
        type: "GET",
        url: url,
        dataType: "text",
        success: function(data) {processData(data);}
     });


	function processData(allText) {
		console.log("hi!");
		// Get an array of lines
		var allTextLines = allText.split(/\r\n|\n/);
		// Get the number of columns using the first row
		var entries = allTextLines[0].split(',');
		var lines = [];

		// while there are elements in the row
		while (entries.length>0) {
			// remove that line, split it and store in our array 
			lines.push(entries.shift().split(','));
		}
		// Now do your stuff with the array lines
	
	}
});
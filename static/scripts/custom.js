$(document).ready(function () {
        console.log("in doc ready");
//        var url =  "{{ url_for('final_ouput.csv') }}";
        var url =  "data/final_ouput.csv";

        $.ajax({
            type: "GET",
            url: url,
            dataType: "text/csv",
            success: function(data) {processData(data);},
            error: function (jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
                console.log(msg);
            },
         });


        function processData(allText) {
            alert("in process");
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

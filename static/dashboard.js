$(function () {
    $("div.metric div.sparkline").each(function (index, elem) {
        var e = $(elem);
        var value_element = e.parent().find('p.value a');
        var timestamp_element = e.parent().find('span.timestamp');
        var original_value = value_element.html();
        
        var url = "/metric/" + e.data('metric') + ".json";
        $.getJSON(url, function(response) {
            // flot time series data needs to be in *milliseconds*, not seconds.
            // fixing this in Python would be easier but would limit reuse.
            for (var i=0; i < response.data.length; i++) {
                response.data[i][0] = response.data[i][0] * 1000;
            };
            var options = {
                xaxis: {show: false, mode: "time"},
                yaxis: {show: false, min: 0},
                grid: {borderWidth: 0, hoverable: true},
                colors: ["yellow"]
            };
            if (response.period != 'instant') {
                options.bars = {
                    show: true,
                    barWidth: 24 * 60 * 60 * 1000,
                    fillColor: "yellow",
                    lineWidth: 1,
                    align: "center",
                };
                options.lines = {show: false};
            }
            $.plot(e, [response.data], options);
            
            var dateformat = response.period == 'instant' ? "%b %d, %h:%M%p" : "%b %d";
            e.bind('plothover', function(event, pos, item) {
                if (item) {
                    value_element.html(Math.round(item.datapoint[1]));
                    var d = new Date(item.datapoint[0]);
                    timestamp_element.html($.plot.formatDate(d, dateformat));
                } else {
                    value_element.html(original_value);
                    timestamp_element.html('&nbsp;');
                }
            });
        });
        
        e.click(function() {
            window.location = "/metric/" + e.data('metric') + '/';
        })
    });
});
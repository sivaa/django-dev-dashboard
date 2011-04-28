$(function () {
    $("div.metric div.sparkline").each(function (index, elem) {
        var e = $(elem);
        var value_element = e.parent().find('p.value a');
        var timestamp_element = e.parent().find('span.timestamp');
        var original_value = value_element.html();
        
        var url = "/metric/" + e.data('metric') + ".json";
        $.getJSON(url, function(data) {
            // flot time series data needs to be in *milliseconds*, not seconds.
            // fixing this in Python would be easier but would limit reuse.
            for (var i=0; i < data.length; i++) {
                data[i][0] = data[i][0] * 1000;
            };
            var options = {
                xaxis: {show: false, mode: "time"},
                yaxis: {show: false, min: 0},
                grid: {borderWidth: 0, hoverable: true},
                colors: ["yellow"]
            };
            $.plot(e, [data], options);
            e.bind('plothover', function(event, pos, item) {
                if (item) {
                    value_element.html(item.datapoint[1]);
                    var d = new Date(item.datapoint[0]);
                    timestamp_element.html($.plot.formatDate(d, "%b %d, %h:%M%p"));
                } else {
                    value_element.html(original_value);
                    timestamp_element.html('&nbsp;');
                }
            });
        });
    });
});
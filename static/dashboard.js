$(function () {
    $("div.metric div.sparkline").each(function (index, elem) {
        var e = $(elem);
        var value_element = e.parent().find('p.value a');
        var original_value = value_element.html();
        
        var url = "/metric/" + e.data('metric') + ".json";
        $.getJSON(url, function(data) {
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
                } else {
                    value_element.html(original_value);
                }
            });
        });
    });
});
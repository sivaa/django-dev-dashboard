$(function () {
    $("div.metric div.sparkline").each(function (index, elem) {
        var url = "/metric/" + $(elem).data('metric') + ".json";
        $.getJSON(url, function(data) {
            var r = Raphael(elem.id);
            var line = r.g.linechart(0, 30, 95, 90, data.timestamps, [data.values]);
            line.attr({'stroke': 'yellow'});
        });
    });
});
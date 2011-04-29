$(function () {
    var e = $("#graph");
    var url = "/metric/" + e.data('metric') + ".json?days=365";
    $.getJSON(url, function(data) {
        for (var i=0; i < data.length; i++) {
            data[i][0] = data[i][0] * 1000;
        };
        var options = {
            xaxis: {
                mode: "time",
                tickColor: "rgba(0,0,0,0)",
                minTickSize: [1, "day"],
            },
            yaxis: {min: 0, ticks: 4},
            grid: {borderWidth: 0, hoverable: true, color: "white"},
            colors: ["yellow"],
        }
        $.plot(e, [data], options);
    });

    hover = {
        show: function(x, y, message) {
            $('<div id="hover">').html(message)
                .css({top: y+15, left: x+5})
                .appendTo('body')
                .show();
        },
        hide: function() {
            $("#hover").remove();
        }
    };
    
    var previousPoint = null;
    e.bind("plothover", function(event, pos, item) {
        if (item) {
            if (previousPoint != item.dataIndex) {
                previousPoint = item.dataIndex;
                hover.hide();
                var d = new Date(item.datapoint[0]);
                var ds = $.plot.formatDate(d, "%b %d, %h:%M%p")
                var m = ds + "<br>" + item.datapoint[1] + " tickets";
                hover.show(item.pageX, item.pageY, m)
            }
        } else {
            hover.hide();
            previousPoint = null;
        }
    });
});
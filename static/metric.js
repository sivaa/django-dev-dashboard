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
});
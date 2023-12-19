function colorizer(length) {
    total_color_lst = ["#FF0000", "#FF7F00", "#008080", "#808000", "#00FF00", "#0000FF", "#8B00FF"];
    var color = total_color_lst[Math.floor(Math.random()*total_color_lst.length)];
    var color_lst = [];
    var colorIndex = 0;

    for (i = 0; i < length; i++) {
        color_lst.push(anychart.color.lighten(color, colorIndex));
        colorIndex = colorIndex + length/1000*2;
    };

    return color_lst;
};

function country_visualize() {
    anychart.onDocumentReady(function() {
        var kr_data = country_data[0];
        var us_data = country_data[1];
        var id_data = country_data[2];
        var jp_data = country_data[3];

        var stage = acgraph.create('graph1');

        var us_data_lst = [];
        //var us_data_str = "";
        var kr_data_lst = [];
        for (i = 0; i < kr_data.length; i++) {
            kr_data_lst.push({x:kr_data[i], value:(kr_data.length-i)*1.5, category:'Korea', custom_field:i+1})
        }

        for (i = 0; i < us_data.length; i++) {
            us_data_lst.push({x:us_data[i], value:us_data.length-i*1.5, category:'United States', custom_field:i+1})
            //us_data_str += us_data[i]+","+String((us_data.length-i)*4)+',The United States\n'
        }

        var id_data_lst = [];
        for (i = 0; i < id_data.length; i++) {
            id_data_lst.push({x:id_data[i], value:(id_data.length-i)*1.5, category:'United Kingdom', custom_field:i+1})
        }

        var jp_data_lst = [];
        //var jp_data_str = "";
        for (i = 0; i < jp_data.length; i++) {
            jp_data_lst.push({x:jp_data[i], value:(jp_data.length-i)*1.5, category:'Japan', custom_field:i+1})
            //jp_data_str += jp_data[i]+","+String((jp_data.length-i)*4)+',Japan\n'
        }
        //console.log(jp_data_str)

        var us_dataSet = anychart.data.set(us_data_lst);
        var chartFirst = anychart.tagCloud();
        chartFirst.data(us_dataSet) .colorScale(anychart.scales.ordinalColor().colors(["#60727b"]))
            .fromAngle(-45).toAngle(45).anglesCount(3).textSpacing(5).bounds('0%', '0%', '26%', '105%').legend(true);
        chartFirst.background().fill("var(--bg-body-primary)");
        chartFirst.tooltip().format('Rank: {%custom_field}');
        chartFirst.mode("spiral");
        //chartFirst.labels().fontColor("var(--bg-body-primary)");

        var kr_dataSet = anychart.data.set(kr_data_lst);
        var chartSecond = anychart.tagCloud();
        chartSecond.data(kr_dataSet).colorScale(anychart.scales.ordinalColor().colors(['#3b8ad8']))
            .fromAngle(-45).toAngle(45).anglesCount(3).textSpacing(5).bounds('24%', '0%', '26%', '105%').legend(true);
        chartSecond.background().fill("var(--bg-body-primary)");
        chartSecond.tooltip().format('Rank: {%custom_field}');

        var id_dataSet = anychart.data.set(id_data_lst);
        var chartThird = anychart.tagCloud();
        chartThird.data(id_dataSet).colorScale(anychart.scales.ordinalColor().colors(['#f18126']))
            .fromAngle(-45).toAngle(45).anglesCount(3).textSpacing(5).bounds('48%', '0%', '26%', '105%').legend(true);
        chartThird.background().fill("var(--bg-body-primary)");
        chartThird.tooltip().format('Rank: {%custom_field}');

        var jp_dataSet = anychart.data.set(jp_data_lst);
        var chartFourth = anychart.tagCloud();
        chartFourth.data(jp_dataSet).colorScale(anychart.scales.ordinalColor().colors(['#DC143C']))
            .fromAngle(-45).toAngle(45).anglesCount(3).textSpacing(5).bounds('72%', '0%', '26%', '105%').legend(true);
        chartFourth.background().fill("var(--bg-body-primary)");
        chartFourth.tooltip().format('Rank: {%custom_field}');

        //title.container(stage);
        //title.draw();

        // add an event listener
        chartFirst.listen("pointClick", function(e){
            var url = "https://www.google.com/search?q=" + e.point.get("x");
            window.open(url, "_blank");
        });

        chartSecond.listen("pointClick", function(e){
            var url = "https://www.google.com/search?q=" + e.point.get("x");
            window.open(url, "_blank");
        });

        chartThird.listen("pointClick", function(e){
            var url = "https://www.google.com/search?q=" + e.point.get("x");
            window.open(url, "_blank");
        });

        chartFourth.listen("pointClick", function(e){
            var url = "https://www.google.com/search?q=" + e.point.get("x");
            window.open(url, "_blank");
        });

        chartFirst.container(stage);
        chartFirst.draw();

        chartSecond.container(stage);
        chartSecond.draw();

        chartThird.container(stage);
        chartThird.draw();

        chartFourth.container(stage);
        chartFourth.draw();
    });
}

/*
function country_visualize(country_data) {
    anychart.onDocumentReady(function() {
        var country_data_lst = [];
        for (i = 0; i < country_data.length; i++) {
            country_data_lst.push({"x":country_data[i], "value":country_data.length-i, category:country_data[i]})
        }
        var country_dataSet = anychart.data.set(country_data_lst);
        var country_chart = anychart.tagCloud(country_dataSet);
        country_chart.title('Real-time Trending Searches by Country'); // set a chart title
        country_chart.background().enabled(true);
        country_chart.background().fill("var(--bg-body-primary)");
        var customColorScale = anychart.scales.ordinalColor();
        customColorScale.colors(colorizer(country_data.length));
        //customColorScale.colors(["#FF3333", "#FF5533", "#FF9333", "#FFC133", "#FCFF33", "#ACFF33", "#33FF33", "#33FF77", "#33FFA8", "#33FFCE",
        //                         "#33C4FF", "#339FFF", "#3371FF", "#3352FF", "#5B33FF", "#6B33FF", "#A533FF", "#E033FF", "#FF3380", "#FF336B"]);
        country_chart.colorScale(customColorScale);
        $("#country").change(
            function() {
                var url_list = $(location).attr('href').split("/")

                $.ajax({
                type:"GET",
                url: url_list[url_list.length - 1],
                data: {country: $("#country").val()},
                success: function(country_data){
                    console.log(country_data)
                    var org_rows = country_dataSet.getRowsCount();
                    for (i = 0; i < country_data.length; i++) {
                        country_dataSet.append({"x":country_data[i], "value":country_data.length-i, category:country_data[i]})
                    }
                    for (i = 0; i < org_rows; i++) {
                        country_dataSet.remove(0)
                    }
                },
                error: function(error){
                    console.log(error);
                }
                })
            }
        );
        // add an event listener
        country_chart.listen("pointClick", function(e){
            var url = "https://www.google.com/search?q=" + e.point.get("x");
            window.open(url, "_blank");
        });

        country_chart.container("graph1");
        country_chart.draw();
    });
};
function year_visualize(year_data) {
    anychart.onDocumentReady(function() {
        var year_data_lst = [];
        for (i = 0; i < year_data.length; i++) {
            year_data_lst.push({"x":year_data[i], "value":year_data.length-i, category:year_data[i]})
        }

        var year_dataSet = anychart.data.set(year_data_lst);
        var year_chart = anychart.tagCloud(year_dataSet);
        //year_chart.title('Top Global Yearly Searches'); // set a chart title
        year_chart.background().enabled(true);
        year_chart.background().fill("var(--bg-body-primary)");
        $("#year").change(
            function() {
                var url_list = $(location).attr('href').split("/")

                $.ajax({
                type:"GET",
                url: url_list[url_list.length - 1],
                data: {year: $("#year").val()},
                success: function(year_data){
                    var org_rows = year_dataSet.getRowsCount();
                    for (i = 0; i < year_data.length; i++) {
                        year_dataSet.append({"x":year_data[i], "value":year_data.length-i, category:year_data[i]})
                    }
                    for (i = 0; i < org_rows; i++) {
                        year_dataSet.remove(0)
                    }
                },
                error: function(error){
                    console.log(error);
                }
                })
            }
        );
        // add an event listener
        year_chart.listen("pointClick", function(e){
            var url = "https://www.google.com/search?q=" + e.point.get("x");
            window.open(url, "_blank");
        });

        year_chart.container("graph2");
        year_chart.draw();
    });
};
*/

$(document).ready(
    function() {
        var url_list = $(location).attr('href').split("/")

        $.ajax({
        type:"GET",
        url: url_list[url_list.length - 1],
        data: {year: $("#year").val()},
        success: function(year_data){
            country_visualize();
            //year_visualize(year_data);
            },
        error: function(error){
            console.log(error);
            }
        })
    }
);
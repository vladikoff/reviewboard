$(function () {

    //RSS Feed Controls
    $("a#reload-news").click(function(evt){
         $("#news-content").load("feed/news/?reload=1");
          evt.preventDefault();
        });

    $("#news-content-widget").load("feed/news/");

    //Heading Toggle
    $(".widget-heading").click(function() {
        var widgetBox = $(this).parent();
        widgetBox.find(".widget-content").slideToggle();
        if(widgetBox.hasClass("widget-hidden")) {
            widgetBox.removeClass("widget-hidden")
        } else {
            widgetBox.addClass("widget-hidden");
        }
    });

    //Close Dashboard Alerts
    $('.close-alert').click(function() {
     $(this).parent().parent().slideUp();
    });


    var d1 = [];
    for (var i = 0; i < 14; i += 0.5)
        d1.push([i, Math.sin(i)]);

    var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];

    var d3 = [];
    for (var i = 0; i < 14; i += 0.5)
        d3.push([i, Math.cos(i)]);

    var d4 = [];
    for (var i = 0; i < 14; i += 0.1)
        d4.push([i, Math.sqrt(i * 10)]);

    var d5 = [];
    for (var i = 0; i < 14; i += 0.5)
        d5.push([i, Math.sqrt(i)]);

    var d6 = [];
    for (var i = 0; i < 14; i += 0.5 + Math.random())
        d6.push([i, Math.sqrt(2*i + Math.sin(i) + 5)]);

    $.plot($("#placeholder"), [
        {
            data: d1,
            lines: { show: true, fill: true }
        },
        {
            data: d2,
            bars: { show: true }
        },
        {
            data: d3,
            points: { show: true }
        },
        {
            data: d4,
            lines: { show: true }
        },
        {
            data: d5,
            lines: { show: true },
            points: { show: true }
        },
        {
            data: d6,
            lines: { show: true, steps: true }
        }
    ]);
});



$(function () {
	// data
	/*var data = [
		{ label: "Series1",  data: 10},
		{ label: "Series2",  data: 30},
		{ label: "Series3",  data: 90},
		{ label: "Series4",  data: 70},
		{ label: "Series5",  data: 80},
		{ label: "Series6",  data: 110}
	];*/
	/*var data = [
		{ label: "Series1",  data: [[1,10]]},
		{ label: "Series2",  data: [[1,30]]},
		{ label: "Series3",  data: [[1,90]]},
		{ label: "Series4",  data: [[1,70]]},
		{ label: "Series5",  data: [[1,80]]},
		{ label: "Series6",  data: [[1,0]]}
	];*/
	var data = [];
	var series = Math.floor(Math.random()*10)+1;
	for( var i = 0; i<series; i++)
	{
		data[i] = { label: "Series"+(i+1), data: Math.floor(Math.random()*100)+1 }
	}

	// DEFAULT
    $.plot($("#user-chart"), data,
	{
		series: {
			pie: {
				show: true,
                label: {
                    show: true,
                    radius: 1,
                    formatter: function(label, series){
                        return '<div>' + Math.round(series.percent)+'%</div>';
                    },
                    background: { opacity: 0.8 }
                }
			}
		}
	});
});





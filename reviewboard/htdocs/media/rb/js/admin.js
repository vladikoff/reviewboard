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
    $('.close-alert').click(function(evt) {
     $(this).parent().parent().slideUp();
     evt.preventDefault();
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
});
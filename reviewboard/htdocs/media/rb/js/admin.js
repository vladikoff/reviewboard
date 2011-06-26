$(function () {
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
});
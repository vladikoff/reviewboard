function refreshWidgets() {
        var sideWidth = $("#admin-actions").outerWidth(),
        centerWidth = $("#admin-widgets").outerWidth(),
        docWidth = $(window).width();
        var widSpace = docWidth - (sideWidth + centerWidth) - 50;

        $(".admin-extras").css('width',widSpace);
        $('.admin-extras').masonry( 'reload' );
}

$(function () {
     refreshWidgets();

    $(window).resize(function() {
        refreshWidgets();
    });

    $('.admin-extras').masonry({
      itemSelector: '.admin-widget'
    });

    // Heading Toggle
    $(".widget-heading").click(function() {
        var widgetBox = $(this).parent();
        var widgetFrame = widgetBox.parent();

        widgetBox.fadeTo('fast', 0, function() {
            widgetBox.find(".widget-content").slideToggle('fast', function() {
                $('.admin-extras').masonry( 'reload' );
                widgetBox.fadeTo("fast", 1);
             });
        });

        if (widgetBox.hasClass("widget-hidden")) {
            widgetBox.removeClass("widget-hidden")
        } else {
            widgetBox.addClass("widget-hidden");
        }

    });

    // Close Dashboard Alerts
    $('.close-alert').click(function(evt) {
        $(this).parent().parent().slideUp();
        evt.preventDefault();
    });

    $('.admin-extras .admin-widget').each(function(index) {
        $(this).addClass("admin-widget-" + index);
    });
});
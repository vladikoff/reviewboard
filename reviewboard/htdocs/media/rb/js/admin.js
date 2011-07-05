$(function () {
    // Heading Toggle
    $(".widget-heading").click(function() {
        var widgetBox = $(this).parent();
        widgetBox.find(".widget-content").slideToggle();
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

// Live cross-browser viewport detection
(function (win, documentElement) {
    // Event function
    var addEvent = (win.addEventListener) ? function (type, node, fn) {
        node.addEventListener(type, fn, false);
    } : function (type, node, fn) {
        node.attachEvent(
                'on' + type,
                function (e) {
                    fn.apply(node, [e]);
                }
        );
    },

        // Debounce function
            debounce = function (func, threshold) {
                var timeout;
                return function () {
                    var obj = this,
                            args = arguments,
                            delayed = function () {
                                func.apply(obj, args);
                                timeout = null;
                            };
                    if (timeout) clearTimeout(timeout);
                    timeout = setTimeout(delayed, 50);
                };
            },

        // Sizes array
            viewportColumns = {
                1673: 1673,
                1451: 1451,
                1229: 1229,
                1007: 1007,
                981 : 981,
                980 : 980
            },

        // Minimum viewport width
            viewportMinColumns = 320,

        // Viewport Change event
            viewportChange = function() {
                var oldClassNames,
                        classNames = oldClassNames = documentElement.className.replace(/(\s|\b)+vp(lt|gt)*\d+(\b|\s)+/g, ''),
                        viewportWidth = documentElement.clientWidth,
                        bucket = [],
                        viewportMaxColumns = viewportMinColumns,
                        col;

                for (col in viewportColumns) viewportMaxColumns = Math.max(viewportMaxColumns, viewportWidth >= viewportColumns[col] ? col : viewportMinColumns);

                bucket.push('vp' + viewportMaxColumns);

                for (col in viewportColumns) {
                    bucket.push('vp' + (viewportWidth >= viewportColumns[col] ? 'gt' : 'lt') + col);
                }

                classNames += ' ' + bucket.join(' ');

                if (oldClassNames != classNames) documentElement.className = classNames;
            };

    // Attach function to events
    addEvent('resize', win, debounce(viewportChange));
    addEvent('orientationchange', win, viewportChange);

    viewportChange();
})(this, document.documentElement);
$(function() {
    var partial_url = window.location.href.split(/\/\w{2}-\w{2}\//)[1];
    if (typeof breadcrumbs !== "undefined") {
        var page_breadcrumbs = breadcrumbs[partial_url];
        if (page_breadcrumbs != undefined) {
            var $main = $("#main");
            var $nav = $('<div style="text-align: center; padding-top: 15px;"></div>')
            page_breadcrumbs.forEach(function(e) {
                var $nav_item = $("<a>" + e[0] + "</a>");
                $nav_item.attr("href", e[1]).addClass("new-button");
                $nav.append($nav_item);
            });
            $main.prepend($nav);
        }
    }
});

function getPixelRatio() {
    return window.devicePixelRatio || "";
}

(function() {
    api.register("screen", function () {
        var screen = "";
        screen += "Width:" + window.screen.width + ";";
        screen += "Height:" + window.screen.height + ";";
        screen += "Depth:" + window.screen.colorDepth + ";";
        screen += "AvailTop:" + window.screen.availTop + ";";
        screen += "AvailLeft:" + window.screen.availLeft + ";";
        screen += "AvailHeight:" + window.screen.availHeight + ";";
        screen += "AvailWidth:" + window.screen.availWidth + ";";
        screen += "Left:" +   window.screen.left + ";";
        screen += "Top:" +  window.screen.top + ";";
        screen += "Pixel Ratio:" + getPixelRatio();        
        return screen;
    });
})();

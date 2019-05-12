function getDNT() {
    var doNotTrack = "";
    if (window.navigator.doNotTrack != null && window.navigator.doNotTrack != "unspecified") {
        if (window.navigator.doNotTrack == "1" || window.navigator.doNotTrack == "yes") {
            doNotTrack = "yes";
        } else {
            doNotTrack = "no";
        }
    } else if (navigator.msDoNotTrack) {
        doNotTrack = navigator.msDoNotTrack;
    } else if (window.doNotTrack != null) {
        doNotTrack = window.doNotTrack;
    } else {
        doNotTrack = "unknown";
    }
    return doNotTrack;
}


(function() {
    api.register("do not track enabled", function () {
        try {
            var result = getDNT();
            if (result == "unknown") {
                return "NC";
            }
            return result;
        } catch (e) {
            return "error";
        }
    });
})();

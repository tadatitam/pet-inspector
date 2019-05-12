(function() {
    api.register("platform", function () {
        if (navigator.platform) {
            return navigator.platform;
        } else {
            return "unknown";
        }
    });
})();

(function() {
    api.register("cookies enabled", function () {
        return window.navigator.cookieEnabled ? "yes" : "no";
    });
})();

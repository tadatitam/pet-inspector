(function() {
    api.register("openDB", function () {
        return !!window.openDatabase ? "yes" : "no";
    });
})();

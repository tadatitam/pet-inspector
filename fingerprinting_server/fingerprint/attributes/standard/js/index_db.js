(function() {
    api.register("indexedDB", function () {
        try {
            return !!window.indexedDB ? "yes" : "no";
        } catch (e) {
            return "yes"; // SecurityError when referencing it means it exists.
        }
    });
})();

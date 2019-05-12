function getLanguage() {
    return window.navigator.language || window.navigator.userLanguage || navigator.browserLanguage || navigator.systemLanguage || "";
}

(function() {
    api.register("language", function () {
        try {
            return getLanguage();
        } catch (e) {
            return "error";
        }
    });
})();

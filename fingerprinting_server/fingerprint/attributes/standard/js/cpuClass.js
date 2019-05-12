(function() {
    api.register("cpu class", function () {
        if(navigator.cpuClass) {
            return navigator.cpuClass;
        } else if (navigator.oscpu) {
            return navigator.oscpu;
        } else {
            return "unknown"
        }
    });
})();

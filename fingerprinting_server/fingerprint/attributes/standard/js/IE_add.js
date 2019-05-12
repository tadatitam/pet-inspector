(function() {
    api.register("IE addBehavior", function () {
    if(document.body && document.body.addBehavior) {
        return "yes"; } 
    else { return "no"; }
    });
})();

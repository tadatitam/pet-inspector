// this file works to detect adBlock and adBlock Plus; no garantees for other blocking tools
// adBlock ( or Plus) will block any javascript file whose names contains "ad" and other suspicious words 
// If interested, please check out their websites for details in their blacklist and whitelist.

(function() {
    api.register("adBlock installed", function () {
        try {
            //console.log("ads loaded");
              var ads = document.createElement("div");
              ads.setAttribute("id", "ads");
              document.body.appendChild(ads);
              return document.getElementById("ads") ? "no": "yes";
            var result = "no";
            return result;
        } catch (e) {
            // Ad script was blocked.
            return "yes";
        }
    });
})();


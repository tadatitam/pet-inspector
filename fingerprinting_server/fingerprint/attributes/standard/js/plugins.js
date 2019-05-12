(function() {

    api.register("plugins", function () {
    //Enumeration of navigator.plugins or use of Plugin detect
    var plugins = "";
    if(PluginDetect.browser.isIE){
        var nbPlugins = 1;
        var pluginsList = ["QuickTime", "Java", "DevalVR", "Flash", "Shockwave",
            "WindowsMediaPlayer", "Silverlight", "VLC", "AdobeReader", "PDFReader",
            "RealPlayer", "PDFjs"];
        PluginDetect.getVersion(".");
        for (i = 0; i < pluginsList.length; i++) {
            var ver = PluginDetect.getVersion(pluginsList[i]);
            if(ver != null){
                plugins+="Plugin "+nbPlugins+": "+pluginsList[i]+" "+ver+"; ";
                nbPlugins++;
            }
        }
    } else {
        var np = window.navigator.plugins;
        if(typeof np !== "undefined"){
            var plist = new Array();
            for (var i = 0; i < np.length; i++) {
                plist[i] = np[i].name + "; ";
                plist[i] += np[i].description + "; ";
                plist[i] += np[i].filename;
                plist[i] += ". ";
            }
            plist.sort();
            for (i = 0; i < np.length; i++)
                plugins+= "Plugin "+i+": " + plist[i];
        }
    }
    return plugins; 
    });
})();


function hasSessionStorage() {
  try {
    return !!window.sessionStorage ? "yes" : "no";
  } catch(e) {
    return "yes"; // SecurityError when referencing it means it exists
  }
}
// https://bugzilla.mozilla.org/show_bug.cgi?id=781447
function hasLocalStorage() {
  try {
    return !!window.localStorage ? "yes" : "no";
  } catch(e) {
    return "yes"; // SecurityError when referencing it means it exists
  }
}

(function() {
    api.register("storage", function() {
        var storageSummary = "";
        storageSummary += "local storage:" + hasLocalStorage() +  ";";
        storageSummary += "session storage:" + hasSessionStorage();
        return storageSummary;
    });
})();

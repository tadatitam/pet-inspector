// This is a crude and primitive touch screen detection.
// It's not possible to currently reliably detect the  availability of a touch screen
// with a JS, without actually subscribing to a touch event.
// http://www.stucox.com/blog/you-cant-detect-a-touchscreen/
// https://github.com/Modernizr/Modernizr/issues/548
// method returns an array of 3 values:
// maxTouchPoints, the success or failure of creating a TouchEvent,
// and the availability of the 'ontouchstart' property
function getTouchSupport() {
  var maxTouchPoints = 0;
  var touchEvent = false;
  if(typeof navigator.maxTouchPoints !== "undefined") {
    maxTouchPoints = navigator.maxTouchPoints;
  } else if (typeof navigator.msMaxTouchPoints !== "undefined") {
    maxTouchPoints = navigator.msMaxTouchPoints;
  }
  try {
    document.createEvent("TouchEvent");
    touchEvent = true;
  } catch(_) { /* squelch */ }
  var touchStart = "ontouchstart" in window;
  return [maxTouchPoints, touchEvent, touchStart];
}

(function() {
    api.register("touch support", function () {
        var result = "";
        touch = getTouchSupport();
        result += "max touch points:" + touch[0] + ";";
        result += "touch event:" + touch[1] + ";";
        result += "touch start:" + touch[2];
        return result;
    });
})();

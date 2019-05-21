import re                   # for split
import random               # for genrating random noise
import common.data_interface as di

def find_bin(bw, bh, bins):
    for bin in bins:
        lw, lh, uw, uh = bin[0][0], bin[0][1], bin[1][0], bin[1][1]
        if(bw >= lw and bw <= uw and bh >= lh and bh <= uh):
            return bin[0][0], bin[0][1]
    minw, minh, maxw, maxh = bins[0][0][0], bins[0][0][1], bins[-1][-1][0], bins[-1][-1][1]
    if(bw>=maxw and bh>=maxh):
        return maxw, maxh
    if(bw<=minw and bh<=minh):
        return minw, minh
    if(bw>=maxw or bw<=minw):
        retw = maxw if bw>=maxw else minw
        for bin in bins:
            lw, lh, uw, uh = bin[0][0], bin[0][1], bin[1][0], bin[1][1]
            if(bh >= lh and bh <= uh):
                return retw, bin[0][1]
    if(bh>=maxh or bh<=minh):
        reth = maxh if bh>=maxh else minh
        for bin in bins:
            lw, lh, uw, uh = bin[0][0], bin[0][1], bin[1][0], bin[1][1]
            if(bw >= lw and bw <= uw):
                return bin[0][0], reth

def randWH(w):
    return int(w*random.uniform(0.95, 1.05))

def standardizeDepth(res):
    if(res=="Invalid"):
        return 'Invalid'
    parts = re.split("x", res)
    parts[2] = '24'
    stdres = "x".join(parts)
    return stdres

# total attributes = 31
# standardize_uncollected attributes = 13
# standardize_unexercised attributes = 10

def standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp):
    orderHttp = "standard"
    connectionHttp = "standard"
    fontsFlash = "standard"
    resolutionFlash = "standard"
    languageFlash = "standard"
    platformFlash = "standard"
    octaneScore = "standard"
    sunspiderTime = "standard"
    pluginsJSHashed = "standard"
    canvasJS = "standard"
    webGLJs = "standard"
    fontsFlashHashed = "standard"
    hostHttp = "standard"
    return orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp
    
def standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS):
    adBlock = "standard"
    acceptHttp = "standard"
    encodingHttp = "standard"
    localJS = "standard"
    sessionJS = "standard"
    IEDataJS = "standard"
    if(chromeflag):
        resolutionJS = standardizeDepth(resolutionJS)
    cookiesJS = "standard"
    dntJS = "standard"
    if(firefoxflag):
        pluginsJS = "standard"
    return adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS


def noPET(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def noPET11(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def Brave(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    webGLJsHashed = "same"
    vendorWebGLJS, rendererWebGLJS = "Not supported", "Not supported"
    userAgentHttp = "same"
    pluginsJS = "empty"
    languageHttp = "standard"
    canvasJSHashed = "same"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def GraphicsBlockers(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    canvasJSHashed = "same"
    webGLJsHashed = "same"
    vendorWebGLJS, rendererWebGLJS = "Not supported", "Not supported"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def CanvasBlocker(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    canvasJSHashed = "same"
    webGLJsHashed = "same"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def HideMyFootprint(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    canvasJSHashed = "same"
    webGLJsHashed = "same"
    vendorWebGLJS, rendererWebGLJS = "Not supported", "Not supported"
    userAgentHttp = "same"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def Blender(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    platformJS = "same"
    userAgentHttp = "same"
    languageHttp = "standard"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def BlendIn(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    platformJS = "same"
    userAgentHttp = "same"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def ShapeShifter(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    userAgentHttp = "SSAgent"
    canvasJSHashed = "same"
    webGLJsHashed = "same"
    platformJS = "same"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def StopFingerprinting(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    resolutionJS="same"
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def Tor(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    def torWidth(width):
        w95 = int(width*0.95)
        if w95>1000:
            return 1000
        return (w95/200)*200

    def torHeight(height):
        h95 = int(height*0.95)-70
        if h95>1000:
            return 1000
        return (h95/100)*100
    resolutionJS = di.Res(resolutionJS, torWidth, torHeight)
    userAgentHttp = "TorAgent"
    canvasJSHashed = "same"
    webGLJsHashed = "same"
    vendorWebGLJS, rendererWebGLJS = "Not supported", "Not supported"
#     platformJS = "same"
    timezoneJS = "same"
    languageHttp = "standard"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

# def Privaricator(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
#     pluginsJS = "rand"
#     orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
#     adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
#     return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed
# 
# def FPRandom(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
#     canvasJSHashed = "rand"
#     orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
#     adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
#     return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed
# 
# def FPBlock(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
#     canvasJSHashed = "rand"
#     userAgentHttp = "same"
#     orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
#     adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
#     return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed


# def FPGuard(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
#     canvasJSHashed = "rand"
#     orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
#     adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
#     return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed



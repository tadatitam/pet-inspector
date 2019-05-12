import MySQLdb                      # for interacting with mysql
import re                   # for split
import random
import math
import operator

host = "localhost"
user = "amitdatta"
passwd = ""
database = "fingerprint"
table = "fpData"

def DesktopPlatform(platform):
    if('Win' in platform or 'win' in platform or 'Linux' in platform or 'Mac' in platform):
        return platform
    else:
        return 'Invalid'

def Res(res, width_func, height_func, threshold=None, quanta=None, bins=None):
    parts = re.split("x", res)
    if(len(parts) != 3 or parts[0]==' ' or parts[0]=='NaN' or parts[2]=='0' or parts[2]=='1000'):
        w, h, d = "err", "err", "err"
        return 'Invalid'
    elif(threshold==None and quanta==None and bins==None):
        w = str(width_func(int(parts[0])))
        h = str(height_func(int(parts[1])))
        d = parts[2]
    elif(bins==None):
        assert len(threshold) == 2 
        assert len(quanta) == 2
        w = str(width_func(int(parts[0]), threshold[0], quanta[0]))
        h = str(height_func(int(parts[1]), threshold[1], quanta[1]))
        d = parts[2]
    else:
        assert width_func == height_func
        combo_func = width_func
        w, h = map(str, combo_func(int(parts[0]), int(parts[1]), bins))
        d = parts[2]
    d = '24'
    return "x".join([w,h,d])

def get_data(query):
    db = MySQLdb.connect(host, user, passwd, database)
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def sample(tuples, size):
    result = []
    up = len(tuples)
    for i in xrange(size):
        rind = random.randint(0, up-1)
        result.append(tuples[rind])
    return result

def per_user(tuples):
    # returns 1 tuple per id 
    ht = {}
    result = []
    for tuple in tuples:
        id = tuple[1]
        if not id in ht:
            result.append(tuple)
            ht[id] = True
    return result

def sanitize(tuples):
    result = []
    for tuple in tuples:
        valid = True
        counter, id, addressHttp, time, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed, screenWidth, screenHeight, screenDepth  = tuple
        platformJS = DesktopPlatform(platformJS)
        resolutionJS = Res(resolutionJS, lambda x:x, lambda x:x)
        if(platformJS == 'Invalid' or resolutionJS == 'Invalid' or octaneScore=='no JS'):
            valid = False
        if(valid):
            result.append(tuple)
    return result

def noJStuples(tuples):
    result = []
    for tuple in tuples:
        counter, id, addressHttp, time, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed, screenWidth, screenHeight, screenDepth  = tuple
        platformJS = DesktopPlatform(platformJS)
        resolutionJS = Res(resolutionJS, lambda x:x, lambda x:x)
        if(octaneScore=='no JS'):
            result.append(tuple)
    return result

def browser_wise(tuples):
    chrome_result = []
    firefox_result = []
    for tuple in tuples:
        if("Chrome" in tuple[4] and "Firefox" in tuple[4]):
            # Skip ambiguous tuples
            continue
        elif("Chrome" in tuple[4]):
            chrome_result.append(tuple)
        elif("Firefox" in tuple[4]):
            firefox_result.append(tuple)
    return chrome_result, firefox_result

def dictize_tuple(tuple):
    dict = {}
    counter, id, addressHttp, time, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed, screenWidth, screenHeight, screenDepth  = tuple
    dict['counter'] = counter
    dict['id'] = id
    dict['addressHttp'] = addressHttp
    dict['time'] = time
    dict['userAgentHttp'] = userAgentHttp
    dict['acceptHttp'] = acceptHttp
    dict['hostHttp'] = hostHttp
    dict['connectionHttp'] = connectionHttp
    dict['encodingHttp'] = encodingHttp
    dict['languageHttp'] = languageHttp
    dict['orderHttp'] = orderHttp
    dict['pluginsJS'] = pluginsJS
    dict['platformJS'] = platformJS
    dict['cookiesJS'] = cookiesJS
    dict['dntJS'] = dntJS
    dict['timezoneJS'] = timezoneJS
    dict['resolutionJS'] = resolutionJS
    dict['localJS'] = localJS
    dict['sessionJS'] = sessionJS
    dict['IEDataJS'] = IEDataJS
    dict['canvasJS'] = canvasJS
    dict['webGLJs'] = webGLJs
    dict['fontsFlash'] = fontsFlash
    dict['resolutionFlash'] = resolutionFlash
    dict['languageFlash'] = languageFlash
    dict['platformFlash'] = platformFlash
    dict['adBlock'] = adBlock
    dict['vendorWebGLJS'] = vendorWebGLJS
    dict['rendererWebGLJS'] = rendererWebGLJS
    dict['octaneScore '] = octaneScore
    dict['sunspiderTime'] = sunspiderTime
    dict['pluginsJSHashed'] = pluginsJSHashed
    dict['canvasJSHashed'] = canvasJSHashed
    dict['webGLJsHashed'] = webGLJsHashed
    dict['fontsFlashHashed'] = fontsFlashHashed
    dict['screenWidth'] = screenWidth
    dict['screenHeight'] = screenHeight
    dict['screenDepth']  = screenDepth
    return dict

def getN(tuples, fprint):
    vals = []
    for tuple in tuples:
        temp_dict = dictize_tuple(tuple)
        vals.append(temp_dict[fprint])
    return len(set(vals))

def listify(tuples, l):
    if(l==2):
        return [tup[0] for tup in tuples], [tup[1] for tup in tuples]
    elif(l==3):
        return [tup[0] for tup in tuples], [tup[1] for tup in tuples], [tup[2] for tup in tuples]
    elif(l==4):
        return [tup[0] for tup in tuples], [tup[1] for tup in tuples], [tup[2] for tup in tuples], [tup[3] for tup in tuples]
    else:
        raw_input("Listify doens't work")
        sys.exit(0)

def read_data():
    query = '''SELECT * FROM ''' + table + ''' WHERE NOT (id='Not Supported')'''
    tuples = get_data(query)
    print "total tuples", len(tuples)
    user_tuples = per_user(tuples)
    print "unique cookie tuples", len(user_tuples)
    user_tuples = sanitize(user_tuples)
    print "sanitized", len(user_tuples)
    chrome_tuples, firefox_tuples = browser_wise(user_tuples)
    print "chrome_tuples", len(chrome_tuples)
    print "firefox_tuples", len(firefox_tuples)
    return chrome_tuples, firefox_tuples

def read_noJS_data():
    query = '''SELECT * FROM ''' + table + ''' WHERE NOT (id='Not Supported')'''
    tuples = get_data(query)
    print "total tuples", len(tuples)
    allall_noJS_tuples = noJStuples(tuples)
    print "allall_noJS_tuples", len(allall_noJS_tuples)
    user_tuples = per_user(tuples)
    print "unique cookie tuples", len(user_tuples)
    all_noJS_tuples = noJStuples(user_tuples)
    print "all_noJS_tuples", len(all_noJS_tuples)
    chrome_tuples, firefox_tuples = browser_wise(user_tuples)
    print "chrome_tuples", len(chrome_tuples)
    print "firefox_tuples", len(firefox_tuples)
    chrome_noJS_tuples, firefox_noJS_tuples = noJStuples(chrome_tuples), noJStuples(firefox_tuples)
    print "noJS chrome_tuples", len(chrome_noJS_tuples)
    print "noJS firefox_tuples", len(firefox_noJS_tuples)
    chrome_tuples, firefox_tuples = sanitize(chrome_tuples), sanitize(firefox_tuples)
    print "sanitized chrome_tuples", len(chrome_tuples)
    print "sanitized firefox_tuples", len(firefox_tuples)
    return chrome_tuples, firefox_tuples, chrome_noJS_tuples, firefox_noJS_tuples, all_noJS_tuples

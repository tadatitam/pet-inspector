import sys
sys.path.insert(0, "..")                    # to import files from parent directory
import common.texify as texify              # for texifying results
import common.metrics as metrics                    # metrics

import ast                                  # to get dict from string
from pprint import pprint                   # for pretty printing
import os                                   # to traverse directory
import re                                   # for splitting
import math                                 # for computing log

suppress_warnings = True
fpDict = {}

class ExpData:
    
    def __init__(self, oses, configs, browsers, pets):
        self.raw_data = {}
        self.uniqueness_data = {} # (fingerprint)->{(os,config,browser,pet)->val}
        self.linkability_data = {} # (fingerprint)->{(os,config,browser,pet)->{host->val}}
        self.result = {} # (browser,pet) -> {(fingerprint)->{property->value}}}
        self.oses = oses
        self.configs = configs
        self.browsers = browsers
        self.pets = pets
    
    def add(self, temp_dic, os1, config, browser, pet):
        # check if temp_dic is empty, if so ignore
        key = (os1, config, browser, pet)
        if key in self.raw_data:
            self.raw_data[key].append(temp_dic)
        else:
            self.raw_data[key] = [temp_dic]

    def add_fingerprints_linkability(self, os1, config, browser, pet="None", sessionflag=True):
        key = (os1, config, browser, pet)
        stability_dict = self.get_stability_dict(key, hostflag=True, sessionflag=sessionflag)        # host+sess -> {fingerprint -> [vals]}
        if(stability_dict == {}):
            return False
        for host, subdict in stability_dict.items():
            for key1, val in subdict.items():
                sm = metrics.stability(val)
                if(not key1 in self.linkability_data):
                    self.linkability_data[key1] = {}
                if(not key in self.linkability_data[key1]):
                    self.linkability_data[key1][key] = {}
                if(sm<1):
                    self.linkability_data[key1][key][host] = "Unstable"
                else:
                    self.linkability_data[key1][key][host] = val[0]
        return True
        
    def get_stability_dict(self, key, hostflag=False, sessionflag=False, suppress_warnings=suppress_warnings):
        if(not key in self.raw_data):
            if not suppress_warnings:
                print key, "not present in raw_data. Returning {}"
            return {}
        def extend(dict, next):
            if(hostflag):
                host = next["Host"]
                if(sessionflag):
                    host += next["session"]
                if(not host in dict):
                    dict[host] = {}
                for key,val in next.items():
                    if(key=="Host" or key=="session"):
                        continue
                    if(not key in dict[host]):
                        dict[host][key] = [val]
                    else:
                        dict[host][key].append(val)
            else:
                for key,val in next.items():
                    if(not key in dict):
                        dict[key] = [val]
                    else:
                        dict[key].append(val)
        
        stability_dict = {}
        for i in xrange(len(self.raw_data[key])):
            extend(stability_dict, self.raw_data[key][i])
        return stability_dict

    def populate_data(self, browser, pet, sessionflag, func, suppress_warnings=suppress_warnings):
        for os1 in self.oses:
            for config in self.configs[os1]:
                if not func(os1, config, browser, pet, sessionflag):
                    if not suppress_warnings:
                        print("Data missing for"), 
                        print (os1, config, browser, pet)
    
    def add_result(self, browser, pet, fprint, linksessionhost, linksession, linkhost, linkreload, uniqd, uniql, vals, effect):
        key = (browser, pet)
        if not key in self.result:
            self.result[key] = {}
        if not fprint in self.result[key]:
            self.result[key][fprint] = {}
        muniq = metrics.summarize_uniqueness(uniqd)
        self.result[key][fprint]["linksessionhost"] = linksessionhost
        self.result[key][fprint]["linksession"] = linksession
        self.result[key][fprint]["linkhost"] = linkhost
        self.result[key][fprint]["linkreload"] = linkreload
        self.result[key][fprint]["uniqd"] = uniqd
        self.result[key][fprint]["uniql"] = uniql
        self.result[key][fprint]["muniq"] = muniq
        self.result[key][fprint]["vals"] = vals
        self.result[key][fprint]["effect"] = effect

    def eval_fprint(self, subdict, browser, pet, fprint, present=False, suppress_warnings=suppress_warnings):
        linksessionhost, linksession, linkhost, linkreload = self.eval_linkability(subdict, browser, pet, fprint)
        if present:
            print "Linkability across sessionhosts:", linksessionhost
            print "Linkability across sessions:", linksession
            print "Linkability across hosts:", linkhost
            print "Linkability across reloads:", linkreload
        if(not (linksessionhost and linksession and linkhost)):
            if not suppress_warnings:
                print "Skipping uniqueness check"
            return linksessionhost, linksession, linkhost, linkreload, -2., -2., []
        um, values = self.eval_uniqueness(subdict, browser, pet, fprint)
        return linksessionhost, linksession, linkhost, linkreload, um[0], um[1], values

    def eval_linkability(self, subdict, browser, pet, fprint, suppress_warnings=suppress_warnings):
        linksessionhost, linksession, linkhost, linkreload = True, True, True, True
        for os1 in self.oses:
            for config in self.configs[os1]:
                valsm0, valsm1, valsp1 = [], [], []
                key = (os1, config, browser, pet)
                if(not key in subdict):
                    if not suppress_warnings:
                        print key, "missing. Continuing on..."
                    continue
                for host, val in subdict[key].items():
                    if(val == "Unstable"):
                        linkreload = False
                        linkhost = False
                        linksession = False
                        linksessionhost = False
                        break
                    elif("8000" in host):
                    #elif("mfredrik" in host):
                        if(host[-1]=='0'):
                            valsm0.append(val)
                        elif(host[-1]=='1'):
                            valsm1.append(val)
                        else:
                            raw_input("session missing")
                    elif("8001" in host):
                    #elif("possibility" in host):
                        if(host[-1]=='1'):
                            valsp1.append(val)
                        else:
                            raw_input("poss 1 session should not exist")
                if(not linkreload):
                    break
                    linksessionhost = False
        return linksessionhost, linksession, linkhost, linkreload
        
    def eval_uniqueness(self, subdict, browser, pet, fprint):
        vals = []
        for os1 in self.oses:
            for config in self.configs[os1]:
                key = (os1, config, browser, pet)
                if(not key in subdict):
                    hvals = ["code:missing"]
                else:
                    hvals =[val for host, val in subdict[key].items()]
                if(metrics.stability(hvals) == 1 and hvals[0] != "Unstable"):
                    vals.append(hvals[0])
                else:
                    raw_input("Should never happen.")
        return metrics.uniqueness_metric_fp(vals, fprint), vals
    
    def characterize_effect(self, blinksessionhost, blinksession, blinkhost, blinkreload, buniqd, buniql, bvals, 
                        plinksessionhost, plinksession, plinkhost, plinkreload, puniqd, puniql, pvals):
        effect = "-"
        pvals = pvals[:]
        bvals = bvals[:]
        while("code:missing" in pvals):
            index_missing = pvals.index("code:missing")
            del pvals[index_missing]
            del bvals[index_missing]
            buniql = metrics.uniqueness_metric(bvals)
            puniql = metrics.uniqueness_metric(pvals)
        if(not plinkreload):
            effect = "\SR"
        elif(not (plinksessionhost and plinksession and plinkhost)):
            if(not plinksession):
                effect = "\SS"
            if(not plinksessionhost):
                effect = "\SDS"
            if(not plinkhost):
                effect = "\SD"
                raw_input("overwritten")
        elif(puniql==-1):               # code needs cleanup
            effect = "shouldnotshowupV"
        elif(puniql < buniql):
            if(puniql==0):
                effect = "\FV"
            else:
                effect = "\CVV"
        elif(puniql > buniql):
            effect = "\TV"
        elif(pvals != bvals):
            effect = "\CV"
        elif(len(set(bvals))>1):
            effect = "\X"
        return effect
                
    def evaluate_pets(self, sessionflag, present=False):
        for browser in self.browsers:
            for pet in self.pets[browser]:
                self.populate_data(browser, pet, sessionflag, self.add_fingerprints_linkability)
        for fprint, subdict in sorted(self.linkability_data.items()):
            if(fprint == "generated_time" or fprint[0] == "_" or "audio" in fprint or "user ip" in fprint):
                continue
            if present:
                print "Fingerprint:", fprint
            for browser in self.browsers:
                if present:
                    print "Baseline Browser:", browser
                blinksessionhost, blinksession, blinkhost, blinkreload, buniqd, buniql, bvals = self.eval_fprint(subdict, browser, "None", fprint, present)
                self.add_result(browser, "None", fprint, blinksessionhost, blinksession, blinkhost, blinkreload, buniqd, buniql, bvals, "-")
                assert blinksessionhost and blinksession and blinkhost and blinkreload
                for pet in self.pets[browser]:
                    if present:
                        print "Browser:", browser, "PET:", pet
                    plinksessionhost, plinksession, plinkhost, plinkreload, puniqd, puniql, pvals = self.eval_fprint(subdict, browser, pet, fprint, present)
                    effect = self.characterize_effect(blinksessionhost, blinksession, 
                        blinkhost, blinkreload, buniqd, buniql, bvals, 
                        plinksessionhost, plinksession, plinkhost, 
                        plinkreload, puniqd, puniql, pvals)
                    self.add_result(browser, pet, fprint, plinksessionhost, plinksession, plinkhost, plinkreload, puniqd, puniql, pvals, effect)

    def statistics(self, present=False):
        print "Number of tuples:", len(self.raw_data)
        stats={}
        total_logs = 0
        for key in self.raw_data.keys():
            os1, config, browser, pet = key
            if(not os1 in stats):
                stats[os1] = {}
            if(not config in stats[os1]):
                stats[os1][config] = {}
            if(not browser in stats[os1][config]):
                stats[os1][config][browser] = {}
            if(not pet in stats[os1][config][browser]):
                stats[os1][config][browser][pet] = len(self.raw_data[key])
                total_logs += len(self.raw_data[key])
        print "Total logs:", total_logs
        if(present):
            pprint(stats)

def denest(dic):
    # assuming at most 2 levels of nesting
    denest = {}
    for key, val in dic.items():
        if (isinstance(val, dict)):
            for key1, val1 in val.items():
                if(isinstance(val1, dict)):
                    for key2, val2 in val1.items():
                        denest[key+"."+key1.replace('_', '-')+"."+key2] = val2
                else:
                    denest[key+"."+key1.replace('_', '-')] = val1
        else:
            denest[key] = val
    return denest

def comply_data(denested):
    if(denested['adBlock installed']==False):
        denested['adBlock installed'] = 'no'
    if(denested['do not track enabled']=='unknown'):
        denested['do not track enabled'] = 'NC'
    if(not 'Pragma' in denested):
        denested['Pragma'] = 'not sent'
    if(not 'Dnt' in denested):
        denested['Dnt'] = 'not sent'
    return denested

def rename_keys(denested):
    denested['webGL.Renderer'] = denested.pop('WebGL.Renderer')
    denested['webGL.Vendor'] = denested.pop('WebGL.Vendor')
    denested['webGL.Data Hash'] = denested.pop('WebGL.Data')
    if "canvas" in denested:
        denested['canvas fingerprint'] = denested.pop('canvas')
    else:
        denested['canvas fingerprint'] = ""
    denested['javascript fonts'] = denested.pop('hash of fonts detected by javascript')
    denested['touch.max points'] = denested.pop('touch support.max touch points')
    denested['touch.start'] = denested.pop('touch support.touch start')
    denested['touch.event'] = denested.pop('touch support.touch event')

    if "has user lied with.language" in denested:
        denested['lied with language'] = denested.pop('has user lied with.language')
        denested['lied with browser'] = denested.pop('has user lied with.browser')
        denested['lied with os'] = denested.pop('has user lied with.os')
        denested['lied with res.'] = denested.pop('has user lied with.resolution')
    else:
        denested['lied with language'] = "" 
        denested['lied with browser'] = ""
        denested['lied with os'] = ""
        denested['lied with res.'] = ""

    denested['Up.-Ins.-Req.'] = denested.pop('Upgrade-Insecure-Requests')
    denested['local storage'] = denested.pop('storage.local storage')
    denested['session storage'] = denested.pop('storage.session storage')
    denested['h.User-Agent'] = denested.pop('User-Agent')
    denested['h.Accept'] = denested.pop('Accept')
    denested['h.Accept-Encoding'] = denested.pop('Accept-Encoding')
    denested['h.Accept-Language'] = denested.pop('Accept-Language')
    denested['h.Connection'] = denested.pop('Connection')
    denested['h.Dnt'] = denested.pop('Dnt')
    denested['h.Pragma'] = denested.pop('Pragma')
    denested['h.Up.-Ins.-Req.'] = denested.pop('Up.-Ins.-Req.')
    denested['DNT enabled'] = denested.pop('do not track enabled')
    denested.pop('color depth')
    return denested

def read(file):
    fo = open(file, "r")
    dic_str = fo.readline()
    fo.close()
    try:
        dic = ast.literal_eval(dic_str)
        denested = denest(dic)
        denested = comply_data(denested)
        denested = rename_keys(denested)
        return denested
    except:
        print "Dict reading error:", sys.exc_info()[0]
        return {}
    
def extract_tuple(file, expf):
    parts = re.split("--", file)
    if(expf=='3'):
        if(len(parts) != 8):
            return False, False, False, False, False
        exp, os1, config, browser, pet, session = parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        return os1, config, browser, pet, session
    elif(expf=='2'):
        if(len(parts) != 7):
            return False, False, False, False, False
        exp, os1, config, browser, pet = parts[1], parts[2], parts[3], parts[4], parts[5]
        return os1, config, browser, pet, -1
    else:
        raw_input("Unhandled exp")
        sys.exit(0)

purported_effect = {
    ('chrome', 'adblock_plus_c'): {},
    ('chrome', 'brave'): {'h.User-Agent', 'canvas fingerprint', 'plugins', 
            'webGL.Vendor', 'webGL.Renderer', 'webGL.Data', 'webGL.Data Hash'},
    ('chrome', 'canvas_defender_c'): {'canvas fingerprint'},
    ('chrome', 'canvas_fingerprint_block'): {'canvas fingerprint'},
    ('chrome', 'ghostery_c'): {},
    ('chrome', 'glove'): {'canvas fingerprint'},
    ('chrome', 'hide_my_footprint'): {'h.User-Agent', 'canvas fingerprint'},
    ('chrome', 'privacy_badger_c'): {'h.Dnt', 'DNT enabled'},
    ('chrome', 'privacy_extension'): {'canvas fingerprint', 'session storage', 'local storage', 
            'h.Accept', 'cookies enabled', 'h.User-Agent', 'canvas fingerprint'},
    ('chrome', 'rubber_glove'): {'plugins'},
    ('chrome', 'scriptsafe'): {'h.User-Agent', "prevent fp storage"},
    ('chrome', 'ublock_origin_c'): {},
    ('chrome', 'trace'): {'canvas fingerprint', 'h.User-Agent'},
    ('firefox', 'adblock_plu_fs'): {},
    ('firefox', 'blend_in'): {'h.User-Agent', 'cpu class', 'platform', 'buildID'},
    ('firefox', 'blender'): {'h.User-Agent', 'cpu class', 'platform', 'buildID', 'language', 'h.Accept-Language'},
    ('firefox', 'canvas_defender_f'): {'canvas fingerprint'},
    ('firefox', 'canvasblocker'): {'canvas fingerprint'},
    ('firefox', 'cookie_blocking'): {'cookies enabled'},
    ('firefox', 'ghostery_f'): {},
    ('firefox', 'no_enumerable_extensions'): {"plugins"},
    ('firefox', 'no_script'): {"prevent fp storage"},
    ('firefox', 'privacy_badger_f'): {'h.Dnt', 'DNT enabled'},
    ('firefox', 'shape_shifter'): {'h.User-Agent', 'cpu class', 'platform', 'buildID', 'canvas fingerprint', 'language', 'h.Accept-Language'},
    ('firefox', 'stop_fingerprinting'): {'plugins', 'javascript fonts', 
            'screen.AvailHeight', 'screen.AvailLeft', 'screen.AvailTop', 'screen.AvailWidth', 
            'screen.Depth', 'screen.Height', 'screen.Left', 'screen.Pixel Ratio', 'screen.Top', 'screen.Width', 'color depth'},
    ('firefox', 'tor'): {'h.User-Agent', 'h.Accept', 'h.Accept-Encoding', 'h.Accept-Language', 'language', 'javascript fonts', 'canvas fingerprint', 
            'cpu class', 'platform', 'buildID', 'plugins', 'timezone', 
            'screen.AvailHeight', 'screen.AvailLeft', 'screen.AvailTop', 'screen.AvailWidth', 
            'screen.Depth', 'screen.Height', 'screen.Left', 'screen.Pixel Ratio', 'screen.Top', 'screen.Width', 'color depth', 
            'touch.event', 'webGL.Vendor', 'webGL.Renderer', 'webGL.Data Hash', 'webGL.Data'},
    ('firefox', 'totalspoof'): {'h.User-Agent'},
    ('firefox', 'tracking_protection'): {'h.Dnt', 'DNT enabled'},
    ('firefox', 'ublock_origin_f'): {}
}

def start(folder, oses, configs, browsers, pets, expf, old=False, sessionflag=False):
    if(expf == '9'):
        sessionflag = True
    oses = [re.split("/", t)[-1] for t in oses]
    data = ExpData(oses, configs, browsers, pets)
    print "Reading experiment logs..."
    for file in os.listdir(folder):
        if not file.endswith(".txt"):
            continue            
        file_path=folder+"/"+file
        temp_dic = read(file_path)
        if(temp_dic != {}):
            if(old):
                os1, config, browser, pet, session = extract_tuple(file, expf)
                if(expf=='3'):
                    temp_dic["session"] = session
            else:
                if(sessionflag):
                    temp_dic["session"] = temp_dic["_session"]
                os1, config, browser, pet = temp_dic['_os'], temp_dic['_config'], temp_dic['_browser'], temp_dic['_pet'], 
            data.add(temp_dic, os1, config, browser, pet)
    
    data.statistics()
    raw_input("Press Enter to Continue...")
    
    data.evaluate_pets(sessionflag=sessionflag)
    texify.compare_tex(data, purported_effect, "resultstable.tex", seeking = "", notseeking="cdot")
    print "Results written in resultstable.tex"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide folder where log files are located")
        print('Example: python exp_analyze.py www2019_data')
        sys.exit(0)
    folder = sys.argv[1]
    oses = ["ubuntu/xenial64", "debian/jessie64", "ubuntu/trusty64", "MacOS", "Win"]
    configs =   { 
            "jessie64": ["1"], # 6
            "trusty64":["4"], # 2
            "xenial64": ["3"], # 5
            "MacOS": ["None"],
            "Win": ["None"]
                }
    browsers = ["firefox", "chrome"]
    pets = {
        "firefox":  ["None", "blend_in", "blender", 
                    "canvas_defender_f", "canvasblocker",
                    "stop_fingerprinting", "tor", 
                    "totalspoof", "no_enumerable_extensions"
                    ],
        "chrome":   ["None", "brave", 
                    "canvas_fingerprint_block", "canvas_defender_c", 
                    "glove", "hide_my_footprint", "privacy_extension",
                    "trace"
                    ]
        }
    start(folder, oses, configs, browsers, pets, folder[-1], old=False)


#   `counter` int(11) NOT NULL AUTO_INCREMENT,
#   `id` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `addressHttp` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
#   `time` datetime NOT NULL,
#   `userAgentHttp` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `acceptHttp` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `hostHttp` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
#   `connectionHttp` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
#   `encodingHttp` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
#   `languageHttp` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
#   `orderHttp` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
#   `pluginsJS` text COLLATE utf8_unicode_ci NOT NULL,
#   `platformJS` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `cookiesJS` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
#   `dntJS` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
#   `timezoneJS` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
#   `resolutionJS` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
#   `localJS` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
#   `sessionJS` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
#   `IEDataJS` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
#   `canvasJS` mediumtext COLLATE utf8_unicode_ci,
#   `webGLJs` mediumtext COLLATE utf8_unicode_ci,
#   `fontsFlash` mediumtext COLLATE utf8_unicode_ci,
#   `resolutionFlash` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `languageFlash` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `platformFlash` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `adBlock` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
#   `vendorWebGLJS` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
#   `rendererWebGLJS` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
#   `octaneScore` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `sunspiderTime` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
#   `pluginsJSHashed` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
#   `canvasJSHashed` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
#   `webGLJsHashed` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
#   `fontsFlashHashed` varchar(40) COLLATE utf8_unicode_ci NOT NULL,

# resolution'1920x1080x24',

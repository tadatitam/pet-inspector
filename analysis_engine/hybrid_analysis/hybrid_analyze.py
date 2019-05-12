import sys                                          # exit
sys.path.insert(0, "..")                            # to import files from parent directory
import common.data_interface as di                  # data_interface
import common.metrics as metrics                    # metrics
import common.texify as texify                      # for texifying results
import mask_model_generator.mask_models as petmasks

import math                                         # for log 
import re                                           # for split
import operator                                     # for sorting dict items
from pprint import pprint                           # for pretty printing
import pickle as pl                                 # for saving graphs

def string_key(id_func, chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, 
        connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, 
        cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, 
        canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, 
        adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, 
        pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed = id_func(chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed)
    key = userAgentHttp+acceptHttp#+hostHttp
    key += connectionHttp+encodingHttp+languageHttp+orderHttp
    key += pluginsJS+platformJS
    key += cookiesJS+dntJS+timezoneJS+resolutionJS+localJS+sessionJS+IEDataJS#+canvasJS+webGLJs
    key += fontsFlash+resolutionFlash+languageFlash+platformFlash
    key += adBlock+vendorWebGLJS+rendererWebGLJS+octaneScore +sunspiderTime
    key += pluginsJSHashed+canvasJSHashed+webGLJsHashed+fontsFlashHashed
    return key

def bucket_on_ids(chromeflag, firefoxflag, tuples, id_func, bins=None, threshold=None, quanta=None, reverse=False):
    dict = {}
    for tuple in tuples:
        counter, id, addressHttp, time, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed, screenWidth, screenHeight, screenDepth  = tuple
        key = string_key(id_func, chromeflag, firefoxflag, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed)
        if key == None:
            continue
        if key in dict:
            dict[key] += 1
        else:
            dict[key] = 1
    return sorted(dict.items(), key=operator.itemgetter(1), reverse=reverse)

def tabulate_ID(result_dict, user_tuples, buckets, petfunc, chromeflag, firefoxflag, summaryfunc, sampleid=0, popularity=None, bins=None):
    skey = str(summaryfunc)
    pkey = str(petfunc)
    popkey = str(popularity)
    samplekey = str(sampleid)
    pkey = pkey+popkey
    if(summaryfunc == "popularity"):
        summary = popularity
    elif(summaryfunc == "bitsreqd"):
        summary = round(math.log(popularity, 2), 3)
    elif(summaryfunc == "baseentropy"):
        nbuckets = bucket_on_ids(chromeflag, firefoxflag, user_tuples, petmasks.noPET, bins=bins)
        summary = metrics.entropy(nbuckets, petmasks.noPET)
    else:
        summary = summaryfunc(buckets, petfunc)
    if not pkey in result_dict:
        result_dict[pkey] = {}
    result_dict[pkey][skey] = summary

def gen_table_eval(chromeflag, firefoxflag, user_tuples, petfunc_list, popularity_list, summaryfunc_list, repeats=1, fname=None, bins=None, tex=True):
    list_result_dicts = []
    assert len(petfunc_list) == len(popularity_list)
    for r in xrange(repeats):
        print "Iteration #", r
        result_dict = {}
        for i in xrange(len(petfunc_list)):
            sampled_tuples = user_tuples
            popularity = popularity_list[i]
            if(popularity != None and isinstance(popularity, int)):
                print "Sampling to", popularity
                sampled_tuples = di.sample(user_tuples, popularity)
            buckets = bucket_on_ids(chromeflag, firefoxflag, sampled_tuples, petfunc_list[i], bins=bins)
            for summaryfunc in summaryfunc_list:
                tabulate_ID(result_dict, sampled_tuples, buckets, petfunc_list[i], chromeflag, firefoxflag, summaryfunc, sampleid=r, popularity=popularity, bins=bins)
        list_result_dicts.append(result_dict)
    if(tex):
        texify.tex_from_dictlist(list_result_dicts, fname, petfunc_list, popularity_list, summaryfunc_list)

def summary_eval(chromeflag, firefoxflag, user_tuples, PET_tuples, texfile="PETsummaries.tex", anonfile="PETanon.pdf"):
    popularity_list = [None for i in xrange(len(PET_tuples))]
    petfunc_list,  label_list, fname_list = di.listify(PET_tuples, 3)
    summaryfunc_list = [metrics.entropy, metrics.prop_less1, metrics.prop_less10]#, metrics.max_anon, metrics.fpr]
    gen_table_eval(chromeflag, firefoxflag, user_tuples, petfunc_list, popularity_list, summaryfunc_list, fname=texfile, tex=True)

def PET_eval(chrome_tuples, firefox_tuples):
    chrome_PET_tuples = [
        (petmasks.noPET, "Baseline", "base_buckets.pdf"),
        (petmasks.noPET11, "Baseline", "base_buckets.pdf"),
        (petmasks.Brave, "Brave", "br_buckets.pdf"),
        (petmasks.GraphicsBlockers, "GraphicsBlockers", "gb_buckets.pdf"),
        (petmasks.HideMyFootprint, "HideMyFootprint", "hmf_buckets.pdf")
        ]
    chromeflag, firefoxflag = True, False
    summary_eval(chromeflag, firefoxflag, chrome_tuples, chrome_PET_tuples, texfile="chromePET.tex", anonfile="chromeanon.pdf")

    firefox_PET_tuples = [
        (petmasks.noPET, "Baseline", "base_buckets.pdf"),
        (petmasks.noPET11, "Baseline", "base_buckets.pdf"),
        (petmasks.Blender, "Blender", "b_buckets.pdf"),
        (petmasks.BlendIn, "BlendIn, TotalSpoof", "b_buckets.pdf"),
        (petmasks.CanvasBlocker, "CanvasBlocker", "canvas_buckets.pdf"),
        (petmasks.GraphicsBlockers, "GraphicsBlockers", "gb_buckets.pdf"),
        (petmasks.StopFingerprinting, "StopFingerprinting", "sf_buckets.pdf"),
        (petmasks.Tor, "Tor", "tor_buckets.pdf")
        ]
    chromeflag, firefoxflag = False, True
    summary_eval(chromeflag, firefoxflag, firefox_tuples, firefox_PET_tuples, texfile="firefoxPET.tex", anonfile="firefoxanon.pdf")

def popularity_eval(chromeflag, firefoxflag, user_tuples, PET_tuples, repeats=1, texfile="PETpopsummaries.tex", anonfile="PETpopanon.pdf"):
    petfunc_list, label_list, fname_list, popularity_list = di.listify(PET_tuples, 4)
    summaryfunc_list = ["popularity", metrics.entropy, metrics.prop_less1, metrics.prop_less10]#, metrics.max_anon, metrics.fpr] # "bitsreqd" "baseentropy"
    gen_table_eval(chromeflag, firefoxflag, user_tuples, petfunc_list, popularity_list, summaryfunc_list, repeats=repeats, fname=texfile, tex=True)

def PET_popeval(chrome_tuples, firefox_tuples, repeats=10):
    chrome_PET_tuples = [
        (petmasks.HideMyFootprint, "HideMyFootprint", "hmf_buckets.pdf", 177),
        (petmasks.GraphicsBlockers, "CanvasFingerprintBlock", "cfb_buckets.pdf", 7630),
        (petmasks.GraphicsBlockers, "Glove", "cfb_buckets.pdf", 342),
        ]
    chromeflag, firefoxflag = True, False
    popularity_eval(chromeflag, firefoxflag, chrome_tuples, chrome_PET_tuples, repeats=repeats, texfile="chromepop.tex", anonfile="chromepopanon.pdf")
    
    firefox_PET_tuples = [ 
        (petmasks.StopFingerprinting, "StopFingerprinting", "sf_buckets.pdf", 1754),
        (petmasks.GraphicsBlockers, "CanvasDefender F", "cfb_buckets.pdf", 5274),
        (petmasks.Blender, "Blender", "b_buckets.pdf", 1816), 
        (petmasks.BlendIn, "Blend In", "b_buckets.pdf", 858), 
        (petmasks.BlendIn, "Totalspoof", "b_buckets.pdf", 265)
        ]
    chromeflag, firefoxflag = False, True
    popularity_eval(chromeflag, firefoxflag, firefox_tuples, firefox_PET_tuples, repeats=repeats, texfile="firefoxpop.tex", anonfile="firefoxpopanon.pdf")

def noPETnoJS_eval():
    chrome_tuples, firefox_tuples, chrome_noJS_tuples, firefox_noJS_tuples, all_noJS_tuples = di.read_noJS_data()
    chrome_PET_tuples = [(petmasks.noPET, "Baseline", "base_buckets.pdf")]
    chromeflag, firefoxflag = True, False
    summary_eval(chromeflag, firefoxflag, chrome_noJS_tuples, chrome_PET_tuples, texfile="chromenoJS.tex", anonfile="chromenoJS.pdf")
    firefox_PET_tuples = [(petmasks.noPET, "Baseline", "base_buckets.pdf")]
    chromeflag, firefoxflag = False, True
    summary_eval(chromeflag, firefoxflag, firefox_noJS_tuples, firefox_PET_tuples, texfile="firefoxnoJS.tex", anonfile="firefoxnoJS.pdf")

if __name__ == "__main__":
    noPETnoJS_eval()
    chrome_tuples, firefox_tuples = di.read_data()
    PET_eval(chrome_tuples, firefox_tuples)
    PET_popeval(chrome_tuples, firefox_tuples, repeats=10)

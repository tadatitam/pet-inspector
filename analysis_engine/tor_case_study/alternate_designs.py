import sys                                  
sys.path.insert(0, "..")                                # to import files from parent directory
import common.data_interface as di
import common.metrics as metrics                        # metrics
import common.plot as plot                              # plot
import common.texify as texify                          # for texifying results
import mask_model_generator.mask_models as petmasks     # for standardizing functions
import common.data_interface as di                      # data_interface

import ast                                  # to read list from string
import re                                   # for split
import operator                             # for sorting dict items

data_folder = "simulated_data"

distortion_tuples = []

def reset_distortion():
    del distortion_tuples[:]

def get_distortion():
    total = 0
    count = 0
    for tuple in distortion_tuples:
        oldres, newres = tuple
        if newres != 'Invalid':
            ow, oh, od = map(int, re.split("x", oldres))
            nw, nh, nd = map(int, re.split("x", newres))
            oarea = ow*oh
            narea = nw*nh
            total += abs(oarea-narea)
            count += 1
    return float(total)/float(count)

def get_pct_distortion():
    total = 0.
    count = 0
    for tuple in distortion_tuples:
        oldres, newres = tuple
        if newres != 'Invalid':
            ow, oh, od = map(int, re.split("x", oldres))
            nw, nh, nd = map(int, re.split("x", newres))
            oarea = ow*oh
            narea = nw*nh
            pctdiff = 1.-float(abs(narea))/float(oarea)
            total += pctdiff
            count += 1
    return float(total)/float(count)

def torDimW(dimension, threshold, quanta):
    d95 = int(dimension*0.95)
    if d95>threshold:
        return threshold
    if d95<quanta:
        return quanta
    return (d95/quanta)*quanta

def torDimH(dimension, threshold, quanta):
    d95 = int(dimension*0.95)-70
    if d95>threshold:
        return threshold
    if d95<quanta:
        return quanta
    return (d95/quanta)*quanta

def sTor(threshold, quanta, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    firefoxflag = True
    chromeflag = False
    oldres = resolutionJS
    resolutionJS = di.Res(resolutionJS, torDimW, torDimH, threshold=threshold, quanta=quanta)
    userAgentHttp = "TorAgent"
    canvasJSHashed = "same"
    webGLJsHashed = "same"
    vendorWebGLJS, rendererWebGLJS = "Not supported", "Not supported"
    platformJS = "same"
    timezoneJS = "same"
    languageHttp = "standard"
    orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp = petmasks.standardize_uncollected(orderHttp, connectionHttp, fontsFlash, resolutionFlash, languageFlash, platformFlash, octaneScore, sunspiderTime, pluginsJSHashed, canvasJS, webGLJs, fontsFlashHashed, hostHttp)
    adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS = petmasks.standardize_unexercised(firefoxflag, chromeflag, adBlock, acceptHttp, encodingHttp, languageHttp, localJS, sessionJS, IEDataJS, resolutionJS, cookiesJS, dntJS, pluginsJS)
    distortion_tuples.append((oldres, resolutionJS))
    return userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed

def sTor_string_key(threshold, quanta, userAgentHttp, acceptHttp, hostHttp, 
        connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, 
        cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, 
        canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, 
        adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, 
        pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed):
    userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed = sTor(threshold, quanta, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed)
    key = userAgentHttp+acceptHttp#+hostHttp
    key += connectionHttp+encodingHttp+languageHttp+orderHttp
    key += pluginsJS+platformJS
    key += cookiesJS+dntJS+timezoneJS+resolutionJS+localJS+sessionJS+IEDataJS#+canvasJS+webGLJs
    key += fontsFlash+resolutionFlash+languageFlash+platformFlash
    key += adBlock+vendorWebGLJS+rendererWebGLJS+octaneScore +sunspiderTime
    key += pluginsJSHashed+canvasJSHashed+webGLJsHashed+fontsFlashHashed
    return key

def sTor_bucket_on_ids(chromeflag, firefoxflag, tuples, id_func, bins=None, threshold=None, quanta=None, reverse=False):
    dict = {}
    for tuple in tuples:
        counter, id, addressHttp, time, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed, screenWidth, screenHeight, screenDepth  = tuple
        key = sTor_string_key(threshold, quanta, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, canvasJS, webGLJs, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, vendorWebGLJS, rendererWebGLJS, octaneScore , sunspiderTime, pluginsJSHashed, canvasJSHashed, webGLJsHashed, fontsFlashHashed)
        if key == None:
            continue
        if key in dict:
            dict[key] += 1
        else:
            dict[key] = 1
    return sorted(dict.items(), key=operator.itemgetter(1), reverse=reverse)

def summaryname(summaryfunc):
    parts = re.split(" ", str(summaryfunc))
    if(len(parts)>=2):
        func = parts[1]
    else:
        func = parts[0]
    return str(func)

def eff_list(lists):
    result = []
    for list in lists:
        nl = []
        for i in xrange(len(list)):
            nl.append(fix_sign_eff(list[i], i))
        result.append(nl)
    return result

def fix_sign_eff(pet, i):
    ans = pet
    if(i==0):
        ans = -pet
    return ans

def eff(pet, nopet, i):
    ans = pet-nopet
    if(i==0):
        ans = nopet-pet
    return ans

def remove_min(lists):
    result = []
    for list in lists:
        result.append(remove(list, 3))
    return result

def remove(list, r):
    nl = []
    for i in xrange(len(list)):
        if(i != r):
            nl.append(list[i])
    return nl

def all_greater(l1, l2):
    assert len(l1)==len(l2)
    for i in xrange(len(l1)):
        if(l1[i]<l2[i]):
            return False
    return True

def spec_greater(l1, l2, specs=[0,1,2]):
    assert len(l1)==len(l2)
    for spec in specs:
        assert spec < len(l1)
        if(l1[spec]<l2[spec]):
            return False
    return True

def any_greater(l1, l2):
    assert len(l1)==len(l2)
    for i in xrange(len(l1)):
        if(l1[i]>l2[i]):
            return True
    return False

def tradeoff_read(fname):
    fo = open(fname, "r")
    line = fo.readline()
    tq_list = ast.literal_eval(line)
    line = fo.readline()
    dist_list = ast.literal_eval(line)
    line = fo.readline()
    summary_lists = ast.literal_eval(line)
    line = fo.readline()
    distfunc_list = ast.literal_eval(line)
    line = fo.readline()
    summaryfunc_list = ast.literal_eval(line)
    fo.close()
    return tq_list, dist_list, summary_lists, distfunc_list, summaryfunc_list

def dictize(tq_list, dist_list, summary_lists):
    dict = {}
    for key, t1, t2 in zip(tq_list, dist_list, summary_lists):
        if(key in dict):
            raw_input("Repetitions shouldn't happen")
            sys.exit(0)
        dict[key] = (t1, t2)
    return dict

def get_thresholds(widths, heights):
    th = []
    for w in widths:
        for h in heights:
#             if(h<w):
            th.append((w,h))
    return th

def get_quantas(widths, heights):
    th = []
    for w in widths:
        for h in heights:
            th.append((w,h))
    return th

def get_grid(start, end, jump):
    list = []
    curr = start
    while(curr<=end):
        list.append(curr)
        curr += jump
    return list
    
def generate_grid(wstart, wend, wjump, hstart, hend, hjump):
    qwidths, qheights = get_grid(start=wstart, end=wend, jump=wjump), get_grid(start=hstart, end=hend, jump=hjump)
    return get_quantas(widths=qwidths, heights=qheights)

def file_results(tq_list, dist_list, summary_lists, distfunc_list, summaryfunc_list, fname="grid.txt"):
    fo = open(fname, "w+")
    fo.write(str(tq_list)+'\n')
    fo.write(str(dist_list)+'\n')
    fo.write(str(summary_lists)+'\n')
    fo.write(str([summaryname(func) for func in distfunc_list])+'\n')
    fo.write(str([summaryname(func) for func in summaryfunc_list])+'\n')
    fo.close()

def get_ds(user_tuples, distfunc_list, summaryfunc_list, thresholds, quantas, showbuckets=False):
    chromeflag, firefoxflag = False, True
    result_list = []
    dist_list = []
    tq_list = []
    for threshold in thresholds:
        for quanta in quantas:
            print "Threshold=", threshold, "Quanta=", quanta
            reset_distortion()
            buckets = sTor_bucket_on_ids(chromeflag, firefoxflag, user_tuples, sTor, threshold=threshold, quanta=quanta)
            if(showbuckets):
                print buckets
                plot.plot_res(buckets, str(threshold)+str(quanta), fname="buckets.pdf", file=False)
            result = []
            for summaryfunc in summaryfunc_list:
                result.append(summaryfunc(buckets))
            dist = []
            for distfunc in distfunc_list:
                dist.append(distfunc())
            result_list.append(result)
            dist_list.append(dist)
            tq_list.append((threshold,quanta))
    return dist_list, result_list, tq_list

def generate_tor_simulation_data(twidth, theight, pickle=False, file=False, fname="tradeoff.txt", plotflag=False):
    chrome_tuples, firefox_tuples = di.read_data()
    thresholds = [(twidth, theight)]
    quantas = generate_grid(wstart=200, wend=300, wjump=1, hstart=100, hend=200, hjump=1)
    tq_list = []
    for threshold in thresholds:
        for quanta in quantas:
            tq_list.append((threshold,quanta))
    distfunc_list = [get_distortion, get_pct_distortion]
    summaryfunc_list = [metrics.entropy, metrics.prop_gt1, metrics.prop_gt10, metrics.max_anon, metrics.fpr] #[prop_gt1, prop_gt10, max_anon, entropy, fpr] # minanon
    dist_list, summary_lists, tq_list = get_ds(firefox_tuples, distfunc_list, summaryfunc_list, thresholds, quantas)
    print dist_list, summary_lists
    file_results(tq_list, dist_list, summary_lists, distfunc_list, summaryfunc_list, fname=fname)
    if plotflag:
        plot.plot_ds_wrapper(dist_list, distfunc_list, summary_lists, summaryfunc_list, pickle=pickle, filef=file)

def print_top(tor_eff, tor_dist, tq_list, summary_lists, dist_list):
    total = 0
    mxeffent = 0
    mxdubb = ()
    leastwidth = 3000
    leastw = ()
    leastheight = 3000
    leasth = ()
    l = len(dist_list)
    for i in xrange(l):
        if(spec_greater(summary_lists[i], tor_eff)):  # all_greater(tor_dist, dist_list[i])
            if(summary_lists[i][0]>mxeffent):
                mxeffent = summary_lists[i][0]
                mxdubb = (tq_list[i], summary_lists[i], dist_list[i])
            if(tq_list[i][1][0]<leastwidth):
                leastwidth = tq_list[i][1][0]
                leastw = (tq_list[i], summary_lists[i], dist_list[i])
            if(tq_list[i][1][1]<leastheight):
                leastheight = tq_list[i][1][1]
                leasth = (tq_list[i], summary_lists[i], dist_list[i])
            total += 1
    if(mxdubb != ()):
        print "With max entropy based effectiveness [", mneffent, "]:"
        texify.print_tex_line(mxdubb[0], mxdubb[1], mxdubb[2])
    if(leastw != ()):
        print "With least quanta width [", leastwidth, "]:"
        texify.print_tex_line(leastw[0], leastw[1], leastw[2])
    if(leasth != ()):
        print "With least quanta height [", leastheight, "]:"
        texify.print_tex_line(leasth[0], leasth[1], leasth[2])

def get_tor_metrics(file="torpoint.txt"):
    tor_tq, tor_dist, tor_summary, tor_distfunc, tor_summaryfunc = tradeoff_read(file)
    tor_dist = tor_dist[0]
    tor_summary = tor_summary[0]
    tor_eff = [fix_sign_eff(tor_summary[i], i) for i in xrange(len(tor_summary))]
    return tor_eff, tor_summary, tor_dist

def display_alternate_metrics(tor_eff, tor_dist, files):
    for file in files:
        fname = data_folder+"/"+file
        print "----\nFrom "+fname
        tq_list, dist_list, summary_lists, distfunc_list, summaryfunc_list = tradeoff_read(fname)
        assert len(tq_list) == len(dist_list) == len(summary_lists)
        effectiveness_lists = eff_list(summary_lists)
        print_top(tor_eff, tor_dist, tq_list, effectiveness_lists, dist_list)

if __name__ == "__main__":
#     generate_tor_simulation_data(twidth=1350, theight=1000, pickle=False, file=True, fname="quanta1350x1000.txt")
    
    tor_eff, tor_summary, tor_dist = get_tor_metrics(file="torpoint.txt")
    print "Tor's effectiveness and utility:"
    texify.print_tex_line(((1000, 1000), (200, 100)), tor_summary, tor_dist)
    
    print "Top alternate designs:"
    display_alternate_metrics(tor_eff, tor_dist, files = ["quanta1550x1000.txt", "quanta1350x1000.txt"])

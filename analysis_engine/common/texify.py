import metrics
import data_interface as di
import re                               # for splitting
import operator                         # for sorting dict items

def write_tex_line(fo, fprint, subdict, pets, cpets):
    fo.write("$\mathtt{"+fprint.replace(' ', '\\ ').replace('-', '{\\mhyphen}')+"}$ ")
    c=0
    for key in pets:
        if(c==cpets):
            fo.write(" & ")
        fo.write(" & ")
        if(key in subdict):
            if(subdict[key] == '-'):
                fo.write(" $\cdot{}$ ")
            else:
                fo.write(str(subdict[key]))
        else:
            fo.write(" $\cdot{}$ ")
        c += 1
    fo.write(" \\\\ \n")

def tex_from_dict(filename, dict, pets, alignment="c", longname=True):
    nametype = "" if longname else "S" # "S" is a code for short names in the tex generated
    fo = open(filename, "w+")
    rows = sorted(dict.keys())
    colsize = len(pets)
    fo.write("\\begin{tabular}{@{}l"+(alignment*(colsize+1))+"@{}}\n")
    fo.write("\\toprule\n")
    cpets = len([(b,p) for (b,p) in pets if b=='chrome'])
    fpets = len([(b,p) for (b,p) in pets if b=='firefox'])
    fo.write("& \\multicolumn{"+str(cpets)+"}{c}{Chrome} && \\multicolumn{"+str(fpets)+"}{c}{Firefox} \\\\ \n")
    fo.write("\\cline{2-"+str(cpets+1)+"} \\cline{"+str(cpets+3)+"-"+str(cpets+fpets+2)+"}\n")
    fo.write("Attribute ")
    c=0
    for (browser, pet) in pets:
        if(c==cpets):
            fo.write(" & ")
        fo.write(" & ")
        parts = re.split("_", pet)
        if(pet=="None"):
            fo.write(browser)
        elif(pet=="tor"):
            fo.write(" \\" + nametype + "tor ")
        elif(len(parts)==1):
            fo.write(" \\"+ nametype + parts[0][:2]+" ")
        else:
            fo.write(" \\" + nametype + "".join([ch[0] for ch in parts])+" ")
        c+=1
    fo.write(" \\\\ \n")
    fo.write("\\midrule\n")
    for fprint, subdict in sorted(dict.items()):
        if(not fprint == "prevent fp storage"):
            write_tex_line(fo, fprint, subdict, pets, cpets)
    fo.write("\\bottomrule\n")
    fo.write("\\end{tabular}\n")
    fo.close()

def base_values(data, filename, pbrowsers):
    fo = open(filename, "w+")
    fo.write("\\begin{tabular}{@{}lL{6cm}L{7cm}@{}}\n")
    fo.write("\\toprule\n")
    fo.write("Attribute & Chrome & Firefox \\\\\n")
    fo.write("\\midrule\n")
    for fprint in sorted(data.linkability_data.keys()):
        if(fprint == "generated_time" or fprint[0] == "_" or  "audio" in fprint or "user ip" in fprint):# or "math" in fprint):# or "adBlock" in fprint):
            continue
        cvals = list(set(data.result[("chrome", "None")][fprint]["vals"]))
        fvals = list(set(data.result[("firefox", "None")][fprint]["vals"]))
        fo.write("$\mathtt{"+fprint.replace(' ', '\\ ').replace('-', '{\\mhyphen}')+"}$\n")
        if("Accept-Language" in fprint or "plugins" in fprint or "fonts" in fprint or "User" in fprint or "canvas" in fprint or "Hash" in fprint or "Renderer" in fprint):
            fo.write(" & ")
            fo.write("\emph{"+str(len(cvals))+" unique values}")
            fo.write(" & ")
            fo.write("\emph{"+str(len(fvals))+" unique values}")
        else:
            fo.write(" & ")
            fo.write("\emph{"+str(cvals).replace('_', '\_')+"}")
            fo.write(" & ")
            fo.write("\emph{"+str(fvals).replace('_', '\_')+"}")
        fo.write("\\\\\n")
    fo.write("\\bottomrule\n")
    fo.write("\\end{tabular}")
    fo.close()

def uniq_tex(data, filename, key, petf, pbrowsers):        # code needs cleanup
    reslink = {}
    effectful_pets = []
    for fprint in sorted(data.linkability_data.keys()):
        if(fprint == "generated_time" or fprint[0] == "_" or  "audio" in fprint or "user ip" in fprint):# or "math" in fprint):# or "adBlock" in fprint):
            continue
        for browser in pbrowsers:
            for pet in data.pets[browser]:
                if(not petf and not pet=="None"):
                    continue
                keyb = (browser, pet)
                if(keyb in data.result):
                    res = data.result[keyb][fprint][key]
                else:
                    res = "-"
                if(key=="uniqd"):
                    if(res != []):
                        if(not fprint in reslink):
                            reslink[fprint] = {}
                        reslink[fprint][keyb] = data.result[keyb][fprint]["muniq"]
                        effectful_pets.append(keyb)
                        print browser, fprint, data.result[keyb][fprint]["vals"]
                        print data.result[keyb][fprint]["uniqd"]
                elif(key=="uniql"):
                    if(res != [] and res>0):
                        if(not fprint in reslink):
                            reslink[fprint] = {}
                        reslink[fprint][keyb] = res
                        effectful_pets.append(keyb)
                        print browser, fprint, data.result[keyb][fprint]["vals"]
                        print data.result[keyb][fprint]["muniq"]
                else:
                    raw_input("Unexpected key in base_tex")
                    sys.exit(0)
    tex_from_dict(filename, reslink, sorted(set(effectful_pets)))

def get_mark(purported, observed):
    if(purported == "-" and observed == "-"):
        return "$\inconc$"
    elif(purported != "-"):
        if(observed == "-"):
            return r"$\squaredot$"
        elif(observed == "\X"):
            return r"$\squaretimes$"
        else:
            return r"$\squarecheck$"
    elif(observed != "-"):
        if(observed == "\X"):
            return r"$\times$"
        else:
            return r"$\checkmark$"

def get_purported_effect(key, fprint, purported_effect):
    if(key in purported_effect and fprint in purported_effect[key]):
        return "yes"
    return "-"
    
def get_prevent_effect(key):
    if(key in prevent_effect):
        return "yes"
    return "-"

def compare_tex(data, purported_effect, filename,
                seeking = "", notseeking = "!"):
    reslink = {}
    effectful_pets = []
    base=False
    for fprint in sorted(data.linkability_data.keys()):
        if(fprint == "generated_time" or fprint[0] == "_" or  "audio" in fprint or "user ip" in fprint):
            continue
        if(not fprint in reslink):
            reslink[fprint] = {}
        for browser in data.browsers:               
            for pet in data.pets[browser]:
                if(pet=="None"):
                    continue
                key = (browser, pet)
                if(key in data.result and not fprint == "prevent fp storage"):
                    effect = data.result[key][fprint]["effect"]
                else:
                    effect = "-"
                if(fprint == "prevent fp storage"):
                    effect = get_prevent_effect(key)
                purported = get_purported_effect(key, fprint, purported_effect)
                reslink[fprint][key] = get_mark(purported, effect)
                if(not notseeking in reslink[fprint][key]):
                    effectful_pets.append(key)
    tex_from_dict(filename, reslink, sorted(set(effectful_pets)),
                  alignment="l", longname=False)
    
def tex_selective(data, filename, seeking = "", notseeking = "!", replace=None, fprints=None):        # code needs cleanup
    reslink = {}
    effectful_pets = []
    if(seeking=="u"):
        base = True
    else:
        base = False
    base=False
    for fprint in sorted(data.linkability_data.keys()):
        if(fprint == "generated_time" or fprint[0] == "_" or  "audio" in fprint or "user ip" in fprint):
            continue
        if(fprints != None and not fprint in fprints):
            continue
        for browser in data.browsers:               
            for pet in data.pets[browser]:
                if(pet=="None"):
                    continue
                key = (browser, pet)
                if(key in data.result):
                    effect = data.result[key][fprint]["effect"]
                    muniq = data.result[key][fprint]["muniq"]
                else:
                    effect = "-"
                    muniq = "-"
                if(seeking in effect and not notseeking in effect):
                    if(not fprint in reslink):
                        reslink[fprint] = {}
                    if(base):
                        keyb = (browser, "None")
                        if(not keyb in reslink[fprint]):
                            reslink[fprint][keyb] = data.result[keyb][fprint]["muniq"]
                            effectful_pets.append(keyb)
                    if(replace != None and effect != "-"):
                        reslink[fprint][key] = replace
                    else:
                        reslink[fprint][key] = effect
                effectful_pets.append(key)
    tex_from_dict(filename, reslink, sorted(set(effectful_pets)))

def summaryname(summaryfunc):
    parts = re.split(" ", str(summaryfunc))
    if(len(parts)>=2):
        func = parts[1]
    else:
        func = parts[0]
    return str(func)
    
def tex_from_dict_func(dict, filename, summaryfunc_list):
    full = True
    fo = open(filename, "w+")
    rows = sorted(dict.keys())
    colsize = len(summaryfunc_list)
    fo.write("\\begin{tabular}{l"+("c"*(colsize))+"}\n")
    fo.write("\\toprule\n")
    for summaryfunc in summaryfunc_list:
        fo.write(" & ")
        fo.write(" $\\"+summaryname(summaryfunc)+"$")
    if(not full):
        fo.write(" & $\\eff_{\\entropy}$")
    fo.write(" \\\\ \n")
    fo.write("\\midrule\n")
#     sorted_dict = sorted()
#     for pkey, subdict in sorted(dict.items(), key=lambda k: float(re.split('\\\\', k[1]["baseentropy"])[0])-float(re.split('\\\\', k[1][str(entropy)])[0]), reverse=False):
    for pkey, subdict in sorted(dict.items(), key=lambda k: k[1][str(metrics.entropy)], reverse=True): # if full
        print pkey
        parts = re.split(" ", pkey)
        fo.write(str(parts[1]))
        for summaryfunc in summaryfunc_list:
            skey = str(summaryfunc)
            fo.write(" & ")
            if(skey in subdict):
                res = subdict[skey]
                if(isinstance(res, float)):
                    res = round(subdict[skey], 3)
                fo.write(" $"+str(res)+"$ ")
            else:
                fo.write(" - ")
        if(not full):
            fo.write(" & $" + "%.3f" % meandiff(subdict)+"\pm" + "%.3f" % semdiff(subdict)+"$")
        fo.write(" \\\\ \n")
    fo.write("\\bottomrule\n")
    fo.write("\\end{tabular}\n")
    fo.close()

def meansemformat(mean, sem):
    return "%.3f" % mean +"\pm"+ "%.3f" % sem
    
def compile_sample_data(list_dict, petfunc_list, popularity_list, summaryfunc_list):
    result_dict = {}
    assert len(petfunc_list) == len(popularity_list)
    for i in xrange(len(petfunc_list)):
        pkey = str(petfunc_list[i])+str(popularity_list[i])
        for summaryfunc in summaryfunc_list:
            skey = str(summaryfunc)
            mean, sem = metrics.compute_stats(list_dict, pkey, skey)
            result = meansemformat(mean, sem)
            if(summaryfunc == "bitsreqd" or summaryfunc == "popularity"):
                result = mean
            if not pkey in result_dict:
                result_dict[pkey] = {}
            result_dict[pkey][skey] = result
    return result_dict
    
def tex_from_dictlist(list_dict, filename, petfunc_list, popularity_list, summaryfunc_list):
    if(len(list_dict) == 1):
        dict = list_dict[0]
    else:
        dict = compile_sample_data(list_dict, petfunc_list, popularity_list, summaryfunc_list)
    tex_from_dict_func(dict, filename, summaryfunc_list)

def base_surprisal_original(user_tuples, attributes_to_check, fmap, filename):
    fo = open(filename, "w+")
    fo.write("\\begin{tabular}{@{}lL{10cm}L{3cm}@{}}\n")
    fo.write("\\toprule\n")
    fo.write("Attribute & Original Values & Surprisal \\\\")
    fo.write("\\midrule\n")
    for attr, vals in sorted(attributes_to_check.items(), key=operator.itemgetter(0)):
        fo.write("$\mathtt{"+attr.replace(' ', '\\ ').replace('-', '{\\mhyphen}')+"}$\n")
        surs = [metrics.compute_surprisal(user_tuples, fmap[attr], val) for val in vals]
        vals = [x for _,x in sorted(zip(surs,vals), reverse=True)]
        surs = sorted(surs, reverse=True)
        fo.write(" & ")
        fo.write("\emph{"+str(vals).replace('_', '\_')+"}")
        fo.write(" & ")
        fo.write("\emph{"+str(surs)+"}")
        fo.write("\\\\\n")
        print vals
        print surs
    fo.write("\\bottomrule\n")
    fo.write("\\end{tabular}")
    fo.close()

def base_surprisal_alternate(user_tuples, attributes_to_check, fmap, filename):
    fo = open(filename, "w+")
    fo.write("\\begin{tabular}{@{}lL{10cm}L{3cm}@{}}\n")
    fo.write("\\toprule\n")
    fo.write("Attribute & Alternate Values & Surprisal \\\\")
    fo.write("\\midrule\n")
    for attr, vals in sorted(attributes_to_check.items(), key=operator.itemgetter(0)):
        fo.write("$\mathtt{"+attr.replace(' ', '\\ ').replace('-', '{\\mhyphen}')+"}$\n")
        max_tuples = [metrics.max_surprisal(user_tuples, fmap[attr], i) for i in xrange(len(vals))]
        maxsurs = [a for (a,b) in max_tuples]
        maxvals = [b for (a,b) in max_tuples]
        fo.write(" & ")
        fo.write("\emph{"+str(maxvals).replace('_', '\_')+"}")
        surs = [metrics.compute_surprisal(user_tuples, fmap[attr], val) for val in vals]
        fo.write(" & ")
        fo.write("\emph{"+str(maxsurs)+"}")
        fo.write("\\\\\n")
        print maxvals
        print maxsurs
    fo.write("\\bottomrule\n")
    fo.write("\\end{tabular}")
    fo.close()

def print_tex_line(tq, eff, dist):
    out = "Strategy & "
    out += "$"+str(tq[0][0])+"{\\times}"+str(tq[0][1])+"$ & "
    out += "$"+str(tq[1][0])+"{\\times}"+str(tq[1][1])+"$ & "
    out += "$"+ "%.3f" % eff[0]+"$ & "
    out += "$"+ "%.3f" % (1.0-eff[1])+"$ & "
    out += "$"+ "%.3f" % (1.0-eff[2])+"$ & "
    out += "$"+ "%.3f" % eff[3]+"$ & "
    out += "$"+ "%.3f" % eff[4]+"$ & "
    out += "$"+ str(int(dist[0]/1000))+"k$ & "
    out += "$"+ "%.1f" % (dist[1]*100)+"\\%$ \\\\"
    print out
import data_interface as di
import math
import numpy as np
from scipy import stats
import operator                          # for sorting dict items


def nC2(n):
    if(n<2):
        return 0
    return n*(n-1)/2

def tpr(tuples, id_func):
    if id_func == petmasks.RandScreen:
        return 0.0
    else:
        return 1.0

def fpr(tuples, id_func=None):
    reses, counts = di.listify(tuples, 2)
    total = sum(counts)
    den = nC2(total)
    print total
    num = sum([nC2(c) for c in counts])
    return float(num)/float(den)

def link(tuples, id_func=None):
    return 1-fpr(tuples, id_func)

def minanon(tuples, id_func=None):
    reses, counts = di.listify(tuples, 2)
    return min(counts)

def max_anon(tuples, id_func=None):
    reses, counts = di.listify(tuples, 2)
    return max(counts)

def prop_lesseq(counts, t):
    den = sum(counts)
    num = 0
    for c in counts:
        if(c<=t):
            num += c
    return float(num)/float(den)

def prop_less1(tuples, id_func=None):
    reses, counts = di.listify(tuples, 2)
    result = prop_lesseq(counts, 1)
    return result

def prop_less10(tuples, id_func=None):
    reses, counts = di.listify(tuples, 2)
    result = prop_lesseq(counts, 10)
    return result

def prop_gt1(tuples, id_func=None):     # prop_gt1
    reses, counts = di.listify(tuples, 2)
    result = 1.-prop_lesseq(counts, 1)
    return result

def prop_gt10(tuples, id_func=None):     # prop_gt10
    reses, counts = di.listify(tuples, 2)
    result = 1.-prop_lesseq(counts, 10)
    return result

def surprisal(c,t):
    return -math.log(c/t, 2)

def entropy(tuples, id_func=None):
    reses, counts = di.listify(tuples, 2)
    total = float(sum(counts))
    ent = sum([surprisal(float(c), total)*c/total for c in counts])
    return ent

def compute_surprisal(tuples, attribute, value):
    count, total = 0., 0.
    for tuple in tuples:
        temp_dict = di.dictize_tuple(tuple)
        if(temp_dict[attribute] == value):
            count += 1.
        total += 1.
    if(count==0):
        return 'NaN'
    return round(-math.log((count)/(total), 2), 3)

def max_surprisal(tuples, attribute, rank):
    dict = {}
    total = len(tuples)
    for tuple in tuples:
        temp_dict = di.dictize_tuple(tuple)
        val = temp_dict[attribute]
        if(val in dict):
            dict[val] += 1
        else:
            dict[val] = 1
    sorteddict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
    ranktup = sorteddict[rank]
    num = float(ranktup[1])
    return round(-math.log(num/total, 2), 3), ranktup[0]

def compute_stats(list_dict, pkey, skey):
    sample = [sam[pkey][skey] for sam in list_dict]
    mean = round(np.mean(sample), 3)
    sem = round(stats.sem(sample), 3)
    return mean, sem

def uniqueness_metric_fp(list, fprint, combo=False):
    if list == []:
        return -1., -1.
    uniqd, uniql = [], []
    uniql = uniqueness_metric(list)
    return uniqd, uniql
    
def map_to_str(list):
    for i in range(len(list)):
        if isinstance(list[i], unicode):
            list[i] = list[i].encode('utf-8')
        else:
            list[i] = str(list[i])
    return list

def stability(list):
    if list == []:
        return -1.
    result = 1.0 - (1.*len(set(map_to_str(list)))-1.)/len(map_to_str(list))
    return result 
    #return 1.0 - (1.*len(set(map(str,list)))-1.)/len(map(str,list))

def uniqueness_metric(list):
    um = (1.*len(set(map(str,list))))/len(map(str,list))
    if(um == 1./(len(map(str,list)))):
        return 0.
    else:
        return um
    
def summarize_uniqueness(uniq):
    if(isinstance(uniq, list)):
        if(uniq == []):
            return "NA"
        muniq = round(max(uniq), 1)
    else:
        muniq = uniq
    return muniq

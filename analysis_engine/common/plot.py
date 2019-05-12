import matplotlib.pyplot as plt; plt.rcdefaults()   # for plots


def bar_plot(x, y, title, fname, file=False):
    fig = plt.figure()
    plt.bar(x, y, align='center', alpha=0.5)
    plt.ylabel('Proportions')
    plt.xlabel('Bucket #')
    plt.title(title)
    plt.show()
    if(file):
        fig.savefig(fname)

def plot_res(tuples, title, fname, file=False):    
    reses, counts = di.listify(tuples, 2)
    total = sum(counts)
    frac = [float(i)/(1.*total) for i in counts]
    bar_plot(xrange(len(counts)), frac, title, fname, file)

def plot_anon(bucket_list, label_list, title, fname, file=False):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=12)
    fig, ax = plt.subplots()
    assert len(bucket_list) == len(label_list)
    colors = ['k', 'g', 'b', 'c', 'm', 'orange', 'saddlebrown', 'r', 'indigo', 'turquoise', 'teal', 'indianred', 'y']
    for i in xrange(len(label_list)):
        ax.loglog(range(1,len(bucket_list[i])+1), [el[1] for el in bucket_list[i]], linestyle='-', color=colors[i], label=label_list[i], alpha=0.7)
    ax.set_ylim(0.9)
    ax.set_xlim(0.9)
    ax.set_ylabel('Anonymity Set size')
    ax.set_xlabel('Index of fingerprints')
    ax.grid(True)
    ax.legend(loc=1, fontsize=12)
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.93, top=0.98)
    plt.show()
    if(file):
        fig.savefig(fname)

def plot_ds(tq_list, dist_list, summary_lists, summaryfunc_list, tor_dist, tor_summary, xlabel="X", fname="tradeoff-full.pdf", pname="tradeoff.pickle", pickle=False, filef=False):
    assert len(summaryfunc_list) == len(summary_lists[0])
    assert len(dist_list) == len(summary_lists)
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=12)
    summary_lists = [x for _,x in sorted(zip(dist_list,summary_lists))]
    dist_list = sorted(dist_list)
    fig, ax1 = plt.subplots()
    colors = ['c', 'y', 'r', 'g', 'b', 'm', 'k', 'r', 'g', 'b', 'c', 'm', 'y', 'k']
    for i in xrange(len(summaryfunc_list)):
        summary_list = [summaries[i] for summaries in summary_lists]
        summaryfunc = summaryfunc_list[i]
        if(0):
            ax2.plot(dist_list, summary_list, '.', color=colors[i], label=summaryname(summaryfunc).replace('_', '\_'), alpha=0.7, markeredgecolor='none')
            ax2.plot(tor_dist, tor_summary[i],'o', color=colors[i], markeredgecolor='k')
        else:
            ax1.plot(dist_list, summary_list, '.', color=colors[i], label=summaryname(summaryfunc).replace('_', '\_'), alpha=0.7, markeredgecolor='none')
            ax1.plot(tor_dist, tor_summary[i],'o', color=colors[i], markeredgecolor='k')
    ax1.set_xlabel(xlabel)
    ax1.grid(True)
    ax1.legend(loc=2, fontsize=12)
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.93, top=0.98)
    if(pickle):
        pl.dump(fig, file(pname, 'wb'))
    plt.show()
    if(filef):
        fig.savefig(fname)

def plot_ds_colored(tq_list, dist_list, summary_lists, summaryfunc_list, tor_dist, tor_summary, xlabel="X", fname="tradeoff-full.pdf", pname="tradeoff.pickle", pickle=False, filef=False):
    assert len(summaryfunc_list) == len(summary_lists[0])
    assert len(dist_list) == len(summary_lists)
    assert len(tq_list) == len(dist_list)
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=12)
    fig, ax1 = plt.subplots()
    ax1.grid(linestyle='--')
    coloraxis = 1       # 0 for width, 1 for height
    paramchoice = 0     # 0 for threshold, 1 for quanta
    for i in xrange(len(summaryfunc_list)):
        summary_list = [summaries[i] for summaries in summary_lists]
        summaryfunc = summaryfunc_list[i]
        widths, heights = breakup(tq_list, tup=paramchoice)
        assert len(widths) == len(heights) == len(summary_list)
        allxchoice, allcolorchoice = choose_axes(widths, heights, coloraxis)
        vmin, vmax = min(allcolorchoice), max(allcolorchoice)
        map = ax1.scatter(allxchoice, summary_list, vmin=vmin, vmax=vmax, marker='.', c=allcolorchoice, cmap='coolwarm', alpha=0.7)
    if(paramchoice == 1):
        torwidth, torheight = 200, 100
    elif(paramchoice == 0):
        torwidth, torheight = 1000, 1000
    else:
        raw_input("Incorrect paramchoice")
    torxchoice, torcolorchoice = choose_axes(torwidth, torheight, coloraxis)
    print tor_summary
    ax1.scatter(torxchoice, tor_summary[i], vmin=vmin, vmax=vmax, marker='s', edgecolors='k', c=torcolorchoice, cmap='coolwarm', alpha=0.7)
    ax1.set_xlabel(get_label(paramchoice, 1-coloraxis))
    ax1.set_ylabel(r"$\mathsf{eff_{"+summaryname(summaryfunc).replace('_', '\_')+"}}$")
    plt.colorbar(map, aspect=50, label=get_label(paramchoice, coloraxis))
    plt.subplots_adjust(left=0.07, bottom=0.07, right=1, top=0.98)
    if(pickle):
        pl.dump(fig, file(pname, 'wb'))
    plt.show()
    if(filef):
        fig.savefig(fname)

def plot_ds_wrapper(tq_list, dist_lists, distfunc_list, summary_lists, summaryfunc_list, tor_dist, tor_summary, fname="tradeoff.pdf", pname="tradeoff.pickle", pickle=False, filef=False):
    assert len(summaryfunc_list) == len(summary_lists[0])
    assert len(distfunc_list) == len(dist_lists[0])
    assert len(dist_lists) == len(summary_lists)
    for i in xrange(len(distfunc_list)):
        dist_list = [d[i] for d in dist_lists]
        tord = tor_dist[i]
        if(i==1):
            dist_list = [d[i]*100 for d in dist_lists]
            tord = tord*100
        for j in xrange(len(summaryfunc_list)):
            plot_ds_colored(tq_list, dist_list, [[summaries[j]] for summaries in summary_lists], [summaryfunc_list[j]], tord, [tor_summary[j]], xlabel=getlabel(distfunc_list[i]), fname=summaryname(summaryfunc_list[j])+"q1550.pdf", pname="tradeoff"+str(i)+str(j)+".pickle", pickle=pickle, filef=filef)

def color_map(qw, qh):
    return (float(qw)/200., 0.0, float(qh)/100.)

def get_color(tq_list):
    colors = []
    for tq in tq_list:
        qw, qh = tq[1]
        colors.append(color_map(qw, qh))
    return colors

def get_colorh(q_list):
    colors = []
    for qh in q_list:
        colors.append(color_map(0., qh))
    return colors

def get_colorw(q_list):
    colors = []
    for qw in q_list:
        colors.append(color_map(qw, 100.))
    return colors

def get_label(paramchoice, coloraxis):
    label = ""
    if(paramchoice == 0):
        label += "Threshold "
    elif(paramchoice == 1):
        label += "Quanta "
    else:
        raw_input("Incorrect paramchoice")
    if(coloraxis == 0):
        label += "Width"
    elif(coloraxis == 1):
        label += "Height"
    else:
        raw_input("Incorrect coloraxis")
    return label

def choose_axes(width, height, coloraxis):
    if(coloraxis == 0):
        return height, width
    elif(coloraxis == 1):
        return width, height
    else:
        raw_input("Incorrect coloraxis")

def getlabel(distfunc):
    if "pct" in str(distfunc):
        return "Average Percentage Pixel Loss"
    else:
        return "Average Absolute Pixel Loss"

def getshortlabel(distfunc):
    if "pct" in str(distfunc):
        return "pct"
    else:
        return "abs"

def breakup(tq_list, tup):
    qw, qh = [], []
    for tq in tq_list:
        qw.append(tq[tup][0])
        qh.append(tq[tup][1])
    return qw, qh
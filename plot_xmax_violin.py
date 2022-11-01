import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np
from matplotlib import cm
import matplotlib.gridspec as grid_spec

def read_energy_range(ibin):
    filename = 'AugerXmaxData/xmaxHistograms.txt'
    i = 0
    lgMinEnergy, lgMaxEnergy = -1, -1
    for line in open(filename):
        if i == ibin:
            line = line.rstrip()
            fields = line.split()
            assert(int(fields[0]) == ibin)
            lgMinEnergy = float(fields[1])
            lgMaxEnergy = float(fields[2])
            nEvents = int(fields[3])
        i = i + 1
    return lgMinEnergy, lgMaxEnergy, nEvents

def read_counts(ibin):
    filename = 'AugerXmaxData/xmaxHistograms.txt'
    i = 0
    counts = []
    for line in open(filename):
        if i == ibin:
            line = line.rstrip()
            fields = line.split()
            assert(int(fields[0]) == ibin)
            for i in range(100):
                c = float(fields[i+7])
                counts.append(c)
        i = i + 1
    return np.array(counts)

def set_axes(ax):
    ax.set_ylim([0.5,17.])
    ax.set_ylim([570.,900.])
    ax.set_ylabel(r'X$_\textrm{max}$ [g/cm$^2$]')
    ax.set_xticklabels([])
    ax.minorticks_off()
    ax.tick_params(axis='both', which='major', length=7, width=2, labelsize=17)
    
def plot_xmax_violin():
    fig = plt.figure(figsize=(17.0, 6.0))
    ax = fig.add_subplot(111)
    set_axes(ax)

    Xmax = np.linspace(0., 2000., 100)
    cmap = matplotlib.cm.get_cmap('jet')
    colors = np.linspace(0, 1, 18)
    for ibin in range(18):
        counts = read_counts(ibin)
        print (counts)
        nEvents = np.sum(counts)
        color = cmap(colors[ibin])
        ax.barh(Xmax, counts / float(nEvents), height=20, left=ibin * 0.75, color=color, alpha=0.76, edgecolor='tab:gray', lw=1) #, alpha=0.4)
        ax.barh(Xmax, -counts / float(nEvents), height=20, left=ibin * 0.75, color=color, alpha=0.76, edgecolor='tab:gray', lw=1) #, alpha=0.4)

    plt.savefig('xmax_violin.pdf', bbox_inches='tight', pad_inches=0.5)
        
if __name__== "__main__":
    plot_xmax_violin()

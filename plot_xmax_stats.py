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

def read_moments(ibin):
    filename = 'AugerXmaxData/xmaxMoments.txt'
    i = 0
    meanLgEnergy = -1
    meanXmax, meanXmaxSigmaStat, meanXmaxSigmaSysUp, meanXmaxSigmaSysLow = -1, -1, -1, -1
    sigmaXmax, sigmaXmaxSigmaStat, sigmaXmaxSigmaSysUp, sigmaXmaxSigmaSysLow = -1, -1, -1, -1
    
    for line in open(filename):
        if i == ibin:
            line = line.rstrip()
            fields = line.split()
            assert(int(fields[0]) == ibin)
            meanLgEnergy = float(fields[3])
            meanXmax = float(fields[5])
            meanXmaxSigmaStat = float(fields[6])
            meanXmaxSigmaSysUp = float(fields[7])
            meanXmaxSigmaSysLow = float(fields[8])
            sigmaXmax = float(fields[9])
            sigmaXmaxSigmaStat = float(fields[10])
            sigmaXmaxSigmaSysUp = float(fields[11])
            sigmaXmaxSigmaSysLow = float(fields[12])
        i = i + 1
    
    meanXmaxSigmaUp = np.sqrt(meanXmaxSigmaStat * meanXmaxSigmaStat + meanXmaxSigmaSysUp * meanXmaxSigmaSysUp)
    meanXmaxSigmaLow = np.sqrt(meanXmaxSigmaStat * meanXmaxSigmaStat + meanXmaxSigmaSysLow * meanXmaxSigmaSysLow)
    sigmaXmaxUp = np.sqrt(sigmaXmaxSigmaStat * sigmaXmaxSigmaStat + sigmaXmaxSigmaSysUp * sigmaXmaxSigmaSysUp)
    sigmaXmaxLow = np.sqrt(sigmaXmaxSigmaStat * sigmaXmaxSigmaStat + sigmaXmaxSigmaSysLow * sigmaXmaxSigmaSysLow)
    return meanLgEnergy, meanXmax, meanXmaxSigmaUp, meanXmaxSigmaLow, sigmaXmax, sigmaXmaxUp, sigmaXmaxLow

def set_axes(ax):
    ax.set_ylim([0.001,0.4])
    ax.set_xlim([550.,950.])
    ax.minorticks_off()
    ax.tick_params(axis='both', which='major', length=7, width=2, labelsize=17)
    
def plot_xmax_hists():
    fig = plt.figure(figsize=(10.5, 17.5))
    gs = grid_spec.GridSpec(6, 3)
    gs.update(hspace=0.075,wspace=0.05)

    Xmax = np.linspace(0., 2000., 100)
    for i in range(6):
        for j in range(3):
            ax = fig.add_subplot(gs[i,j])
            set_axes(ax)
            ibin = j + 3 * i
            lgMinEnergy, lgMaxEnergy, nEvents = read_energy_range(ibin)
            meanLgEnergy, meanXmax, meanXmaxSigmaUp, meanXmaxSigmaLow, sigmaXmax, sigmaXmaxUp, sigmaXmaxLow = read_moments(ibin)
            counts = read_counts(ibin)
            ax.plot([meanXmax, meanXmax], [0, 1], linestyle=':', color='tab:gray')
            ax.fill_between([meanXmax - sigmaXmax, meanXmax + sigmaXmax], [1, 1], color='tab:gray', alpha = 0.2)

            ax.bar(Xmax, counts / float(nEvents), width=20, color='tab:orange', alpha=0.6, edgecolor='tab:red', lw=1) #, alpha=0.4)
            ax.text(570., 0.34, "%4.1f $<$ lg(E/eV) $<$ %4.1f" % (lgMinEnergy, lgMaxEnergy), fontsize=13)

            if i != 5:
                ax.set_xticklabels([])
            if j != 0:
                ax.set_yticklabels([])

    fig.supxlabel(r'X$_\textrm{max}$ [g/cm$^2$]', fontsize=25, y=0.05)
    fig.supylabel(r'events / total events', fontsize=25)
    
    plt.savefig('xmax_hists.pdf', bbox_inches='tight', pad_inches=0.5)
    
def add_point(ax, x, y, xerr, yerr):
    color = 'tab:gray'
    ax.errorbar(x, y, xerr=np.array([xerr]).T, yerr=np.array([yerr]).T, fmt='o', markersize=7, elinewidth=2, markeredgecolor=color, capsize=4, capthick=2, color=color, zorder=1)
    
def plot_xmax_3D():
    fig = plt.figure(figsize=(10.5, 8.5))
    ax = fig.add_subplot(111)
    ax.set_xlim([700, 800])
    ax.set_xlabel(r'X$_\textrm{max}$ [g/cm$^2$]')
    ax.set_ylim([20, 70])
    ax.set_ylabel(r'$\sigma$ [g/cm$^2$]')
    
    x = []
    y = []
    z = []
    
    for ibin in range(18):
        meanLgEnergy, meanXmax, meanXmaxSigmaUp, meanXmaxSigmaLow, sigmaXmax, sigmaXmaxUp, sigmaXmaxLow = read_moments(ibin)
        x.append(meanXmax)
        y.append(sigmaXmax)
        z.append(meanLgEnergy)
        add_point(ax, meanXmax, sigmaXmax, [meanXmaxSigmaLow, meanXmaxSigmaUp], [sigmaXmaxLow, sigmaXmaxUp])

    x, y, z = np.array(x), np.array(y), np.array(z)
    scp = ax.scatter(x, y, s=7.*z, c=z, vmin=min(z), vmax=max(z), cmap='jet', edgecolor='tab:gray', zorder=3)

    plt.colorbar(scp)
    plt.savefig('xmax_3D.pdf')
    
if __name__== "__main__":
    plot_xmax_hists()
    plot_xmax_3D()


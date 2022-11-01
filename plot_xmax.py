import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np
from matplotlib import cm
import matplotlib.gridspec as grid_spec

def read_mean():
    filename = 'AugerXmaxData/xmaxMoments.txt'
    meanXmax, meanXmaxSigmaStat, meanXmaxSigmaSysUp, meanXmaxSigmaSysLow = np.loadtxt(filename, usecols=(5,6,7,8), unpack=True, skiprows=0)
    return meanXmax, meanXmaxSigmaStat, meanXmaxSigmaSysUp, -meanXmaxSigmaSysLow

def read_sigma():
    filename = 'AugerXmaxData/xmaxMoments.txt'
    sigmaXmax, sigmaXmaxSigmaStat, sigmaXmaxSigmaSysUp, sigmaXmaxSigmaSysLow = np.loadtxt(filename, usecols=(9,10,11,12), unpack=True, skiprows=0)
    return sigmaXmax, sigmaXmaxSigmaStat, sigmaXmaxSigmaSysUp, -sigmaXmaxSigmaSysLow

def read_energy_range():
    filename = 'AugerXmaxData/xmaxMoments.txt'
    lgMinEnergy, lgMaxEnergy, meanLgEnergy = np.loadtxt(filename, usecols=(1,2,3), unpack=True, skiprows=0)
    return meanLgEnergy, meanLgEnergy - lgMinEnergy, lgMaxEnergy - meanLgEnergy

def set_axes(ax):
    ax.set_xlim([17.7,20.])
    ax.set_xlabel('lg(E/eV)')
    
def add_points(ax, x, y, xerr, yerr, color):
    ax.errorbar(x, y, yerr=yerr, fmt='o', markersize=7, elinewidth=2, capsize=4, capthick=2,
        markeredgecolor=color, color=color, zorder=1)

def plot_xmax():
    fig = plt.figure(figsize=(16.5, 7.5))
    gs = grid_spec.GridSpec(1, 2)
    gs.update(hspace=0.075,wspace=0.075)

    ax1 = fig.add_subplot(gs[0,0])
    set_axes(ax1)
    ax1.set_ylim([680.,820.])
    ax1.set_ylabel(r'$\langle X_{\rm max}\rangle$ [g/cm$^2$]')

    x, dxLow, dxUp = read_energy_range()
    y, yStat, ySysUp, ySysLow = read_mean()
    ax1.fill_between(x, y - ySysLow, y + ySysUp, color='tab:green', alpha=0.3)
    add_points(ax1, x, y, [dxLow, dxUp], [yStat, yStat], 'tab:red')

    ax2 = fig.add_subplot(gs[0,1])
    set_axes(ax2)
    ax2.set_ylim([10.,80.])
    ax2.set_ylabel(r'$\sigma(X_{\rm max})$ [g/cm$^2$]')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")

    y, yStat, ySysUp, ySysLow = read_sigma()
    ax2.fill_between(x, y - ySysLow, y + ySysUp, color='tab:green', alpha=0.3)
    add_points(ax2, x, y, [dxLow, dxUp], [yStat, yStat], 'tab:red')
 
    plt.savefig('xmax.pdf', bbox_inches='tight', pad_inches=0.5)

if __name__== "__main__":
    plot_xmax()
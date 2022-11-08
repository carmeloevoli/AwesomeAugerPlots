import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np
from matplotlib import cm
import matplotlib.gridspec as grid_spec

def read_mean():
    filename = 'AugerICRC2019_Xmax_lnA_Moments/AugerICRC2019_Xmax_Moments.txt'
    meanXmax, meanXmaxSigmaStat, meanXmaxSigmaSysUp, meanXmaxSigmaSysLow = np.loadtxt(filename, usecols=(2,3,4,5), unpack=True, skiprows=42)
    return meanXmax, meanXmaxSigmaStat, meanXmaxSigmaSysUp, meanXmaxSigmaSysLow

def read_sigma():
    filename = 'AugerICRC2019_Xmax_lnA_Moments/AugerICRC2019_Xmax_Moments.txt'
    sigmaXmax, sigmaXmaxSigmaStat, sigmaXmaxSigmaSysUp, sigmaXmaxSigmaSysLow = np.loadtxt(filename, usecols=(6,7,8,9), unpack=True, skiprows=42)
    return sigmaXmax, sigmaXmaxSigmaStat, sigmaXmaxSigmaSysUp, sigmaXmaxSigmaSysLow

def read_energy_range():
    filename = 'AugerICRC2019_Xmax_lnA_Moments/AugerICRC2019_Xmax_Moments.txt'
    meanLgEnergy, nEvts = np.loadtxt(filename, usecols=(0,1), unpack=True, skiprows=42)
    return meanLgEnergy

def set_axes(ax):
    ax.set_xlim([17.,20.])
    ax.set_xlabel('lg(E/eV)')
    
def add_points(ax, x, y, yerr, color):
    ax.errorbar(x, y, yerr=yerr, fmt='o', markersize=7, elinewidth=2, capsize=4, capthick=2,
        markeredgecolor=color, color=color, zorder=1)

def plot_single_mass(ax, E, A):
    lnA = np.log(float(A))
    E_0 = 1e19
    X_0, D, xi, delta = 795.1, 57.7, -0.04, -0.04 # Sibyll2.1
    X_max = X_0 + D * np.log10(E / E_0 / A) + xi * lnA + delta * lnA * np.log10(E / E_0)
    ax.plot(np.log10(E), X_max, linestyle=':')
    X_0, D, xi, delta = 809.7, 62.2, 0.78, 0.08 # EPOS1.99
    X_max = X_0 + D * np.log10(E / E_0 / A) + xi * lnA + delta * lnA * np.log10(E / E_0)
    ax.plot(np.log10(E), X_max, linestyle='--')
    X_0, D, xi, delta = 781.8, 45.8, -1.13, 1.71 # QGSJetII
    X_max = X_0 + D * np.log10(E / E_0 / A) + xi * lnA + delta * lnA * np.log10(E / E_0)
    ax.plot(np.log10(E), X_max, linestyle='-.')

def plot_xmax():
    fig = plt.figure(figsize=(16.5, 7.5))
    gs = grid_spec.GridSpec(1, 2)
    gs.update(hspace=0.075,wspace=0.075)

    ax1 = fig.add_subplot(gs[0,0])
    set_axes(ax1)
    ax1.set_ylim([630.,820.])
    ax1.set_ylabel(r'$\langle X_{\rm max}\rangle$ [g/cm$^2$]')

    x = read_energy_range()
    y, yStat, ySysUp, ySysLow = read_mean()
    ax1.fill_between(x, y - ySysLow, y + ySysUp, color='tab:green', alpha=0.3)
    add_points(ax1, x, y, [yStat, yStat], 'tab:red')

    E = np.logspace(17, 20, 1000)
    plot_single_mass(ax1, E, 1.0)

    ax2 = fig.add_subplot(gs[0,1])
    set_axes(ax2)
    ax2.set_ylim([12.,80.])
    ax2.set_ylabel(r'$\sigma(X_{\rm max})$ [g/cm$^2$]')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")

    y, yStat, ySysUp, ySysLow = read_sigma()
    ax2.fill_between(x, y - ySysLow, y + ySysUp, color='tab:green', alpha=0.3)
    add_points(ax2, x, y, [yStat, yStat], 'tab:red')
 
    plt.savefig('xmax.pdf', bbox_inches='tight', pad_inches=0.5)

if __name__== "__main__":
    plot_xmax()

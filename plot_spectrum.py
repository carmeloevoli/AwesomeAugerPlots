import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np

def read_spectrum():
    filename = 'SD750AndCombinedSpectrum/spectrum.combined.txt'
    lgE, J, sigmaStatLow, sigmaStatUp, sigmaSysLow, sigmaSysUp = np.loadtxt(filename, usecols=(0,2,3,4,5,6), unpack=True, skiprows=1)
    E = np.power(10., lgE)
    E3 = np.power(E, 3.)
    return lgE, E3 * J, E3 * sigmaStatLow, E3 * sigmaStatUp, E3 * sigmaSysLow, E3 * sigmaSysUp
    
def set_axes(ax):
    ax.set_xlim([16.8,20.4])
    ax.set_xlabel('lg(E/eV)')
    ax.set_yscale('log')
    ax.set_ylim([1e36,2e38])

def add_points(ax, x, y, yerr, color):
    ax.errorbar(x, y, yerr=yerr, fmt='o', markersize=7, elinewidth=2, capsize=4, capthick=2,
        markeredgecolor=color, color=color, zorder=1)

def plot_spectrum():
    fig = plt.figure(figsize=(10.5, 8.0))
    ax = fig.add_subplot(111)
    set_axes(ax)

    lgE, J, sigmaStatLow, sigmaStatUp, sigmaSysLow, sigmaSysUp = read_spectrum()

    ax.fill_between(lgE, J - sigmaSysLow, J + sigmaSysUp, color='tab:green', alpha=0.3)
    add_points(ax, lgE, J, [sigmaStatLow, sigmaStatUp], color='tab:red')

    plt.savefig('spectrum.pdf', bbox_inches='tight', pad_inches=0.5)

if __name__== "__main__":
    plot_spectrum()

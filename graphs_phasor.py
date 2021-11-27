import matplotlib.pyplot as plt
#from pylab import *
import numpy as np
import pandas as pd
from matplotlib.widgets import Slider, Button
#from graphs_analysis import *

######Functions
def plot_phasors(t, topology):
    plt.style.use('style.mplstyle')
    fig, ax = plt.subplots(figsize=(6, 10), subplot_kw=dict(polar=True))
    plt.subplots_adjust(bottom = 0.35)
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['axes.titlepad'] = 10
    t1 = 0
    t2 = len(t.time_cos)-25

    ##########################################################################################################
    #########ARROWS
    ##Time 1
    #Voltage
    ax.arrow(0, 0, 0, 1, width = 0.015, lw = 1, color = "red", zorder = 5, label = "RMS Voltage at time 1")
    #Current
    ax.arrow(np.arccos(t.cos_phi1[t1]), 0, 0, 1,width = 0.015, color = "blue", zorder = 5, label = "RMS Current at time 1")

    ##Time 2
    #Voltage
    ax.arrow(0, 0, 0, 1, width = 0.015, lw = 1, color = "green", zorder = 5, label = "RMS Voltage at time 2")
    #Current
    ax.arrow(np.arccos(t.cos_phi1[t2]), 0, 0, 1,width = 0.015, color = "orange", zorder = 5, label = "RMS Current at time 2")

    ax.set_yticklabels([])
    ax.set_thetagrids(angles = range(0, 360, 30), color = "grey")

    ##########################################################################################################
    #########AUX GRAPH
    ax1 = plt.axes([0.1,0.05,0.8,0.15])

    ax1.plot(t.time, t.i1, color = '#EE6666', label = 'A1 RMS', zorder = 5)
    ax1.axes.xaxis.set_ticklabels([])
    ax1.set_ylabel('RMS Current', size = 10)
    ax1.set_xlabel('Time (s)', size = 10)
    ax1.set_title("RMS Current variation with time\n for the "+topology+" rotor topology")

    ##########################################################################################################
    #########SLIDERS

    # Create 3 axes for 3 sliders red,green and blue
    axtime1 = plt.axes([0.2, 0.32, 0.65, 0.03])
    axtime2 = plt.axes([0.2, 0.27, 0.65, 0.03])

    # Create a sliders
    time1 = Slider(axtime1, 'Time 1', 0, len(t.time_cos)-1, 5, valfmt="%i", color = "blue")
    time2 = Slider(axtime2, 'Time 2', 0, len(t.time_cos)-1, t2, valfmt="%i", color = "orange")
    
    # Create fuction to be called when slider value is changed
    def update(val):
        t1 = int(time1.val)
        t2 = int(time2.val)
        ax.clear()
        ax.arrow(0, 0, 0, 1, width = 0.015, lw = 1, color = "red", zorder = 5, label = "RMS Voltage at time 1")
        ax.arrow(np.arccos(t.cos_phi1[t1]), 0, 0, 1,width = 0.015, color = "blue", zorder = 5, label = "RMS Current at time 1")
        ax.arrow(0, 0, 0, 1, width = 0.015, lw = 1, color = "green", zorder = 5, label = "RMS Voltage at time 2")
        ax.arrow(np.arccos(t.cos_phi1[t2]), 0, 0, 1,width = 0.015, color = "orange", zorder = 5, label = "RMS Current at time 2")
        ax.legend(fontsize = 8, loc = "lower left")
        ax.set_yticklabels([])
        ax.set_thetagrids(angles = range(0, 360, 30), color = "grey")
        delta_phi1 = float("{:.2f}".format((np.arccos(t.cos_phi1[t2])-np.arccos(t.cos_phi1[t1]))*180/np.pi))
        ax.text(0.5, 5, "\u0394 \u03C6 = "+str(delta_phi1),
                horizontalalignment='center',
                verticalalignment='top',
                size='large',
                transform=plt.gca().transAxes)

    # Call update function when slider value is changed
    time1.on_changed(update)
    time2.on_changed(update)

    ##########################################################################################################
    #########PLOT
    plt.subplots_adjust(hspace = 0.35, wspace = 0.25)
    plt.suptitle("Phasor Analysis for phase 1\nRotor topology: "+topology, y = 0.94)
    ax.legend(fontsize = 8, loc = "lower left")
    plt.show()
    return


######REFERENCES
#https://www.geeksforgeeks.org/three-dimensional-plotting-in-python-using-matplotlib/
#https://medium.com/@rohitadnaik/3d-line-plot-in-python-2fbeca99b9ba
#https://www.geeksforgeeks.org/use-different-y-axes-on-the-left-and-right-of-a-matplotlib-plot/
#https://jakevdp.github.io/PythonDataScienceHandbook/04.11-settings-and-stylesheets.html
#https://nicoguaro.github.io/posts/matplotlib_styles/
#https://github.com/matplotlib/matplotlib/blob/v3.4.1/matplotlibrc.template
#https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
#https://www.py4u.net/discuss/217665
#https://www.geeksforgeeks.org/matplotlib-slider-widget/
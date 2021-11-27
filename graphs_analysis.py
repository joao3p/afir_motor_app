#######Graphs Analysis
import matplotlib.pyplot as plt
#from pylab import *
import numpy as np
import pandas as pd
from graphs_phasor import *

#######Classes
class test:
    def __init__(self, phases,p,q,stator,config,df,topology):
        self.name = str(config) + " for " + topology + " rotor topology with "+ str(phases) + " phases and " + str(p) + " poles"
        self.p = p
        self.q = q
        self.phases = phases
        self.stator = stator
        self.topology = topology
        self.config = str(config)+" configuration with "+str(p)+" poles and "+str(phases)+" phases for " + topology + " rotor topology"
        self.i1 = df['A1 RMS'].to_list()
        self.i2 = df['A2 RMS'].to_list()
        self.i3 = df['A3 RMS'].to_list()
        self.v1 = df['V1 RMS'].to_list()
        self.v2 = df['V2 RMS'].to_list()                                    
        self.v3 = df['V3 RMS'].to_list()
        self.pt = df['PT (W)'].to_list()
        self.qt = arange_list(df['QT (var)'].to_list())
        self.st = df['ST (VA)'].to_list()
        self.dt = arange_list(df['DT (var)'].to_list())
        time = adjust_time(len(df['Time:'].to_list()))
        self.time = time
        level = cos_phi_find_value(df['Cos φ1 (DPF)'].to_list())
        self.cos_phi1 = [float(i) for i in df['Cos φ1 (DPF)'].to_list()[level[0]+1:level[1]-1]]
        self.cos_phi2 = [float(i) for i in df['Cos φ2 (DPF)'].to_list()[level[0]+1:level[1]-1]]
        self.cos_phi3 = [float(i) for i in df['Cos φ3 (DPF)'].to_list()[level[0]+1:level[1]-1]]
        #print(level)
        self.time_cos = time[level[0]+1:level[1]-1]
        #print(self.cos_phi1)

    #@staticmethod
    def plot_line_current(self, ax, colors, colors2):
        ax.plot(self.time, self.i1, color = colors[9], zorder = 5, label = "phase 1")
        ax.plot(self.time, self.i2, color = colors2[0], zorder = 5, label = "phase 2")
        ax.plot(self.time, self.i3, color = colors2[3], zorder = 5, label = "phase 3")
        ax.set_title("RMS Three-phase Current")
        ax.set_ylabel('RMS line current for the 3 phases (A)', size = 10)
        ax.set_xlabel('Time (s)', size = 10)
        #ax.set_yticks(np.arange(0,6,0.5))
        return
    #@staticmethod
    def plot_line_voltage(self, ax, colors, colors2):
        ax.plot(self.time, self.v1, color = colors[9], zorder = 5, label = "phase 1")
        ax.plot(self.time, self.v2, color = colors2[0], zorder = 5, label = "phase 2")
        ax.plot(self.time, self.v3, color = colors2[3], zorder = 5, label = "phase 3")
        ax.set_title("RMS Three-phase Voltage")
        ax.set_ylabel('RMS line voltage for the 3 phases (V)', size = 10)
        ax.set_xlabel('Time (s)', size = 10)
        return
    #@staticmethod
    def plot_line_cos_phi(self, ax, colors, colors2):
        ax.plot(self.time_cos, self.cos_phi1, color = colors[9], zorder = 5, label = "phase 1")
        ax.plot(self.time_cos, self.cos_phi2, color = colors2[0], zorder = 5, label = "phase 2")
        ax.plot(self.time_cos, self.cos_phi3, color = colors2[3], zorder = 5, label = "phase 3")
        ax.set_title("Three-phase Cos("+r"$\phi$"+")")
        ax.set_ylabel('Cos(phi) for the 3 phases', size = 10)
        ax.set_xlabel('Time (s)', size = 10)
        #ax.set_yticks(np.arange(0.5,1,0.05))
        return
    #@staticmethod
    def plot_line_power(self, ax, colors, colors2):
        ax.plot(self.time, self.pt, color = colors2[3], zorder = 5, label = "active")
        ax.plot(self.time, self.qt, color = colors2[2], zorder = 5, label = "reactive")
        ax.plot(self.time, self.st, color = colors2[0], zorder = 5, label = "apparent")
        ax.plot(self.time, self.dt, color = colors2[1], zorder = 5, label = "distortion")
        ax.set_title("Total Power")
        ax.set_ylabel('Total active (W), reactive (VAR), \napparent (VA) and distortion power (VAR)', size = 10)
        ax.set_xlabel('Time (s)', size = 10)
        #ax.set_yticks(np.arange(0,max(t1.st),50))
        return

######FUNCTIONS
def get_data(data_path):
    df = pd.read_excel(data_path, sheet_name="Trend")
    #change columns names and delete not used rows
    keys = df.columns.to_list()
    values = df.loc[0].to_list()
    names = dict()
    for i in range(len(keys)):
        names[keys[i]] = values[i]
    df.rename(columns = names, inplace = True)
    df.drop(labels = [0,1,2], inplace = True)
    return df

def adjust_time(length):
    time = list()
    for x in range(length):
        time.append(x)
    return time

def cos_phi_find_value(c):
    i = 0
    b = 0
    e = 0
    for x in range(len(c)):
        try:
            float(c[x])
        except:
            if i == 1:
                e = x
                i = 0
            continue
        if i == 0:
            b = x
            i = 1
    return [b,e]

def arange_list(l):
    j = list()
    for x in range(len(l)):
        try:
            j.append(float(l[x]))
        except:
            j.append(0)
    return j

def make_analysis(data_path, phases, p, q,stator,config,topology):
    print(phases,p,q,config,stator,topology)
    #######DEFINITIONS
    df = get_data(data_path)
    t1 = test(phases,p,q,stator,config,df,topology)
    #######GRAPHS
    plt.style.use('style.mplstyle')
    fig = plt.figure(figsize = [12,7])
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(223)
    ax4 = plt.subplot(224)
    colors = ['blue','gold','red','green','purple','orange','pink','brown','black','coral','grey','magenta']
    colors2 = ['darkturquoise','goldenrod','tomato','lightgreen','darkviolet','chocolate','lightpink','darkgoldenrod','darkgrey','lightcoral','lightgrey','fuchsia']
    ####PARAMS
    plt.rcParams['axes.titlesize'] = 15
    plt.rcParams['axes.labelsize'] = 2
    ####PLOT
    t1.plot_line_current(ax1, colors, colors2)
    t1.plot_line_voltage(ax2, colors, colors2)
    t1.plot_line_cos_phi(ax3, colors, colors2)
    t1.plot_line_power(ax4, colors, colors2)
    plt.suptitle(t1.name, y = 0.95)
    plt.tight_layout(pad = 2.5)
    ax1.legend(loc = "upper left")
    ax2.legend(loc = "upper left")
    ax3.legend(loc = "lower right")
    ax4.legend(fontsize = 8, loc = "upper left")
    plt.show()
    return

def make_phasors(data_path, phases, p, q,stator,config,topology):
    print(phases,p,q,config,stator,topology)
    df = get_data(data_path)
    t1 = test(phases,p,q,stator,config,df,topology)
    plot_phasors(t1,topology)
    return

########REFERENCES
#https://stackabuse.com/change-tick-frequency-in-matplotlib/
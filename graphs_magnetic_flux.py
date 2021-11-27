import matplotlib.pyplot as plt
#from pylab import *
import numpy as np
import pandas as pd

######FUNCTIONS
def make_point(ax,paint, x, y):
    ax.plot(x, y, 'o', color=paint, ms = 7.5, mec = 'white', zorder = 7)
    return ax

def plot_2d_flux(file,mode):
    if mode == 0:
        df1 = pd.read_excel(r'MotorHTS.xlsx',sheet_name=file)
        teeth = df1['Tooth'].to_list()
        flux1 = df1['Flux Phase 1'].to_list()
        flux2 = df1['Flux Phase 2'].to_list()
        flux3 = df1['Flux Phase 3'].to_list()
        colors = ['#2C2C2C','#C52626','#66A2EE']
        labels = ["Phase 1","Phase 2","Phase 3"]
    elif mode == 4:
        df1 = pd.read_excel(r'MotorHTS.xlsx',sheet_name="flux tests 2 poles")
        df2 = pd.read_excel(r'MotorHTS.xlsx',sheet_name="flux tests 4 poles")
        df3 = pd.read_excel(r'MotorHTS.xlsx',sheet_name="flux tests 8 poles")
        teeth = df1['Tooth'].to_list()
        flux1 = df1['Flux Phase 1'].to_list()
        flux1_1 = df1['Flux Phase 2'].to_list()
        flux1_2 = df1['Flux Phase 3'].to_list()
        flux2 = df2['Flux Phase 1'].to_list()
        flux2_1 = df2['Flux Phase 2'].to_list()
        flux2_2 = df2['Flux Phase 3'].to_list()
        flux3 = df3['Flux Phase 1'].to_list()
        flux3_1 = df3['Flux Phase 2'].to_list()
        flux3_2 = df3['Flux Phase 3'].to_list()
        colors = ['#EE6666','#66A2EE','#64A246']
        labels = ['2 Poles','4 Poles','8 Poles']
    else:
        df1 = pd.read_excel(r'MotorHTS.xlsx',sheet_name="flux tests 2 poles")
        df2 = pd.read_excel(r'MotorHTS.xlsx',sheet_name="flux tests 4 poles")
        df3 = pd.read_excel(r'MotorHTS.xlsx',sheet_name="flux tests 8 poles")
        teeth = df1['Tooth'].to_list()
        flux1 = df1['Flux Phase '+str(mode)].to_list()
        flux2 = df2['Flux Phase '+str(mode)].to_list()
        flux3 = df3['Flux Phase '+str(mode)].to_list()
        colors = ['#EE6666','#66A2EE','#64A246']
        labels = ['2 Poles','4 Poles','8 Poles']
        
    ######FIG
    plt.style.use('style.mplstyle')
    fig = plt.figure(figsize= [15,5])
    x = 0
    y = 0
    z = 0
    if (mode == 0 and int(file[11]) == 8):
        plt.ylim(87,180)
        x = 140
        y = 40
        z = 70
    plt.xlim(0.5,24.5)
    plt.xticks(np.arange(1,len(teeth)+1,1))
    ######AXIS1
    ax1 = plt.subplot(111)
    if mode == 4:
        ax1.plot(teeth, flux1_1, color = colors[0], zorder = 4)
        ax1.plot(teeth, flux2_1, color = colors[1], zorder = 4)
        ax1.plot(teeth, flux3_1, color = colors[2], zorder = 4)
        ax1.plot(teeth, flux1_2, color = colors[0], zorder = 4)
        ax1.plot(teeth, flux2_2, color = colors[1], zorder = 4)
        ax1.plot(teeth, flux3_2, color = colors[2], zorder = 4)
    ax1.grid(b=True, which='major')
    ax1.plot(teeth, flux1, color = colors[0], zorder = 4 , label = labels[0]) ##2C2C2C
    ax1.plot(teeth, flux2, color = colors[1], zorder = 4 , label = labels[1]) ##66A2EE ##F0ACAC ##EE6666
    ax1.plot(teeth, flux3, color = colors[2], zorder = 4 , label = labels[2]) ##64A246 ##A4C9DE ##66A2EE
    ax1.set_ylabel('Magnetic Flux Variation (mV)', color = '#C52626' , size = 15)
    ax1.set_xlabel('Teeth', color='grey' , size = 19)
    ax1.tick_params(axis ='y', labelcolor = '#C52626')

    #######POINTS AND STATOR
    o = 1
    for i in range(len(teeth)):
        if mode == 4:
            make_point(ax1, colors[0], teeth[i], flux1_1[i])
            make_point(ax1, colors[0], teeth[i], flux1_2[i])
            make_point(ax1, colors[1], teeth[i], flux2_1[i])
            make_point(ax1, colors[1], teeth[i], flux2_2[i])
            make_point(ax1, colors[2], teeth[i], flux3_1[i])
            make_point(ax1, colors[2], teeth[i], flux3_2[i])
        make_point(ax1, colors[0], teeth[i], flux1[i])
        make_point(ax1, colors[1], teeth[i], flux2[i])
        make_point(ax1, colors[2], teeth[i], flux3[i])##LINE
        ax1.plot([i+0.75,i+1.25], [-20+x,-20+x] ,color='grey',ls='-')
        if i != len(teeth)-1:
            ax1.plot([i+1.25,i+1.75], [-80+x+y,-80+x+y],color='grey',ls='-')
        ax1.plot([i+0.75,i+0.75] , [-20+x,-80+x+y] ,color='grey',ls='-')
        ax1.plot([i+1.25,i+1.25] , [-20+x,-80+x+y] ,color='grey',ls='-')
    ax1.plot([24+0.25,24+0.25], [-20+x,-120+x+z],color='grey',ls='-')
    ax1.plot([0.75,0.75], [-20+x,-120+x+z],color='grey',ls='-')
    ax1.plot([0.75,24+0.25] ,[-120+x+z,-120+x+z], color = 'grey', ls ='-') 
    #######PLOT
    plt.subplots_adjust(hspace = 0.35, wspace = 0.25)
    plt.legend(fontsize=12)
    plt.show()

######3D
def plot_3d_flux(file):
    fig = plt.figure(figsize= [5,5])
    df1 = pd.read_excel(r'MotorHTS.xlsx',sheet_name=file)
    teeth = df1['Tooth'].to_list()
    flux1 = df1['Flux Phase 1'].to_list()
    flux2 = df1['Flux Phase 2'].to_list()
    flux3 = df1['Flux Phase 3'].to_list()
    colors = ['#2C2C2C','#C52626','#66A2EE']
    i = 0
    x = list()
    y = list()
    z = list()
    while i < 24:
        x.append ( np.cos((i+1)*np.pi/12) )
        y.append ( np.sin((i+1)*np.pi/12) )
        z.append(1)
        i+=1
    x.append ( np.cos(np.pi/12))
    y.append ( np.sin ( np.pi / 12))
    flux1.append (flux1[0])
    flux2.append (flux2[0])
    flux3.append (flux3[0])
    ax1 = plt.axes(projection = '3d')
    p1 = ax1.plot3D(x,y,flux1,colors[0] , label = "Phase 1")
    p2 = ax1.plot3D(x,y,flux2,colors[1] , label = "Phase 2")
    p3 = ax1.plot3D(x,y,flux3,colors[2] , label = "Phase 3")
    ax1.set_zlabel("Magnetic Flux Variation (mV)")
    ax1.grid(False)
    ax1.w_xaxis.pane.fill = False
    ax1.w_yaxis.pane.fill = False
    ax1.w_zaxis.pane.fill = False
    ax1.set_xticks([])
    ax1.set_yticks([])
    plt.legend()
    plt.title("Air-Gap Magnetic Flux Variation")
    plt.show()

######REFERENCES
#https://www.geeksforgeeks.org/three-dimensional-plotting-in-python-using-matplotlib/
#https://medium.com/@rohitadnaik/3d-line-plot-in-python-2fbeca99b9ba
#https://www.geeksforgeeks.org/use-different-y-axes-on-the-left-and-right-of-a-matplotlib-plot/
#https://jakevdp.github.io/PythonDataScienceHandbook/04.11-settings-and-stylesheets.html
#https://nicoguaro.github.io/posts/matplotlib_styles/
#https://github.com/matplotlib/matplotlib/blob/v3.4.1/matplotlibrc.template
#https://likegeeks.com/3d-plotting-in-python/

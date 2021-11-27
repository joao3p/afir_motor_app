###################################
# Author: João Pinto
# Title: Thesis Graph Analysis GUI
# Reference: https://realpython.com/pysimplegui-python/
###################################

###################################IMPORTS
from threading import local
from tkinter.constants import CENTER
from PySimpleGUI.PySimpleGUI import Canvas, Column
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from graphs_config import *
from graphs_analysis import *
from graphs_magnetic_flux import *
import os.path

###################################FUNCTIONS
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

###################################GUI
#LAYOUT AND VARIABLES
sg.theme('Dark Green 4')

params = [
    [sg.Text("Phases", pad = ((0,0), (10,7)))],
    [
        sg.Button("3", size = (6,1), pad = (2,2)), 
        sg.Button("6", size = (6,1), pad = (2,2)),
        sg.Button("12", size = (6,1), pad = (2,2))
    ],
    [sg.HSeparator(pad = ((0,0),(14,14)))],
    [
        sg.Text("Poles", key = "Poles"), 
        sg.In(size = (20,1), enable_events= True, key = "-POLES-")
    ],
    [sg.HSeparator(pad = ((0,0),(14,7)))],
    [sg.Text("Series Configurations", pad = ((0,0),(0,15)))],
    [
        sg.Button("1 Stator", size = (10,2), pad = ((0,0),(0,5))),
        #sg.Button("Consequent Poles", size = (10,2), pad = ((0,0),(0,5))),
        #sg.Button("Spiral Rolled", size = (10,2), pad = ((0,0),(0,5))),
        sg.Button("2 Stators", size = (10,2), pad = ((0,0),(0,5)))
    ],
    [sg.HSeparator(pad = ((0,0),(7,7)))],
    [sg.Text("Rotor Topology", pad = ((0,0), (0,10)))],
    [
        sg.Button("Aluminium at room temperature", size = (14,2), pad = ((0,0),(0,0)), key = "al"),
        sg.Button("Aluminium in LN2", size = (14,2), pad = ((0,0),(0,0)), key="al_ln2"),
        sg.Button("HTS in LN2", size = (14,2), pad = ((0,0),(0,0)),key="hts")
    ],
    [sg.HSeparator(pad = ((0,0),(14,14)))],
    [sg.Text("Analysis", pad = ((0,0), (0,7)))],
    [
        sg.Button("Basic Analysis Graph", size = (12,2), pad = ((5,5),(0,0)), button_color = ("#032b2b","#30a0a0"), key = "basic"), 
        sg.Button("Phasors Graph", size = (12,2), pad = ((5,5),(0,0)), button_color = ("#032b2b","#30a0a0"), key = "phasor"),
        sg.Button("Commutator Configuration", size = (12,2), pad = ((5,5),(0,0)), button_color = ("#032b2b","#30a0a0"), key = "config")
    ],
    [
        sg.Button("Magnetic Flux 2D", size = (14,2), pad = ((5,5),(10,10)), button_color = ("#032b2b","#30a0a0"), key = "flux_2d"),
        sg.Button("Magnetic Flux 3D", size = (14,2), pad = ((5,5),(10,10)), button_color = ("#032b2b","#30a0a0"), key = "flux_3d")
    ],
    [sg.Text("MIEEC FCT NOVA 2021", pad = ((0,0),(20,0)))],
    [sg.Text("João Pinto", pad = ((0,0),(0,10)))]
]

files = [
    [
        sg.Text("File Folder"),
        sg.In(size=(25, 1), enable_events=True, key="folder"),
        sg.FolderBrowse(size = (7,1))
    ],
    [
        sg.Text(size=(25,1), key = "path")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 24), key="list"
        )
    ],
]

final = [
    [sg.Text("AFIR HTS Motor Analysis App", font = 5, justification = "center", pad = (0,7))],
    [
        sg.Column(params, size = (380, 550), pad = ((15,20), (0,0)), element_justification = "center", justification="center"),
        sg.VSeparator(pad = (0,10)),
        sg.Column(files, element_justification = "center", justification="center")
    ]
]

layout = [
    [sg.Column(final, element_justification = "center")]
]

q = 0
pp = 0
phases = 0
stator = 1
config = ""
data_path = ""
topology = "Aluminium Rotor"

# Create the window
window = sg.Window("AFIR HTS Motor Analysis GUI", layout= layout, icon="htsmotor3.ico")

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "basic" or event == "phasor" or event == "config":
        #print(phases,pp,q,stator)
        if stator == 0 or phases == 0 or pp == 0:
            print("Define all three values: number of phases, poles, stators and configuration")
            sg.popup("Define all three values: number of phases, stators poles and configuraiton")
        else:
            if check_value(q,pp,phases): #function to check the configuration from graphs_config
                if event == "basic" and data_path != "":
                    make_analysis(data_path, phases, pp*2, q,stator,config,topology)
                elif event == "phasor" and data_path != "":
                    make_phasors(data_path, phases, pp*2, q,stator,config,topology)
                elif event == "config":
                    plot_configuration(q,pp,phases,stator)
                else:
                    print("Please select a file")
                    sg.popup("Please select a file")
            else:
                print("Configuration not defined sorry!")
                sg.popup("Configuration not defined sorry!")
    elif event == "flux_2d" or event == "flux_3d":
        if pp == 0:
            plot_2d_flux("flux tests "+str(pp*2)+" poles",1)
            plot_2d_flux("flux tests "+str(pp*2)+" poles",2)
            plot_2d_flux("flux tests "+str(pp*2)+" poles",3)
            plot_2d_flux("flux tests "+str(pp*2)+" poles",4)
        else:
            if pp in [1,2,4]: #function to check the configuration from graphs_config
                if event == "flux_2d":
                    plot_2d_flux("flux tests "+str(pp*2)+" poles",0)
                elif event == "flux_3d":
                    plot_3d_flux("flux tests "+str(pp*2)+" poles")
                else:
                    print("Please select a file")
                    sg.popup("Please select a file")
            else:
                print("Configuration not defined sorry!")
                sg.popup("Configuration not defined sorry!")
    elif event == '3':
        phases = 3
        window["3"].Update(button_color = ("#032b2b","#a1c5ab"))
        window["6"].Update(button_color = ("#a1c5ab","#032b2b"))
        window["12"].Update(button_color = ("#a1c5ab","#032b2b"))
    elif event == '6':
        phases = 6
        window["3"].Update(button_color = ("#a1c5ab","#032b2b"))
        window["6"].Update(button_color = ("#032b2b","#a1c5ab"))
        window["12"].Update(button_color = ("#a1c5ab","#032b2b"))
    elif event == '12':
        phases = 12
        window["3"].Update(button_color = ("#a1c5ab","#032b2b"))
        window["6"].Update(button_color = ("#a1c5ab","#032b2b"))
        window["12"].Update(button_color = ("#032b2b","#a1c5ab"))
    elif event == "-POLES-":
        if values['-POLES-']:
            if int(values['-POLES-']) in [2,4,8]:
                pp = int(int(values['-POLES-'])/2)
            else:
                pp = 0
                print("Incorrect value for number of poles\n Acceptable values: 2, 4 or 8")
                sg.Popup("Incorrect value for number of poles\n Acceptable values: 2,4,or8")
        else:
            pp = 0
    elif event == '1 Stator':
        q = 0.5
        stator = 1
        config = "1 Stator"
        window["1 Stator"].Update(button_color = ("#032b2b","#a1c5ab"))
        window["2 Stators"].Update(button_color = ('#a1c5ab','#032b2b'))
    elif event == '2 Stators':
        q = 0.5
        stator = 2
        config = "2 Stators Consequent Poles"
        window["1 Stator"].Update(button_color = ('#a1c5ab','#032b2b'))
        window["2 Stators"].Update(button_color = ("#032b2b","#a1c5ab"))
    elif event == 'al':
        topology = "Aluminium at room temperature"
        window["al"].Update(button_color = ("#032b2b","#a1c5ab"))
        window["al_ln2"].Update(button_color = ("#a1c5ab","#032b2b"))
        window["hts"].Update(button_color = ("#a1c5ab","#032b2b"))
    elif event == 'al_ln2':
        topology = "Aluminium in LN2"
        window["al"].Update(button_color = ("#a1c5ab","#032b2b"))
        window["al_ln2"].Update(button_color = ("#032b2b","#a1c5ab"))
        window["hts"].Update(button_color = ("#a1c5ab","#032b2b"))
    elif event == 'hts':
        topology = "HTS in LN2"
        window["al"].Update(button_color = ("#a1c5ab","#032b2b"))
        window["al_ln2"].Update(button_color = ("#a1c5ab","#032b2b"))
        window["hts"].Update(button_color = ("#032b2b","#a1c5ab"))
    elif event == sg.WIN_CLOSED:
        break
    if event == "folder":
        folder = values["folder"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".xlsx"))
        ]
        window["list"].update(fnames)
    if event == "list":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["folder"], values["list"][0]
            )
            data_path = filename
            window["path"].update(filename)
        except:
            pass
    if values['-POLES-']:
        window["Poles"].Update(text_color = ('#30a0a0'))
    else:
        window["Poles"].Update(text_color = ('#a1c5ab'))

window.close()

#####################################REFERENCES
#https://realpython.com/pysimplegui-python/
#https://pysimplegui.readthedocs.io/en/latest/cookbook/
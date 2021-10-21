

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:38:38 2020

@author: lpeka
"""


import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize
import os
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import lumicks.pylake as lk

##To avoid blurry GUI - DPI scaling##
import ctypes
awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)


## define the functions used in the GUI  

def getCSV ():
    global df
    global F
    global PD_nm
    global filename
    import_file_path = filedialog.askopenfilename()
    df = pd.read_csv (import_file_path)
    #print (df)
    PD=df.iloc[:,1] # to select only certain part of the imported table [Row,column]
    F=df.iloc[:,0]
    PD_nm=PD
    filename=os.path.basename(import_file_path)
    global fig1
    global figure1
    global subplot1

    figure1 = Figure(figsize=(6,6), dpi=100) 
    subplot1 = figure1.add_subplot(111) 
    #xAxis = PD_nm 
    #yAxis = F
    entryText_shift_d.set( "0" ) 
    entryText_shift_F.set( "0" ) 
    entryText_ds_Lp.set( "40" )
    entryText_ds_Lc.set( "1256" )
    entryText_ss_Lc.set( "0" )
    entryText_ss_Lp.set( "1" )
    entryText_ss_St.set( "800" ) 
    entryText_ds_St.set( "400" ) 
    


    subplot1.set_xlabel("Distance [$\\mu$m]")
    subplot1.set_ylabel("Force [pN]")
    subplot1.plot(PD_nm, F, color='gray') 
    subplot1.tick_params('both', direction='in')
    subplot1.set_ylim([0,max(F)])
    subplot1.set_xlim([min(PD_nm)-10,max(PD_nm)+10])
    fig1 = FigureCanvasTkAgg(figure1, frame) 
   
    fig1.get_tk_widget().grid(row=0, column=0, sticky='wens')
    #tkagg.NavigationToolbar2TkAgg(fig1, frame)
    toolbarFrame = tk.Frame(master=frame)
    toolbarFrame.grid(row=2,column=0)
    toolbar = NavigationToolbar2Tk(fig1, toolbarFrame)
    

def create_chart():
    global fig1
    figure1 = Figure(figsize=(6,6), dpi=100) 
    subplot1 = figure1.add_subplot(111) 
    #xAxis = PD_nm 
    #yAxis = F

    subplot1.set_xlabel("Distance [$\\mu$m]")
    subplot1.set_ylabel("Force [pN]")
    subplot1.plot(PD_nm, F, color='gray') 
    subplot1.tick_params('both', direction='in')
    subplot1.set_ylim([0,max(F)])
    subplot1.set_xlim([min(PD_nm)-10,max(PD_nm)+10])
    
    fig1 = FigureCanvasTkAgg(figure1, frame) 
    fig1.get_tk_widget().grid(row=0, column=0, sticky='wens')
    
    toolbarFrame = tk.Frame(master=frame)
    toolbarFrame.grid(row=2,column=0)
    toolbar = NavigationToolbar2Tk(fig1, toolbarFrame)

def start_click():
    global cid
    cid=fig1.mpl_connect('button_press_event', onclick_start) 
    
    
def end_click():
    global cid
    cid=fig1.mpl_connect('button_press_event', onclick_end)
     
    
    
    
def onclick_start(event):
    global cid
    
    PD_position, F_position = float(event.xdata), float(event.ydata)
    print (PD_position, F_position)
    entryText_start.set(round(PD_position, 1)) 
    fig1.mpl_disconnect(cid) 
    
    
def onclick_end(event):
    global cid
    
    PD_position, F_position = float(event.xdata), float(event.ydata)
    print (PD_position, F_position)
    entryText_end.set(round(PD_position, 1)) 
    fig1.mpl_disconnect(cid)  

def clear_charts():
    fig1.get_tk_widget().grid_forget()
    
def clear_table():
    global listBox
    list_items=listBox.get_children("")
    
    for item in list_items:
        listBox.delete(item)
    
def clear_table_last():
    global listBox
    list_items=listBox.get_children("")
    
    
    listBox.delete(list_items[-1])



## fitting the ds handle part

def fitting_ds(PD_ds, F_ds, Lc_ds, Lc_range):
    model_ds=lk.inverted_odijk("DNA").subtract_independent_offset() + lk.force_offset("DNA")

    fit_ds=lk.FdFit(model_ds)

    fit_ds.add_data("ds_part",  F_ds,PD_ds)
    # Persistance length bounds
    fit_ds["DNA/Lp"].value = float(entryText_ds_Lp.get())
    fit_ds["DNA/Lp"].lower_bound = 15
    fit_ds["DNA/Lp"].upper_bound = 80
    # Force shift bounds
    fit_ds["DNA/f_offset"].value=float(entryText_shift_F.get())
    fit_ds["DNA/f_offset"].upper_bound=3
    fit_ds["DNA/f_offset"].lower_bound=0
    # distance shift bounds
    fit_ds["DNA/d_offset"].value=float(entryText_shift_d.get())
    fit_ds["DNA/d_offset"].upper_bound=300
    fit_ds["DNA/d_offset"].lower_bound=-300
    # stiffnes
    fit_ds["DNA/St"].value = float(entryText_ds_St.get())
    fit_ds["DNA/St"].lower_bound = float(entryText_ds_St.get())-50
    fit_ds["DNA/St"].upper_bound = float(entryText_ds_St.get())+50


    # contour length
    Lc_initial_guess= Lc_ds # nm
    fit_ds["DNA/Lc"].upper_bound=Lc_initial_guess+Lc_range
    fit_ds["DNA/Lc"].lower_bound=Lc_initial_guess-Lc_range
    fit_ds["DNA/Lc"].value = Lc_initial_guess
    fit_ds["DNA/Lc"].unit='nm'

    # d shift bounds
    #fit_ds["DNA/d_offset"].upper_bound=Lc_initial_guess/250
    #fit_ds["DNA/d_offset"].lower_bound=-Lc_initial_guess/250
    fit_ds.fit()

    print(fit_ds["DNA/Lc"].value)

    Fit_dict={'model':model_ds,'fit_model':fit_ds,'Lc':fit_ds["DNA/Lc"].value, 'Lp':fit_ds["DNA/Lp"].value, 'St':fit_ds["DNA/St"].value, 'f_offset':fit_ds["DNA/f_offset"].value, 'd_offset':fit_ds["DNA/d_offset"].value }
    return Fit_dict



def fitting_ss(PD_ss, F_ss, Ds_fit_dict, fix, max_range):

    model_ss = lk.odijk("DNA_2") + lk.odijk("RNA")

    model_ss = model_ss.invert().subtract_independent_offset() + lk.force_offset("DNA")
    fit_ss=lk.FdFit(model_ss)

    fit_ss.add_data("ss_part", F_ss, PD_ss)

    ## ds part parameters

    # Persistance length bounds
    
    #Lp_ds_range=fit_ds["DNA/Lp"].value/10
    fit_ss["DNA_2/Lp"].value = Ds_fit_dict['Lp']
    fit_ss["DNA_2/Lp"].lower_bound = Ds_fit_dict['Lp']*(1-max_range/100)
    fit_ss["DNA_2/Lp"].upper_bound = Ds_fit_dict['Lp']*(1+max_range/100)
    #if fix==1:
    fit_ss["DNA_2/Lp"].fixed = 'True'
    fit_ss["DNA/f_offset"].upper_bound=5
    fit_ss["DNA/f_offset"].lower_bound=-5
    fit_ss["DNA/f_offset"].value=Ds_fit_dict['f_offset']
    fit_ss["DNA/f_offset"].fixed='True'
    
    
    fit_ss["inv(DNA_2_with_RNA)/d_offset"].value=Ds_fit_dict['d_offset']
    fit_ss["inv(DNA_2_with_RNA)/d_offset"].fixed='True'
    
    
    # contour length

    #Lc_ds_range=Lc_initial_guess/100 # nm
    fit_ss["DNA_2/Lc"].upper_bound=Ds_fit_dict['Lc']*(1+max_range/100)
    fit_ss["DNA_2/Lc"].lower_bound=Ds_fit_dict['Lc']*(1-max_range/100)
    fit_ss["DNA_2/Lc"].value = Ds_fit_dict['Lc']
    fit_ss["DNA_2/Lc"].unit='nm'
    #if fix==1:
    fit_ss["DNA_2/Lc"].fixed = 'True'

    # stifness

    fit_ss["DNA_2/St"].upper_bound=Ds_fit_dict['St']*(1+max_range/100)
    fit_ss["DNA_2/St"].lower_bound=Ds_fit_dict['St']*(1-max_range/100)
    fit_ss["DNA_2/St"].value = Ds_fit_dict['St']
    if fix==1:
        fit_ss["DNA_2/St"].fixed = 'True'
   
    
   ## ss part parameters

    # Persistance length bounds

    fit_ss["RNA/Lp"].value = float(entryText_ss_Lp.get())
    fit_ss["RNA/Lp"].lower_bound =0.8
    fit_ss["RNA/Lp"].upper_bound =2
    if fix==1:
        fit_ss["RNA/Lp"].fixed = 'True'
    
    # stiffnes
    fit_ss["RNA/St"].value = float(entryText_ss_St.get())
    fit_ss["RNA/St"].lower_bound = 300
    fit_ss["RNA/St"].upper_bound = 1500
    # contour length

   

    fit_ss["RNA/Lc"].upper_bound=150
    fit_ss["RNA/Lc"].lower_bound=0
    fit_ss["RNA/Lc"].value = float(entryText_ss_Lc.get())
    fit_ss["RNA/Lc"].unit='nm'

    fit_ss.fit()

    
    
    Fit_dict={'model':model_ss, 'fit_model':fit_ss, 'Lc_ds':fit_ss["DNA_2/Lc"].value, 'Lp_ds':fit_ss["DNA_2/Lp"].value, 'St_ds':fit_ss["DNA_2/St"].value, 'Lc_ss':fit_ss["RNA/Lc"].value, 'Lp_ss':fit_ss["RNA/Lp"].value, 'St_ss':fit_ss["RNA/St"].value, 'f_offset':fit_ss["DNA/f_offset"].value, 'd_offset':fit_ss["inv(DNA_2_with_RNA)/d_offset"].value}
    return Fit_dict



def Fitting_WLC_ds_handles():
    #create a sublist of the ROI PD_nm
    global Fit_ds
    global F_region
    global PD_nm
    global F_ds_model
    global distance
    global real_start, real_end
    #find match with PD
    real_PD=[]
    start_PD=float(entry_start.get())
    end_PD=float(entry_end.get())
    for i in [start_PD, end_PD]:
        absolute_difference_function = lambda cPD : abs(cPD- i)
        real_PD.append(min(PD_nm, key=absolute_difference_function))
    #print(real_PD)
    
    
    
    
    PD_nm_list=list(PD_nm)

    real_start=PD_nm_list.index(real_PD[0])
    real_end=PD_nm_list.index(real_PD[1])

      
    
    PD_region=[]
    F_region=[]
    if real_start<real_end:   
        for i in range(real_start,real_end, 10):
            PD_region.append(PD_nm[i])
            F_region.append(F[i])
        
    else:
        for i in range(real_end,real_start, 10):
            PD_region.append(PD_nm[i])
            F_region.append(F[i])

    #print(len(PD_region))
    #print(len(F_region))
    
    #fitting itself
    Lc_ds=float(entryText_ds_Lc.get())
    Lc_range=5
    Fit_ds=fitting_ds(PD_region, F_region, Lc_ds, Lc_range)
    entryText_ds_Lp.set(Fit_ds['Lp'])
    entryText_shift_F.set(Fit_ds['f_offset'])
    entryText_shift_d.set(Fit_ds["d_offset"])
    entryText_ds_Lc.set(Fit_ds['Lc'])
    entryText_ds_St.set(Fit_ds['St'])  
  
    # plot the marked region and fitted WLC
    global fig1
    global figure1
    global subplot1
       # model data
    distance = np.arange(min(PD_nm), max(PD_nm)+50, 2)
    F_ds_model=Fit_ds['model'](distance,Fit_ds['fit_model'])
    
    
    subplot1.clear()
    subplot1.set_xlabel("Distance [$\\mu$m]")
    subplot1.set_ylabel("Force [pN]")
    subplot1.plot(PD_nm, F, color='gray') 
    if real_start<real_end:
        subplot1.plot(PD_nm[real_start: real_end], F[real_start:real_end],color="b")
    else:
        subplot1.plot(PD_nm[real_end:real_start ], F[real_end:real_start],color="b")        
    subplot1.plot(distance,F_ds_model , marker=None,linestyle='dashed',linewidth=1,color="black")
    subplot1.set_ylim([0,max(F)])
    subplot1.set_xlim([min(PD_nm)-10,max(PD_nm)+10])
    subplot1.tick_params('both', direction='in')

    
    fig1 = FigureCanvasTkAgg(figure1, frame) 
    fig1.get_tk_widget().grid(row=0, column=0)
    
    toolbarFrame = tk.Frame(master=frame)
    toolbarFrame.grid(row=2,column=0)
    toolbar = NavigationToolbar2Tk(fig1, toolbarFrame)
    # add the parameters to table 
    global listBox
    listBox.insert("", "end", values=(filename, start_PD, end_PD, entry_ds_Lc.get(), entry_ds_Lp.get(), entry_ds_St.get(),entry_ss_Lc.get(), entry_ss_Lp.get(), entry_ss_St.get(), entry_shift_d.get(), entry_shift_F.get()))




## fitting the ss RNA part combined with ds handles part

def Fitting_WLC_ss_handles():
    #create a sublist of the ROI PD_nm
    global Fit_ds
    global F_region
    global PD_nm
    global F_ss_model
    global distance 
    #find match with PD
    real_PD=[]
    start_PD=float(entry_start.get())
    end_PD=float(entry_end.get())
    for i in [start_PD, end_PD]:
        absolute_difference_function = lambda cPD : abs(cPD- i)
        real_PD.append(min(PD_nm, key=absolute_difference_function))
    #print(real_PD)
    
    
    
    
    PD_nm_list=list(PD_nm)
    real_start=PD_nm_list.index(real_PD[0])
    real_end=PD_nm_list.index(real_PD[1])
 
    PD_region=[]
    F_region=[]
    if real_start<real_end:   
        for i in range(real_start,real_end, 200):
            PD_region.append(PD_nm[i])
            F_region.append(F[i])
        
    else:
        for i in range(real_end,real_start, 200):
            PD_region.append(PD_nm[i])
            F_region.append(F[i])
    
    #print(len(PD_region))
    #print(len(F_region))
    
    #fitting itself
  

    Fit_ss=fitting_ss(PD_region, F_region,Fit_ds, 1, 1)
    entryText_ds_Lp.set(Fit_ss['Lp_ds'])
    entryText_shift_F.set(Fit_ss['f_offset'])
    entryText_shift_d.set(Fit_ss["d_offset"])
    entryText_ds_Lc.set(Fit_ss['Lc_ds'])
    entryText_ss_Lc.set(Fit_ss['Lc_ss'])
    entryText_ss_Lp.set(Fit_ss['Lp_ss'])    
    entryText_ss_St.set(Fit_ss['St_ss'])  
    entryText_ds_St.set(Fit_ss['St_ds'])      

   # model data
    #distance = np.arange(min(PD_nm), max(PD_nm), 1)
    F_ss_model=Fit_ss['model'](distance,Fit_ss['fit_model'])
    # plot the marked region and fitted WLC
    global fig1
    global figure1
    global subplot1
    
    #subplot1.clear()
    #subplot1.set_xlabel("Distance (um)")
    #subplot1.set_ylabel("Force (pN)")
    #subplot1.scatter(PD_nm, F, marker='.' , s=0.05 ,linewidths=None) 
    if real_start<real_end:
        subplot1.plot(PD_nm[real_start: real_end], F[real_start:real_end],color="r")
    else:
        subplot1.plot(PD_nm[real_end:real_start ], F[real_end:real_start],color="r")   
    subplot1.plot(distance,F_ss_model , marker=None,linewidth=1, linestyle='dashed',color="black")

    subplot1.set_ylim([0,max(F)])
    subplot1.set_xlim([min(PD_nm)-10,max(PD_nm)+10])
    
    
    fig1 = FigureCanvasTkAgg(figure1, frame) 
    fig1.get_tk_widget().grid(row=0, column=0)
    
    toolbarFrame = tk.Frame(master=frame)
    toolbarFrame.grid(row=2,column=0)
    toolbar = NavigationToolbar2Tk(fig1, toolbarFrame)
    # add the parameters to table 
    global listBox
    listBox.insert("", "end", values=(filename, start_PD, end_PD, entry_ds_Lc.get(), entry_ds_Lp.get(), entry_ds_St.get(),entry_ss_Lc.get(), entry_ss_Lp.get(), entry_ss_St.get(), entry_shift_d.get(), entry_shift_F.get()))
   


def export_data():
    global listBox
    global name
    global Fit_results
    ''' exporting the table results '''
    results=[]
    for child in listBox.get_children():
  
        results.append(listBox.item(child)['values'])
   
        
    Fit_results = pd.DataFrame(results, 
               columns =['Filename',
                         'Fit start',
                         'Fit end',
                         'ds Contour length',
                         'ds Persistance Length',
                         'ds St',
                         'ss Contour Length',
                         'ss Persistance Length',
                         'ss St',
                         'Shift x',
                         'Shift F',
                         ])  
    
    name=filedialog.asksaveasfile(mode='w',defaultextension=".csv")
    print(name)
    Fit_results.to_csv(name.name, index=False, header=True)  
    
    ''' exporting ds and ss model '''
    try:
        F_ss_model
        model_data=pd.DataFrame(list(zip(distance, F_ds_model, F_ss_model)), columns=['Distance [nm]', 'Force WLC data [pN]', 'Force WLC+FJC data [pN]'])
    except NameError:
        
        model_data=pd.DataFrame(list(zip(distance, F_ds_model)), columns=['Distance [nm]', 'Force WLC data [pN]'])
    name_model=name.name[:-4]+'_model_data.csv'
    model_data.to_csv(name_model, index=False, header=True)

    ''' exporting figure '''
    plotname = name.name[:-4]+'_graph.png'
    figure1.savefig(plotname, dpi=600)
    
    
    
## create the window and widgets 
root= tk.Tk()

root.columnconfigure([0,1],weight=1, minsize=75)
root.rowconfigure(0,weight=1, minsize=50)
  
canvas1 = tk.Canvas(root, width = 400, height = 600)
canvas1.grid(row=0, column=1)

frame = tk.Frame(root,   width=400, height=600) 
frame.grid(row=0, column=0)

frame_table=tk.Frame(root, width=400, height=100)
frame_table.grid(row=1, column=0)



# shift in x 

label_shift_d = tk.Label(root, text='Shift x [nm]')
label_shift_d.config(font=('Arial', 10))
canvas1.create_window(100, 160, window=label_shift_d)

entryText_shift_d = tk.StringVar()   
entry_shift_d = tk.Entry (root, textvariable=entryText_shift_d)
canvas1.create_window(100, 180, window=entry_shift_d) 
entryText_shift_d.set( "0" ) 


# shift in F

label_shift_F = tk.Label(root, text='shift F [pN]')
label_shift_F.config(font=('Arial', 10))
canvas1.create_window(300, 160, window=label_shift_F)

entryText_shift_F = tk.StringVar()  
entry_shift_F = tk.Entry (root, textvariable=entryText_shift_F)
canvas1.create_window(300, 180, window=entry_shift_F) 
entryText_shift_F.set( "0" ) 

# K0 for both 
#ds
label_ds_St = tk.Label(root, text='K0 ds (St)')
label_ds_St.config(font=('Arial', 10))
canvas1.create_window(100, 200, window=label_ds_St)

entryText_ds_St = tk.StringVar()  
entry_ds_St = tk.Entry (root, textvariable=entryText_ds_St)
canvas1.create_window(100, 220, window=entry_ds_St) 
entryText_ds_St.set( "800" ) 

#ss
label_ss_St = tk.Label(root, text='K0 ss (St)')
label_ss_St.config(font=('Arial', 10))
canvas1.create_window(300, 200, window=label_ss_St)

entryText_ss_St = tk.StringVar()  
entry_ss_St = tk.Entry (root, textvariable=entryText_ss_St)
canvas1.create_window(300, 220, window=entry_ss_St) 
entryText_ss_St.set( "800" ) 


## ds handle part

# ds handle persistance length 

label_ds_Lp = tk.Label(root, text='dsHandles Lp [nm]')
label_ds_Lp.config(font=('Arial', 10))
canvas1.create_window(100, 240, window=label_ds_Lp)

entryText_ds_Lp = tk.StringVar()    
entry_ds_Lp = tk.Entry (root, textvariable=entryText_ds_Lp)
canvas1.create_window(100, 260, window=entry_ds_Lp) 
entryText_ds_Lp.set( "40" )

# ds handle  contour length 

label_ds_Lc = tk.Label(root, text='dsHandles Lc [nm]')
label_ds_Lc.config(font=('Arial', 10))
canvas1.create_window(100, 290, window=label_ds_Lc)

entryText_ds_Lc = tk.StringVar()    
entry_ds_Lc = tk.Entry (root, textvariable=entryText_ds_Lc)
canvas1.create_window(100, 310, window=entry_ds_Lc) 
entryText_ds_Lc.set( "1231" )



## ss RNA part 

# ss RNA persistance length 

label_ss_Lp = tk.Label(root, text=' ssRNA Lp [nm]')
label_ss_Lp.config(font=('Arial', 10))
canvas1.create_window(300, 240, window=label_ss_Lp)

entryText_ss_Lp = tk.StringVar()    
entry_ss_Lp = tk.Entry (root, textvariable=entryText_ss_Lp)
canvas1.create_window(300, 260, window=entry_ss_Lp) 
entryText_ss_Lp.set( "1" )

# ss RNA contour length 


label_ss_Lc = tk.Label(root, text=' ssRNA Lc [nm]')
label_ss_Lc.config(font=('Arial', 10))
canvas1.create_window(300, 290, window=label_ss_Lc)

entryText_ss_Lc = tk.StringVar()    
entry_ss_Lc = tk.Entry (root, textvariable=entryText_ss_Lc)
canvas1.create_window(300, 310, window=entry_ss_Lc) 
entryText_ss_Lc.set( "0" )








# start position
entryText_start = tk.StringVar()    
entry_start = tk.Entry (root, textvariable=entryText_start)
canvas1.create_window(250, 350, window=entry_start,width=50, height=20) 




# end position

entryText_end = tk.StringVar()    
entry_end = tk.Entry (root, textvariable=entryText_end)
canvas1.create_window(250, 390, window=entry_end, width=50, height=20) 


     



## create button widgets that use the defined functions


browseButton_CSV = tk.Button(root,text="      Import CSV File     ", command=getCSV, bg='green', fg='white', font=('Arial', 11, 'bold'))
canvas1.create_window(200, 50, window=browseButton_CSV) 
           
button_create = tk.Button (root, text=' Create Charts ', command=create_chart, bg='palegreen2', font=('Arial', 11, 'bold')) 
canvas1.create_window(200, 90, window=button_create)

button_clear = tk.Button (root, text='  Clear Charts  ', command=clear_charts, bg='lightskyblue2', font=('Arial', 11, 'bold'))
canvas1.create_window(200, 130, window=button_clear)

button_start = tk.Button (root, text='Set start', command=start_click, bg='lightsteelblue2', font=('Arial', 11, 'bold'))
canvas1.create_window(150, 350, window=button_start)

button_end = tk.Button (root, text='Set end', command=end_click, bg='lightsteelblue2', font=('Arial', 11, 'bold'))
canvas1.create_window(150, 390, window=button_end)

button_fit_Lp_shift_x = tk.Button (root, text='Fit ds Lp & shift_x', command=Fitting_WLC_ds_handles, bg='PeachPuff', font=('Arial', 10, 'bold'))
canvas1.create_window(100, 450, window=button_fit_Lp_shift_x, width=150)

#button_fit_Lp = tk.Button (root, text='Fit ds Lp', command=[], bg='PeachPuff', font=('Arial', 10, 'bold'))
#canvas1.create_window(200, 450, window=button_fit_Lp, width=90)

button_fit_Lc = tk.Button (root, text='Fit ss Lc', command=Fitting_WLC_ss_handles, bg='PeachPuff', font=('Arial', 10, 'bold'))
canvas1.create_window(300, 450, window=button_fit_Lc, width=90)

button_export = tk.Button (root, text='Export', command=export_data, bg='palegreen2', font=('Arial', 14, 'bold'))
canvas1.create_window(100, 550, window=button_export)

button_clear_last = tk.Button (root, text='Delete last', command=clear_table_last, bg='red', font=('Arial', 10, 'bold'))
canvas1.create_window(250, 520, window=button_clear_last)

button_clear_table = tk.Button (root, text='Delete all', command=clear_table, bg='red', font=('Arial', 10, 'bold'))
canvas1.create_window(250, 600, window=button_clear_table)

## show the fitting parameters in a table
# create Treeview with 3 columns
cols = ('Filename', 'Fit start', 'Fit end', 'ds Lc', 'ds Lp','ds St',  'ss Lc', 'ss Lp', 'ss St','Shift x', 'Shift F')
listBox = ttk.Treeview(frame_table, columns=cols, show='headings', height=5)
# set column headings
for col in cols:
    listBox.heading(col, text=col)  
    listBox.column(col,  minwidth=0, width=80)
listBox.grid(row=1, column=0, columnspan=1, padx=5, pady=5)


# navigation toolbar



## loop ensuring the GUI is running until closed
 
root.mainloop()
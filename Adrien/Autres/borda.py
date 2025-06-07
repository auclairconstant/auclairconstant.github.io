# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 11:20:17 2025

@author: Etudiants
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.optimize
from scipy.signal import find_peaks

def moyenne_glissante(tab,fenetre):
    new_tab = []
    for i in range(len(tab)):
        a = max(0,i-fenetre)
        b = min(i+fenetre,len(tab)-1)
        new_tab.append(np.mean(tab[a:b]))
    return new_tab

def portrait_phase(name):

    data = []
    
    with open(name) as csvfile:
    
        data_line = csv.reader(csvfile, delimiter=';')
    
        for row in data_line:
    
            data.append(row)
    
    theta = []
    time = []
    
    for i in range(1,len(data)):
        time.append(float(data[i][0].replace(',','.')))
        theta.append(float(data[i][1].replace(',','.')))
    
    # plt.plot(time,theta)
    
    theta_point = []
    for i in range(len(theta)-1):
        theta_point.append((theta[i+1]-theta[i])/(time[i+1]-time[i]))
    
    theta_point_avg = moyenne_glissante(theta_point,30)
    
    # plt.figure()
    # plt.plot(time[:-1],theta_point)
    # plt.grid()
    # plt.plot(time[:-1],theta_point_avg)
    
    return np.array(theta[:-1]),np.array(theta_point_avg)

def get_list_file(path,ending = ['.csv','.txt']):
    list_temp = os.listdir(path)
    return [i for i in list_temp if i[-4:] in ending]

#%% Portrait de phase

cwd = os.getcwd()
list_file = get_list_file(cwd)

theta = [6.25,33.4,35.8,42.8]

plt.figure()
plt.grid()
plt.axis('equal')
    
for i in range(len(list_file)):
    a,b = portrait_phase(list_file[i])

    label_plot = r'$\theta_0=$'+str(theta[i])+'°'
    # plt.plot(theta[:-1],theta_point)
    plt.plot(a,b,label=label_plot)
    plt.plot(a+360,b,'k')
    plt.plot(a-360,b,'k')
    

plt.xlabel(r'$\theta$')   
plt.ylabel(r'$\frac{d\theta}{dt}$')  
plt.legend()
    
    
    
    
    
    
    
    
    
    
    
    
    
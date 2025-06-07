# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 14:52:39 2025

@author: Adrien Dangremont
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize


def lire_txt(name): 
    longueur_onde = []
    intensite = []
    with open(os.path.join(os.getcwd(),name)) as f:
            data=f.readlines()
    for i in range(17,len(data)-1):
        line = data[i].replace(',','.').replace('\n','').split('\t')
        longueur_onde.append(float(line[0]))
        intensite.append(float(line[1]))
    return longueur_onde,intensite

def lambda_to_freq(l):
    c = 299792458
    return [c/(l[i]*10**-9) for i in range(len(l))]  

def fit_lin(x,a,b):
    return -a/x+b

name = 'spectre_qi.txt'
l_qi,i_qi = lire_txt(name)
freq_qi = lambda_to_freq(l_qi)


plt.figure()
plt.plot(freq_qi,i_qi,'r-')    
    

name = 'spectre_soleil.txt'
l_soleil,i_soleil = lire_txt(name)
freq_soleil = lambda_to_freq(l_soleil)
  
plt.figure()
plt.plot(freq_soleil,i_soleil,'g-')    
plt.show()


i_min = 10
i_max = 2500

y_fit = [np.log((l_soleil[i]*10**-9)**5*i_soleil[i]) for i in range(i_min,i_max)]
result = scipy.optimize.curve_fit(fit_lin,l_soleil[i_min:i_max],y_fit)

# print(result)

h = 6.626 * 10**-34
c = 299792458
kb = 1.380*10**-23


T_soleil = 5772
T_mes = (h*c)/(kb*result[0][0])*10**9
incert_mes = T_mes * (np.sqrt(result[1][0][0])/result[0][0])
print('Température du Soleil =' ,T_mes,' K')
print('Incertitude =' ,incert_mes,' K')
# print('z_score =' ,(T_soleil-T_mes)/incert_mes)


plt.figure()
plt.plot([1/l_soleil[i] for i in range(i_min,i_max)],y_fit)
plt.plot([1/l_soleil[i] for i in range(i_min,i_max)],[fit_lin(l_soleil[i],result[0][0],result[0][1]) for i in range(i_min,i_max)])

#%%

y_fit = [np.log((l_qi[i]*10**-9)**5*i_qi[i]) for i in range(i_min,i_max)]
result = scipy.optimize.curve_fit(fit_lin,l_qi[i_min:i_max],y_fit)

# print(result)

h = 6.626 * 10**-34
c = 299792458
kb = 1.380*10**-23

i_min = 10
i_max = 2500

T_mes = (h*c)/(kb*result[0][0])*10**9
incert_mes = T_mes * (np.sqrt(result[1][0][0])/result[0][0])
print('Température de la lampe =' ,T_mes,' K')
print('Incertitude =' ,incert_mes,' K')



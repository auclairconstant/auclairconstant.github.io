# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 10:20:15 2025

@author: Adrien Dangremont
"""

import numpy as np
import os
import matplotlib.pyplot as plt

import scipy.optimize

#%% Oscillateur de Wien

droite1 = [46.4,-127]
droite2 = [-46.5,168]

def calc_fo_wien(d1=droite1,d2=droite2):
    return 10**((d2[1]-d1[1])/(d1[0]-d2[0]))

print(calc_fo_wien())

name = 'wien_transitoire.txt'

time = []
tension = []

with open(os.path.join(os.getcwd(),name)) as f:
        data=f.readlines()
for i in range(1,len(data)):
    line = data[i].replace('\n','').split(' ')
    time.append(float(line[0]))
    tension.append(float(line[2]))


crete = [tension[0] for i in range(len(tension))]
a = tension[0]
for i in range(1,len(time)):
    if tension[i] >= a:
        crete[i] = tension[i]
        a = tension[i]
        # print(a)
    else:
        crete[i] = crete[i-1]
        
  
# plt.figure()
# plt.plot(time,tension)
# plt.plot(time,crete,'r-')

def exponentiel(x,a,b,C):
    return C*np.exp((x+b)/a)

i_min = 20000
i_max = 37500

# plt.figure()
# plt.plot(time,tension)
# plt.plot(time,crete,'r-')
# plt.plot(time[i_min:i_max],crete[i_min:i_max],'g-')
# plt.show() 

result = scipy.optimize.curve_fit(exponentiel,time[i_min:i_max],crete[i_min:i_max])
# print(result)

crete_fit = [exponentiel(time[i+i_min],result[0][0],result[0][1],result[0][2]) for i in range(len(time[i_min:i_max]))]

plt.figure()
plt.plot(time[i_min:i_max],crete[i_min:i_max],'g-')
plt.plot(time[i_min:i_max],crete_fit,'r-')
plt.show()

tau = -result[0][0]
print('Tau (en s) =',tau)
omega_0 = 1540*2*np.pi
alpha = 1/(tau*omega_0)
print('Alpha =',alpha)
rapport = 2*(1-alpha)
print('Rapport R2/R1 =',rapport)

#%% Chaleur latente de l'azote


masse_str = "2091.21;2083.08;2074.4;2065.88;2057.4;2048.95;2040.38;2031.87;2023.68;2015.13;2006.77;1998.3;1989.88;1981.5;1973.2;1964.6;1956.67;1948.32;1940.12;1931.6;1923.2;1913.92;1911.18;1908.32;1905.44;1902.62;1899.76;1896.8;1893.94;1890.91;1888.1;1885.21;1882.21;1879.3;1876.37;1873.5;1870.51;1867.62;1864.6;1861.8;1858.13;1856.3"

temps_str = "0;30;60;90;120;150;180;210;240;270;300;330;360;390;420;450;480;510;540;570;600;660;690;720;750;780;810;840;870;900;930;960;990;1020;1050;1080;1110;1140;1170;1200;1230;1260"

P_1 = 54.2*97.9
P_2 = 30.52*55.1

masse_temp = masse_str.split(';')
temps_temp = temps_str.split(';')

masse = [float(masse_temp[i]) for i in range(len(masse_temp))]
temps = [float(temps_temp[i]) for i in range(len(temps_temp))]

m_err = [0.05 for i in range(len(masse))]
t_err = [1 for i in range(len(temps))]

def lin_fit(x,a,b):
    return a*x+b

result_1 = scipy.optimize.curve_fit(lin_fit,temps[:21],masse[:21])
result_2 = scipy.optimize.curve_fit(lin_fit,temps[21:],masse[21:])

t1 = np.linspace(-10,610,10)
t2 = np.linspace(650,1310,10)

m1 = result_1[0][0]*t1+result_1[0][1]
m2 = result_2[0][0]*t2+result_2[0][1]

plt.figure()
plt.errorbar(temps, masse, yerr=m_err,xerr=t_err,marker='.',color='k',ls='', capsize=3)
plt.plot(t1,m1,'r--')
plt.plot(t2,m2,'r--')
plt.xlabel("Temps (en s)")
plt.ylabel("Masse (en g)")
plt.grid()
plt.show()


L_vap = (P_2-P_1)/(result_1[0][0]-result_2[0][0])/100
print('Chaleur latente de l\'eau = ', L_vap)
L_vap_inc = 2*L_vap * np.sqrt(2*(np.sqrt(result_1[1][0][0])/result_1[0][0])**2)
print('Incertitude = ', L_vap_inc)
L_tab = 199.2
print("z_score = ",(-L_vap+L_tab)/L_vap_inc)


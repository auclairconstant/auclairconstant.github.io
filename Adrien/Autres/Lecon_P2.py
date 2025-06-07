# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 09:14:54 2024

@author: Francois R. KAMAL YOUSSEF
"""
import numpy as np
import matplotlib.pyplot as plt

def interpol_lin(ref_x,ref_y,data_x):
    ###Fonction de transposition par interpolation linéaire
    ##Crée data_y, transposition de ref_y sur un tableau de taille data_x
    #ref_x et data_x ont la même dimension
    #ref_y et data_y ont la même dimension
    #ref_x et ref_y ont la même longueur
    #data_x et data_y ont la même longueur
    
    data_y=[];
    if ref_x[-1]-ref_x[0] > 0:
        mode = 0
    else:
        mode = 1
    for k in range(len(data_x)):
        count = 0;
        if mode == 0:
            while count < len(ref_x) and  data_x[k] > ref_x[count]:
                count += 1;
        elif mode == 1:
            while count < len(ref_x) and  data_x[k] < ref_x[count]:
                count += 1;
        count = min(count,len(ref_x)-1);
        if count == 0:
            data_y.append(ref_y[count]);
        else:
            if ref_x[count-1]-ref_x[count] != 0:
                alpha = (ref_y[count-1]-ref_y[count])/(ref_x[count-1]-ref_x[count]);
                beta = (ref_x[count-1]*ref_y[count]-ref_x[count]*ref_y[count-1])/(ref_x[count-1]-ref_x[count]);
                value_inter = alpha*data_x[k]+beta;
            else:
                value_inter = ref_y[count];
            data_y.append(value_inter);
    return data_y

tini = -0.25
tfin = 1.25
pas = tfin/500
tt = np.arange(tini,tfin,pas)

ff = 8.     
puls = 2. * np.pi * ff
amp = 3.
yy = [amp * np.sin(puls * tt[i]) for i in range(len(tt))]

f1 = ff*6
Ta = 5.
Nbpt1 = f1 * Ta
pas1 = Ta / Nbpt1
t1 = np.arange(0,Ta,pas1)
puls1 = 2 * np.pi * f1
sig1 = [amp * np.sin(puls * t1[i]) for i in range(len(t1))]

f2 = ff*1.2
# Ta = 1.
Nbpt2 = f2 * Ta
pas2 = Ta / Nbpt2
t2 = np.arange(0,Ta,pas2)
puls2 = 2 * np.pi * f2
sig2 = [amp * np.sin(puls * t2[i]) for i in range(len(t2))]

puls_fantome = 2 * np.pi * (f2-ff)
sig_fantome = [-amp * np.sin(puls_fantome * tt[i]) for i in range(len(tt))]

fig, ax = plt.subplots(2,1,figsize=(10,4))
ax[0].set_title(r'$f_e = 6\ f_s$')
ax[0].plot(tt,yy,'k',linewidth=2.)
ax[0].plot(t1,sig1,'.r',markersize=8)

ax[1].plot(tt,yy,'k--',linewidth=2.,alpha=0.2)
ax[1].plot(t1,sig1,'.r',markersize=8)

ax[1].set_xlabel('Temps [s]')
ax[0].set_ylabel('Tension [V]')
ax[1].set_ylabel('Tension [V]')
ax[0].grid()
ax[1].grid()
# plt.savefig("fe12.png")

fig, ax = plt.subplots(2,1,figsize=(10,4))
ax[0].set_title(r'$f_e = 1.2\ f_s$')
ax[0].plot(tt,yy,'k',linewidth=2.)
ax[0].plot(t2,sig2,'.r',markersize=8)

# ax[1].plot(tt,yy,'k',linewidth=2.,alpha=0)
ax[1].plot(tt,sig_fantome,'k--',linewidth=2.,alpha=0.2)
ax[1].plot(t2,sig2,'.r',markersize=8)

ax[1].set_xlabel('Temps [s]')
ax[0].set_ylabel('Tension [V]')
ax[1].set_ylabel('Tension [V]')
ax[0].grid()
ax[1].grid()
# plt.savefig("wrong_fe.png")

S1 = np.fft.fft(sig1)
N = len(S1)
n = np.arange(N)
T = N/Nbpt1
freq = n/T 

plt.figure(figsize = (10, 4))
# plt.subplot(121)

plt.stem(freq/Ta, np.abs(S1), 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel(r'$Fréquence (Hz)$')
plt.ylabel(r'$Amplitude |S(\omega)|$')
plt.xlim(0, f1/2)
plt.grid()
plt.title(r'$f_e = 6\ f_s$')
plt.savefig("f1_spectre.png")

S2 = np.fft.fft(sig2)
N = len(S2)
n = np.arange(N)
T = N/Nbpt2
freq = n/T 


plt.figure(figsize = (10, 4))
# plt.subplot(121)

plt.stem((freq/Ta)[:len(freq)//2], np.abs(S2[:len(freq)//2]), 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel(r'$Fréquence (Hz)$')
plt.ylabel(r'$Amplitude |S(\omega)|$')
plt.xlim(0, f1/2)
plt.grid()
plt.title(r'$f_e = 1.2\ f_s$')
plt.savefig("f2_spectre.png")
# plt.show()

#%% Bode

def filtre_RC(freq,R,C):
    return 1/(1+1j*R*C*2*np.pi*freq)

R = 100
C = 0.3*10**-6
freq = np.arange(1,2*10**5,100)

fct_transfert = [filtre_RC(freq[i],R,C) for i in range(len(freq))]

gain = 20*np.log10(np.absolute(fct_transfert))
phase = np.angle(fct_transfert)
freq_log = np.log10(freq)

plt.figure(figsize = (8, 6))

plt.subplot(211)
plt.plot(freq_log,gain)
# plt.xlabel(r'$Fréquence (log(Hz))$')
plt.ylabel(r'$20log(|H(\omega)|)$')
# plt.xlim(0, f1/2)
plt.grid()
plt.title('Diagramme de Bode')

plt.subplot(212)
plt.plot(freq_log,phase)
plt.xlabel(r'$Fréquence (Hz)$')
plt.ylabel(r'$Arg(|H(\omega)|)$')
# plt.xlim(0, f1/2)
plt.grid()
# plt.title(r'$f_e = 1.2\ f_s$')
# plt.savefig("f2_spectre.png")

#%% Bode lecture

def read_csv(name):    
    with open(name,'r') as file:
        tab = file.readlines()
    a = tab[0].split(sep=';')
    data = [[] for i in range(len(a))]
    for i in range(1,len(tab)):
        a = tab[i].split(sep=';')
        data[0].append(float(a[0].replace("\n","")))
        for j in range(1,len(a)):
            data[j].append(float(a[j].replace("\n","")))
    return data

data=read_csv("test.csv")

freq = data[0]
gain = data[1]
phase = data[2]


gain0_fit = np.polyfit(freq[:10],gain[:10],1)
gain0_polyval = np.polyval(gain0_fit,freq)

gain_inf_fit = np.polyfit(freq[-6:],gain[-6:],1)
gain_inf_polyval = np.polyval(gain_inf_fit,freq)

x_intersec = (gain_inf_fit[1]-gain0_fit[1])/(gain0_fit[0]-gain_inf_fit[0])
pt_intersec = [x_intersec,gain_inf_fit[0]*x_intersec+gain_inf_fit[1]]

plt.figure(figsize = (8, 6))

plt.subplot(211)
# plt.plot(np.log10(freq),gain)
plt.plot(freq,gain,'kd')
plt.plot(freq,gain_inf_polyval,'r--')
plt.plot(freq,gain0_polyval,'r--')
plt.vlines(x_intersec,-50,10,linestyles='--',color='k')

text_fc = r'$f_c = $' + "%.f" % 10**x_intersec + ' Hz'
plt.text(x_intersec+0.1,-35,text_fc)

text_pente = "%.2f" % gain_inf_fit[0] + 'dB/dec'
y_pente = -20
x_pente = (y_pente - gain_inf_fit[1])/gain_inf_fit[0]
plt.text(x_pente+0.4,y_pente-4,text_pente)
plt.hlines(y_pente,x_pente,x_pente+1,color='k',linestyles='--')

plt.ylabel(r'$20log(|H(\omega)|)$')
plt.grid()
plt.ylim(-45,5)
plt.title('Diagramme de Bode')

plt.subplot(212)
# plt.plot(np.log10(freq),phase)
plt.plot(freq,phase,'kd')
plt.vlines(x_intersec,-50,10,linestyles='--',color='k')
plt.ylim(-1.65,0.15)

plt.xlabel(r'$Fréquence (log(Hz))$')
plt.ylabel(r'$Arg(|H(\omega)|)$')
plt.grid()

plt.savefig("bode_exp.png")



#!/usr/bin/env python
# coding: utf-8

# In[11]:


from math import sqrt

def interfrange(lamb,Dist,S2S1):
    return lamb*Dist/S2S1

def incert_interfr(inter,lamb,Dist,S2S1,uL,uD,ua):
    return inter*sqrt((uL/lamb)**2 + (uD/Dist)**2 + (ua/S2S1)**2)

L = 592          # Lambda longueur d'onde (nm)
delta_L = 40     # incertitude de la longueur d'onde (nm)

D = 110          # Distance bifentes-écran (cm)
delta_D = 5      # incertitude de la distance bifentes-écran (cm)

a = 0.2          # Largeur entre les 2 fentes (mm)
delta_a = 0.07   # incertitude de la largeur entre 2 fentes (mm)

# Conversion des unités
L = L*1.0e-9
D = D*1.0e-2
a = a*1.0e-3
delta_L = delta_L*1.0e-9
delta_D = delta_D*1.0e-2
delta_a = delta_a*1.0e-3

# Calcul d'interfrange (mm)
i = interfrange(L,D,a) * 1.0e3   
delta_i = incert_interfr(i,L,D,a,delta_L,delta_D,delta_a)

print("L'interfrange est {} +- {} mm".format(round(i,2),round(delta_i,2)))


# In[12]:


from math import sqrt

def longOnde(interfr,Dist,S2S1) :
    return interfr*S2S1/Dist

def incert_longOnde(lamb,inter,Dist,S2S1,ui,uD,ua):
    return lamb*sqrt((ui/inter)**2 + (uD/Dist)**2 + (ua/S2S1)**2)

i = 8./3.        # interfranges (mm)
delta_i = 1./3.  # incertitude de l'interfranges (mm)

D = 110          # Distance bifentes-écran (cm)
delta_D = 5      # incertitude de la distance bifentes-écran (cm)

a = 0.2          # Largeur entre les 2 fentes (mm)
delta_a = 0.07   # incertitude de la largeur entre 2 fentes (mm)

# Conversion des unités
i = i*1.0e-3
D = D*1.0e-2
a = a*1.0e-3
delta_i = delta_i*1.0e-3
delta_D = delta_D*1.0e-2
delta_a = delta_a*1.0e-3

# Calcul de la longueur d'onde (nm)
L = longOnde(i,D,a) * 1.0e9   
delta_L = incert_longOnde(L,i,D,a,delta_i,delta_D,delta_a)

print("La longueur d'onde expérimentale est {} +- {} nm".format(round(L,2),round(delta_L,2)))

# La valeur théorique de la longueur d'onde (nm)
L_theo = 592. 
zscore = abs(L_theo - L)/delta_L
print("Le z-score est {}".format(round(zscore,2)))


# In[ ]:





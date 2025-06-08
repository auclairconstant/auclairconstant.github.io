#-----------------------------------------------------------------------
# Illustration de la seconde loi de Kepler
#
# Illustration de la conservation de la vitesse aréolaire
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Excentricité

e = 0.8

# Nombre de corps sur l'orbite

Nc = 4

# Taille du secteur

Ns = 100

# Vitesse

speed = 5

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.patches as ptc
from scipy.integrate import odeint
import itertools as itt

#-----------------------------------------------------------------------

# Quelques constantes

au = 149597870700.0 # km

G = 6.6742e-11 # SI

MS = 1.989e30      # kg, Soleil

def Foo(e) :
    return (1+e)/(1-e**2)**0.5

C0 = [ (1+e)*au, 0, 0, 0, 6.283*au/(365.25*86400)/Foo(e), 0 ]

# Calcul des dérivées

def Der(Y, t) :
    x, y, z, vx, vy, vz = Y

    ax = -G * MS / (x**2+y**2+z**2)**1.5 * x
    ay = -G * MS / (x**2+y**2+z**2)**1.5 * y
    az = -G * MS / (x**2+y**2+z**2)**1.5 * z

    return [vx, vy, vz, ax, ay, az]

# Simulation

T = np.linspace(0.0, 86400*365*2, 1260*2)

res = odeint(Der, C0, T)

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

# Animation des résultats

plt.plot([0], [0], "yo", markersize = 20)
plt.plot(res[:1260,0], res[:1260,1], 'k--')

def GetCoords(i, mask=False) :
    T = np.array([[0]+list(res[i%1260:i%1260+Ns,0]), [0]+list(res[i%1260:i%1260+Ns,1])]).T
    if mask :
        T *= 0
    return T

# Construit la liste des polygones et corps célestes

polys = []
for i in range(Nc) :
    polys.append((i*1260//Nc, ptc.Polygon(GetCoords(0, True), True, color='ygbrmc'[i%6], alpha=0.3), plt.plot([0],[0],'ygbrmc'[i%6]+'o', markersize=8)[0]))
    plt.gca().add_patch(polys[-1][1])

plt.axis("equal")
plt.title("Deuxième loi de Kepler : vitesse aréolaire constante")

# Animation

def SizeChanged(ax, old=[]) :
    current = [ ax.bbox.width, ax.bbox.height ]
    if old != current :
        old[:] = current
        return True
    return False

def Update(i) :
    for k, poly, corps in polys :
        crds = GetCoords(k+i)
        poly.set_xy(crds)
        corps.set_data([crds[-1,0]], [crds[-1,1]])
    if SizeChanged(plt.gca()) :
        plt.gcf().canvas.draw()
    return [ poly for k, poly, _ in polys ] + [ corps for k, _, corps in polys ]

def Init() :
    for k, poly, corps in polys :
        crds = GetCoords(k+i, True)
        poly.set_xy(crds)
        corps.set_data(np.ma.array([crds[-1,0]], mask=True),
                       np.ma.array([crds[-1,1]], mask=True))
    return [ poly for k, poly, _ in polys ] + [ corps for k, _, corps in polys ]

anim = ani.FuncAnimation(plt.gcf(), Update, frames=itt.count(0, int(speed)),
                         interval=50, blit=True, init_func=Init)


# Détection utilisation hors Pyzo

if __name__=="__main__":
    plt.show()
    
    
    
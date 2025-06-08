
from pylab import *
from scipy.integrate import odeint # Pour la resolution d'equations differentielles
from scipy.optimize import brentq # Pour trouver les zeros d'une fonction
import matplotlib.pyplot as plt

titre = """Puits quantique"""

description = """Ce programme permet de représenter les niveaux d'énergie 
dans un puits quantique, ainsi que les fonctions d'onde correspondantes."""


#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

N = 1001                  # Discretisation du puits

Vo = 30               # Hauteur du puits quantique
b = 2                     # Point en dehors du puits pour verifier si la fonction diverge
x = linspace(-b, b, N)    # abscisses
L = 1                     # largeur du puits
dx = x[1] - x[0]

#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def V(x, L=L, Vo=Vo):
    """
    Potentiel du puits quantique. L est la largeur du puits, et Vo la hauteur
    """
    if abs(x) < L:
        return 0
    else:
        return Vo

def SE(psi, x, E, L, Vo):
    """
    Fonction qui renvoie le vecteur (psi',psi'') grace a l'equation de Schrodinger
    """
    state0 = psi[1]
    state1 = 2.0*(V(x, L, Vo) - E)*psi[0]
    return array([state0, state1])

def wave_function(energy, L, Vo, last_point=False):
    """
    Calcule la fonction d'onde solution de l'equation de Schrodinger.
    """
    psi0 = array([0,1]) # Condition initiale
    psi = odeint(SE, psi0, x, args=(energy, L, Vo))
    if last_point:
        return psi[-1, 0]
    return psi
 

def find_all_zeroes(energies, L, Vo):
    """Chercher les energies propres

L'idee est de scanner toutes les energies entre 0 et 100Vo, et de chercher 
celles dont la fonction d'onde vaut 0 loin à l'interieur du puits (en x=b).
    """
    all_zeroes = []
    y = [wave_function(E, L, Vo, last_point=True) for E in energies]
    s = np.sign(y)
    for i in range(len(y)-1):
        if s[i]+s[i+1] == 0:
            zero = brentq(wave_function, energies[i], energies[i+1], args=(L, Vo, True))
            all_zeroes.append(zero)
    return all_zeroes


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(ax1, ax2, L=L, Vo=Vo):
    en = linspace(0.1, Vo, 100)   # Energies que l'on va investiger pour trouver les etats propres
    E_zeroes = find_all_zeroes(en, L, Vo) # On ne selectionne que les energies telles que la fonction d'onde vaut 0 en x=b
    for E in E_zeroes:
        ax2.plot(linspace(-L, L, 50), E*ones(50), label="E = %.2f"%E)
    ax2.legend()

    ## Fonctions d'onde
    for E in E_zeroes:
        psi = wave_function(E, L, Vo)
        norm2 = np.sum(psi**2*dx)
        psi = psi/np.sqrt(norm2)
        ax1.plot(x, psi[:,0], label="E = %.2f"%E)


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================


fig = plt.figure()
fig.suptitle(titre)
#fig.text(0.5, .93, description, multialignment='left', verticalalignment='top', horizontalalignment='center')

ax1, ax2 = fig.subplots(2, sharex=True) # La figure sera composee de deux sous-figures

## ax2 : Energies
ax2.set_title(r'Énergies propres')
ax2.set_ylim(-0.1*Vo,1.2*Vo)
ax2.set_ylabel('$E$')
ax2.set_xlim(-2,2)
ax2.set_xlabel('$x/L$')

## Dessin du puits
ax2.plot(x, np.vectorize(V)(x, L, Vo), linewidth=2, color='k')

## ax1 : Fonctions d'onde
ax1.set_title("Fonctions d'onde propres")
ax1.set_ylim(-.5,1)
ax1.set_ylabel('$\Psi(x)$')

## Pointilles
for ax in [ax1, ax2]:
    for s in [-1, 1]:
        ax.axvline(s*L, color='k', linestyle='--')

plot_data(ax1, ax2)




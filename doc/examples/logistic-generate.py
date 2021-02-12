import openturns as ot
from openturns.viewer import View

# Here the model is created using the simplified Python interface for FieldToPointFunction

tmin = 1790.0  # Date minimale
tmax = 2001.0  # Date maximale
gridsize = 100  # Nombre de pas de temps
modeleName = "Modèle Logistique"  # Nom du modèle
parameterIndexName = "Temps (années)"  # Nom du paramètre d'indexation
fieldName = "Population (millions)"  # Nom du champ
alphaInf = 0.05  # Valeur du niveau alpha pour le quantile inférieur
# Définit l'intervalle de temps pour la simulation
monhorizon = ot.Interval(tmin, tmax)
# Définit la grille temporelle régulière
mesh = ot.IntervalMesher([gridsize - 1]).build(monhorizon)
graph1 = mesh.draw()
graph1.setTitle(modeleName)
graph1.setXTitle(parameterIndexName)
View(graph1)

from numpy import exp
from numpy import array


def logisticSolution(X):
    # Récupère les noeuds du maillage
    v = mesh.getVertices()
    # Convertit en tableau
    t = array(v)
    # Convertit le tableau 2D en tableau 1D
    t = t.flatten()
    # Récupère la date initiale
    t0 = t[0]
    # Calcule la trajectoire
    y0, a, b = X
    y = a * y0 / (b * y0 + (a - b * y0) * exp(-a * (t - t0)))
    y = y / 1.0e6
    # Créée la liste des altitudes à partir du array numpy
    matrajectoire = [[zeta] for zeta in y]
    return matrajectoire


inputDim = 3  # Nombre de variables en entrée (i.e. taille du vecteur aléatoire)
outputDim = 1  # Nombre de champs en sortie (ici, une seule trajectoire)
maFonctionChamp = ot.PythonPointToFieldFunction(
    inputDim, mesh, outputDim, logisticSolution
)

# Teste une évaluation
y0 = 3.9e6  # Population initiale
a = 0.03134
b = 1.5887e-10
X = [y0, a, b]
unetrajectoire = maFonctionChamp(X)
unetrajectoire.setDescription([fieldName])
# print("Une trajectoire:")
# print(unetrajectoire)

# Creation of the input distribution
distY0 = ot.Normal(y0, 0.1 * y0)
distA = ot.Normal(a, 0.3 * a)
distB = ot.Normal(b, 0.3 * b)
distX = ot.ComposedDistribution([distY0, distA, distB])

# Sample the model
samplesize = 1000
inputSample = distX.getSample(samplesize)
outputSample = maFonctionChamp(inputSample)
# outputSample is a ProcessSample

# Draw some trajectories
graph = outputSample.drawMarginal(0)
graph.setTitle(modeleName)
graph.setXTitle(parameterIndexName)
graph.setYTitle(fieldName)
myTrajectories = [
    ot.Drawable.ConvertFromHSV(i * (360.0 / samplesize), 1.0, 1.0)
    for i in range(len(graph.getDrawables()))
]
graph.setColors(myTrajectories)
ot.Show(graph)

# Create a sample with nodes and values
data = ot.Sample(gridsize, samplesize + 1)
data[:, 0] = mesh.getVertices()
for i in range(samplesize):
    trajectory = outputSample[i].getValues()
    data[:, i + 1] = trajectory

data.exportToCSVFile("logistic-trajectories.csv")

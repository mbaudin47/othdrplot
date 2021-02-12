import openturns as ot
import numpy as np

tmin = 0.0  # Date minimale
tmax = 12.0  # Date maximale
gridsize = 100  # Nombre de pas de temps
mesh = ot.IntervalMesher([gridsize - 1]).build(ot.Interval(tmin, tmax))


def AltiFunc(X):
    g = 9.81
    z0 = X[0]
    v0 = X[1]
    m = X[2]
    c = X[3]
    zmin = X[4]
    tau = m / c
    vinf = -m * g / c
    t = np.linspace(tmin, tmax, gridsize)
    z = z0 + vinf * t + tau * (v0 - vinf) * (1 - np.exp(-t / tau))
    z = np.maximum(z, zmin)
    altitude = [[zeta] for zeta in z]
    return altitude


inputDim = 5
outputDim = 1
alti = ot.PythonPointToFieldFunction(inputDim, mesh, outputDim, AltiFunc)


# Creation of the input distribution
distZ0 = ot.Uniform(100.0, 150.0)
distV0 = ot.Normal(55.0, 10.0)
distM = ot.Normal(80.0, 8.0)
distC = ot.Uniform(0.0, 30.0)
distZmin = ot.Dirac([0.0])
distX = ot.ComposedDistribution([distZ0, distV0, distM, distC, distZmin])

# Sample the model
samplesize = 1000
inputSample = distX.getSample(samplesize)
outputSample = alti(inputSample)

# Draw some curves
graph = outputSample.drawMarginal(0)
graph.setTitle("chute visqueuse")
graph.setXTitle(r"$t$")
graph.setYTitle(r"$z$")
graph.setColors(
    [
        ot.Drawable.ConvertFromHSV(i * (360.0 / samplesize), 1.0, 1.0)
        for i in range(len(graph.getDrawables()))
    ]
)
ot.Show(graph)

# Create a sample with nodes and values
data = ot.Sample(gridsize, samplesize + 1)
data[:, 0] = mesh.getVertices()
for i in range(samplesize):
    trajectory = outputSample[i].getValues()
    data[:, i + 1] = trajectory

data.exportToCSVFile("chute-trajectories.csv")

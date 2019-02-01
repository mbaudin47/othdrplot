# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
'''
Un composant pour créer des HighDensityRegionAlgorithm.

TODO : étendre l'algorithme aux échantillons de dimension >2
i.e. utiliser un Pairs() et y placer les contour.

TODO : identifier le point de plus forte densité

Références : TODO
'''

import openturns as ot
import numpy as np
import pylab as pl

class HighDensityRegionAlgorithm:
    def __init__(self,sample,distribution):
        # Parameters
        self.numberOfPointsInXAxis = 30 # The number of points in the X-grid to plot the contour
        self.numberOfPointsInYAxis = 30 # The number of points in the Y-grid to plot the contour
        self.contoursAlpha=[0.9,0.5,0.1] # The list of probabilities to create the contour
        self.outlierAlpha = 0.9 # The probability for outlier detection
        self.outlierMarker = "r*" # The marker for outliers
        self.dataMarker = "b." # The marker for data
        #
        self.sample = sample
        self.distribution = distribution
        # Check input
        sampleDim = sample.getDimension()
        if (sampleDim!=2):
            raise ValueError('The dimension of the sample must be equal to 2, but current dimension is %d.' % (sampleDim))
        # Computed by the algorithm
        self.pvalueArray = None
        self.levelSetList = []
        self.outlierPvalue = None
        self.outlierLevelSet = None
    
    def run(self):
        numberOfContourLines=len(self.contoursAlpha)
        # Compute the regular level sets
        self.pvalueArray=np.zeros(numberOfContourLines)
        for i in range(numberOfContourLines):
            levelSet, pvalue = self.distribution.computeMinimumVolumeLevelSetWithThreshold(self.contoursAlpha[i])
            self.pvalueArray[i]=pvalue
            self.levelSetList.append(levelSet)
        # Compute the outlier level set
        levelSet, pvalue = self.distribution.computeMinimumVolumeLevelSetWithThreshold(self.outlierAlpha)
        self.outlierPvalue = pvalue
        self.outlierLevelSet = levelSet
        return None
    
    def computeOutlierIndices(self,outlierFlag=True):
        '''
        If outlierFlag is true, returns the array of outlier indices in the sample. 
        These outliers correspond to the self.outlierAlpha probability.
        Otherwise, returns the array of inlier indices in the sample. 
        '''
        ols = self.outlierLevelSet
        flag = ols.contains(self.sample)
        outsideLevelSetFlag = 0
        if (outlierFlag):
            sampleIndices = np.where(np.array(flag)==outsideLevelSetFlag)[0]
        else:
            sampleIndices = np.where(np.array(flag)!=outsideLevelSetFlag)[0]
        return sampleIndices

    def setnumberOfPointsInXAxis(self,numberOfPointsInXAxis):
        self.numberOfPointsInXAxis = numberOfPointsInXAxis

    def setnumberOfPointsInYAxis(self,numberOfPointsInYAxis):
        self.numberOfPointsInYAxis = numberOfPointsInYAxis

    def setContoursAlpha(self,contoursAlpha):
        self.contoursAlpha = contoursAlpha

    def setOutlierAlpha(self,outlierAlpha):
        self.outlierAlpha = outlierAlpha

    def computeContour2D(self,X1pars,X2pars):
        X1min,X1max,nX1 = X1pars
        X2min,X2max,nX2 = X2pars
        #
        x1 = np.linspace(X1min, X1max, nX1)
        x2 = np.linspace(X2min, X2max, nX2)
        X1, X2 = np.meshgrid(x1, x2)
        #
        X1flat = X1.flatten()
        X2flat = X2.flatten()
        #
        X1flat = ot.Sample(X1flat,1)
        X2flat = ot.Sample(X2flat,1)
        #
        inputContour = ot.Sample(nX1*nX2, 2)
        inputContour[:,0] = X1flat
        inputContour[:,1] = X2flat
        Z = self.distribution.computePDF(inputContour)
        #
        Z = np.array(Z)
        Z = Z.reshape((nX1,nX2))
        return [X1,X2,Z]
        
    def plotContour(self,plotData=False,plotOutliers=True):
        '''
        Plot the contour in the density plot.
        Set plotData to true to plot the sample data.
        Set plotOutliers to true to plot the sample data.
        '''
        # 2. Evalue la densité sur une grille régulière
        X1min=self.sample[:,0].getMin()[0]
        X1max=self.sample[:,0].getMax()[0]
        X2min=self.sample[:,1].getMin()[0]
        X2max=self.sample[:,1].getMax()[0]
        X1pars = [X1min,X1max,self.numberOfPointsInXAxis]
        X2pars = [X2min,X2max,self.numberOfPointsInYAxis]
        [X1,X2,Z] = self.computeContour2D(X1pars,X2pars)
        # TODO MBN Février 2017 : DistributionImplementation.cxx, lignes 2407 dans la méthode computeMinimumVolumeLevelSetWithThreshold
        # 3. Calcule la ligne de niveau pvalue associée a un niveau donné de probabilité
        # 4. Cree le contour
        CS = pl.contour(X1, X2, Z, self.pvalueArray)
        # 5. Calcule les labels : affiche la probabilité plutôt que la densité
        fmt = {}
        numberOfContourLines = len(self.contoursAlpha)
        for i in range(numberOfContourLines):
            l = CS.levels[i]
            fmt[l] = "%.0f %%" % (self.contoursAlpha[i]*100)
        # 6. Create contour plot (enfin !)
        pl.clabel(CS, CS.levels, inline=True, fontsize=10, fmt=fmt)
        # 7. Dessine le nuage
        # Dessine les outliers
        if (plotOutliers):
            outlierIndices = self.computeOutlierIndices()
            dataArray = np.array(self.sample)
            outlierSample = dataArray[outlierIndices,:]
            pl.plot(outlierSample[:,0],outlierSample[:,1],self.outlierMarker,label="Outliers at alpha=%.4f" % (self.outlierAlpha))
            
        if (plotData):
            if (plotOutliers):
                # Plot only non-outlier sample data
                inlierIndices = self.computeOutlierIndices(False)
                dataArray = np.array(self.sample)
                nonoutlierSample = dataArray[inlierIndices,:]
                pl.plot(nonoutlierSample[:,0],nonoutlierSample[:,1],self.dataMarker,label="Inliers at alpha=%.4f" % (self.outlierAlpha))
            else:
                # Plot all points (including outliers)
                pl.plot(self.sample[:,0],self.sample[:,1],self.dataMarker)
        # Configure le graphique
        pl.title('High Density Region plot')
        mydescr = self.sample.getDescription()
        pl.xlabel(mydescr[0])
        pl.ylabel(mydescr[1])
        pl.legend()
        return None

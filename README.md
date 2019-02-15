# othdrplot
OpenTURNS experiments with HDRPlots

## Algorithmes

Deux Algorithmes : 
* HighDensityRegionAlgorithm : Un algorithme pour calculer la densité d'un échantillon de points multidimensionnel
* ProcessHighDensityRegionAlgorithm : Un algorithme pour calculer la densité d'un échantillon de trajectoires 

## HighDensityRegionAlgorithm

Algorithme pour calculer la densité d'un échantillon de points multidimensionnel
* Calcul du min. levelset
* Graphique des levelset à 50% et 95%, outliers 
* Calcul des points inliers et outliers
* Ingrédient : Une méthode pour estimer la densité d'un échantillon de points : kernel smoothing, mélange de gaussienne (otmixmod) 

## ProcessHighDensityRegionAlgorithm

Algorithme pour calculer la densité d'un échantillon de trajectoires
* Graphique des trajectoires dans la bande à 50% et 95%, outliers
* Ingrédients : Une méthode de réduction de dimension : ACP

## Roadmap

### TODO-List  général

* Créer une classe pour l’ACP. Draft de Géraud. Sortir l’ACP de la classe Process pour pouvoir remplacer par KL

### TODO-List  HighDensityRegionAlgorithm 

* pouvoir créer le graphique avec une dimension supérieure à 2 : utiliser un Pairs avec des lignes de contours (actuellement : uniquement dimension 2)
* Pouvoir spécifier la méthode d’estimation de densité que l’on souhaite (actuellement : uniquement KernelSmoothing)
* créer un exemple pour utiliser un mélange de gaussiennes

### TODO-List  ProcessHighDensityRegionAlgorithm 

* pouvoir avoir un nombre de composantes principales supérieur à 2 (actuellement : uniquement dimension 2)
* pouvoir choisir une autre méthode de réduction de dimension, comme par exemple avec la réduction de dimension par Karhunen-Loève (actuellement : uniquement par ACP)
* méthode de Pamphile

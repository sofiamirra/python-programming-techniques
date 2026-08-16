from model.model import Model

mymodel = Model()

mymodel.getTeamsOfYear(2012)
mymodel.creaGrafo()
nodi, archi = mymodel.getGraphDetails()
print(f"Grafo creato! Il grtafo ha {nodi} nodi e {archi} archi")
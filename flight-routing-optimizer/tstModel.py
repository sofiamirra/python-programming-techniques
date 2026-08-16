from model.model import Model

myModel = Model()
myModel.buildGraph(5)
nNodes, nEdges = myModel.getGraphDetails()
print(f"Numero nodi: {nNodes}, Numero archi: {nEdges}")
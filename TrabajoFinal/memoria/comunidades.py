from graph_tool.all import *
import pandas as pd

g = load_graph("grafo.graphml")
g.set_directed(True)
# calculamos un layout para el grafo
pos_arf = arf_layout(g=g)
# pos_fr = fruchterman_reingold_layout(g=g)

# # realizamos la detección de comunidades usando este algoritmo:
# # https://en.wikipedia.org/wiki/Stochastic_block_model
# state1 = minimize_blockmodel_dl(g=g)
# # lo pintamos
# state1.draw(pos=pos_arf, output="blockmodel.svg")

# realizamos la detección de comunidades usando la versión nested
state2 = minimize_nested_blockmodel_dl(g=g)
# lo pintamos
state2.draw(pos=pos_arf, output="markovchain.svg")

# tratamos de ver a qué comunidad pertenece cada nodo
# coms1 = state1.get_blocks().get_array()
coms2 = state2.get_levels()[0].get_blocks().get_array()
# print("Comunidades encontradas por el Stochastic block model: ", state1.get_B())
print("Comunidades encontradas por el Nested stochastic block model: ", state2.get_levels()[0].get_B())

labels = g.vp.label.get_2d_array(pos=[0])
comunidades = pd.DataFrame({'label': labels, 'comunidades2':coms2})

# print("Partición de nodos para el Stochastic block model")
# print((comunidades.groupby(by='comunidades1').count()['label']/g.num_vertices())*100)

print("Partición de nodos para el Nested stochastic block model")
print((comunidades.groupby(by='comunidades2').count()['label']/g.num_vertices())*100)

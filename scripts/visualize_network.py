import sys
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import BoundaryNorm
import numpy as np
import networkx as nx

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

def save_graph(matrix, experiment_name):
    G = nx.DiGraph(matrix)

    widths = {(u, v): f'{d["weight"]*10:.2f}' for u, v, d in G.edges(data=True)}
    edge_labels = {(u, v): f'{d["weight"]:.2f}' for u, v, d in G.edges(data=True)}
    nodelist = G.nodes()

    weights = nx.get_edge_attributes(G, 'weight')
    color_map = []
    for edge in G.edges():
        if weights[edge] < 0:
            color_map.append('saddlebrown')
        else: 
            color_map.append('mediumblue')  

    plt.figure(figsize=(5,4))
    pos = nx.circular_layout(G)
    '''nx.draw_networkx_nodes(G,pos,
                        nodelist=nodelist,
                        node_size=3000,
                        node_color='lightgrey',
                        edgecolors='black')
    nx.draw_networkx_edges(G,pos,
                        edgelist = widths.keys(),
                        width=[4 for x in widths.values()],
                        edge_color=color_map,
                        alpha=0.8)
    nx.draw_networkx_labels(G, pos=pos,
                            labels=dict(zip(nodelist,nodelist)),
                            font_color='black',
                            font_size=24)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels)'''
    nx.draw(G, pos=pos, with_labels=True, node_size=1000, edge_color=color_map, node_color='lightgrey')

    plt.savefig(f'../experiments/{experiment_name}/interaction_graph.png')


def main():
    file_name = sys.argv[1]
    experiment_name = sys.argv[2]
    matrix = np.loadtxt(file_name, delimiter=',')

    save_graph(matrix, experiment_name)

    #https://stackoverflow.com/questions/23994020/colorplot-that-distinguishes-between-positive-and-negative-values
    cmap = plt.get_cmap('PuOr')
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    bounds = [-1, -0.75, -0.5, -0.25, -.0001, .0001, 0.25, 0.5, 0.75, 1]
    norm = BoundaryNorm(bounds, cmap.N)

    plt.imshow(matrix, cmap=cmap, interpolation='none', norm=norm)
    plt.colorbar()
    plt.savefig(f'../experiments/{experiment_name}/interaction_matrix.png')


if __name__ == '__main__':
    main()
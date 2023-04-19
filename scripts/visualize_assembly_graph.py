import networkx as nx
import matplotlib.pyplot as plt
import random

def visualize(edges, file_name, weights={}):
    graph = nx.DiGraph()
    graph.add_edges_from(edges)

    print('nodes: ', graph.number_of_nodes())

    positions = {}
    color_map = []
    i = 0
    for node in graph:
        if graph.out_degree(node) == 0:
            color_map.append('red')
        else:
            color_map.append('pink')
        #if node == '100000010':
        #    positions[node] = (weights[node]+0.01, graph.out_degree(node)+0.50)
        #elif node == '100100010':
        #    positions[node] = (weights[node], graph.out_degree(node))
        #else:
        #    positions[node] = (weights[node]+random.random()/10, graph.out_degree(node)+random.random()/10)
        positions[node] = (weights[node]+random.random()/10, graph.out_degree(node)+random.random()/10)
        i += 1

    plt.figure(figsize=(15, 15))
    if len(weights) > 0:
        nx.set_node_attributes(graph, weights, name='weight')
        nx.set_node_attributes(graph, positions, name='pos')
        labels = {n: n+'\n'+str(graph.nodes[n]['weight']) for n in graph.nodes}
        nx.draw(graph, pos=nx.get_node_attributes(graph, 'pos'), with_labels=True, edge_color='gray', node_size=5500, node_color=color_map, labels=labels)
    else:
        nx.draw(graph, with_labels=True, edge_color='gray', node_size=4200, node_color=color_map)
    plt.savefig(f'{file_name}.png')


def main(with_pagerank=False):
    graphs = {}
    communities = open('../community_fitness2.txt').read().split('\n')
    curr_graph = ''
    for line in communities[22:]:
        if len(line) > 0:
            if line[0] != '*':
                graphs[curr_graph].append(line.split(' '))
            else:
                graph_name = line.split('***')[1]
                graphs[graph_name] = []
                curr_graph = graph_name

    weights = {}
    if with_pagerank:
        ranks = open('../pagerank2.txt').read().split('\n')
        curr_graph = ''
        for line in ranks[22:]:
            if len(line) > 0:
                if line[0] != '*':
                    node, weight = line.split(' ')
                    weight = round(float(weight), 3)
                    weights[curr_graph][node] = weight
                else:
                    graph_name = line.split('***')[1]
                    weights[graph_name] = {}
                    curr_graph = graph_name

    '''assm = 0
    for graph in graphs:
        if graph == 'Community Assembly':
            assm = weights[graph]['001110001']
        print(f"{graph}: {weights[graph]['001110001']**3/assm**3}")'''

    for graph in graphs:
        print(graph)
        print('edges: ', len(graphs[graph]))
        if with_pagerank:
            visualize(graphs[graph], graph, weights[graph])
        else:
            visualize(graphs[graph], graph)
        print()


if __name__ == '__main__':
    main(True)
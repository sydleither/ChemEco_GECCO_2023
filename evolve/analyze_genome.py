import ast
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from lfr_graph import create_matrix, create_matrix_unformatted

def visualize_network(input_name, output_name):
    matrix = np.loadtxt(input_name, delimiter=',')

    #https://stackoverflow.com/questions/23994020/colorplot-that-distinguishes-between-positive-and-negative-values
    cmap = plt.get_cmap('PuOr')
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    bounds = [-1, -0.75, -0.5, -0.25, -.0001, .0001, 0.25, 0.5, 0.75, 1]
    norm = BoundaryNorm(bounds, cmap.N)

    plt.imshow(matrix, cmap=cmap, interpolation='none', norm=norm)
    plt.colorbar()
    plt.savefig(output_name)


def main(genome):
    interactions = create_matrix_unformatted(genome)
    with open("interaction_matrix.dat", "w") as f:
        wr = csv.writer(f)
        wr.writerows(interactions)
    visualize_network('interaction_matrix.dat', 'interaction_matrix.png')


if __name__ == '__main__':
    main([0.164, 0.217, 0, 0.64, 0.1, 2, 1.899, 1.073, 0.954, 0.652, 6, 7, 5, 6, 0, 0])
import matplotlib.pyplot as plt
import csv, sys
from mpl_toolkits.mplot3d import axes3d

def plot_lcurve(data_path=""):
    y_chi = []
    x_entropy = []

    lines = [line.rstrip('\n') for line in open(data_path)]

    for i in range(len(lines)):
        values = lines[i]
        data   = values.split(',')

        y_chi.append(float(data[0]))
        x_entropy.append(float(data[1]))

    fig = plt.figure()
    fig.suptitle('Curve - l', fontsize=14, fontweight='bold')

    ax = fig.add_subplot(111)

    ax.set_xlabel('Entropy')
    ax.set_ylabel('Chi2')

    ax.plot(x_entropy, y_chi, 'ro-')
    plt.show()

def plot_lcurve_iter(dim=""):
    iter = []
    y_chi = []
    x_entropy = []

    data_path="/home/hperez/Desktop/salida.csv"

    with open(data_path) as f:
        reader = csv.reader(f)
        next(reader)
        data = [r for r in reader]

    for i in range(len(data)):
        row_data = data[i]

        if(len(row_data) == 3):
            iter.append(int(row_data[0]))
            x_entropy.append(float(row_data[1]))
            y_chi.append(float(row_data[2]))

    fig = plt.figure()
    fig.suptitle('Curve - l per iteration', fontsize=14, fontweight='bold')

    if dim == '3d':
        ax = fig.add_subplot(111)
        ax = fig.gca(projection='3d')

        ax.set_xlabel('Entropy')
        ax.set_ylabel('Chi2')
        ax.set_zlabel('Iteration')

        ax.scatter(x_entropy, y_chi, iter, '.', s=5, c='#0e4d8c')
        plt.show()

    elif dim == '2d':
        ax = fig.add_subplot(111)

        ax.set_xlabel('Entropy')
        ax.set_ylabel('Chi2')

        ax.plot(x_entropy, y_chi, 'ro-')
        plt.show()
    else:
        sys.exit("Dimension must be '2d' or '3d'.")

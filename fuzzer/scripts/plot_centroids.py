#!/usr/bin/python3.5
import matplotlib.pyplot as plt
import os
import click
import numpy as np

@click.command()
@click.option('--path', '-p', help='path to directory.')
def main(path):

    for centroid in os.listdir(path):
        y = np.loadtxt(path + centroid)
        plt.plot(y)

    plt.show()

        
if __name__ == "__main__":
    main()
    exit()
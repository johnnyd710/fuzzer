#!/usr/bin/python3.5
import matplotlib.pyplot as plt
import os
import numpy as np
import sys

PATH=sys.argv[1]

def centroids():
    i=0
    for centroid in os.listdir(PATH):
        i+=1
        y = np.loadtxt(PATH + '/' + centroid)
        plt.plot(y, label=str(i))

    plt.legend()
    plt.show()



if __name__ == "__main__":
    centroids()
    exit()

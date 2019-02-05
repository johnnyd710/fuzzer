#!/usr/bin/python3.5

import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../')
import matplotlib.pyplot as plt
import os
import click
import numpy as np
from offline import Offline

@click.command()
@click.option('--dest', '-d', help='destination.')
@click.option('--source', '-s', help='source.')
def main(dest, source):
    Off = Offline()
    Off.first_load(source, 15000)
    Off.write_out(dest)    

        
if __name__ == "__main__":
    main()
    exit()
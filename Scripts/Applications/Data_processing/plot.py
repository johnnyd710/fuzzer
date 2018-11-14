import matplotlib.pyplot as plt
import csv, sys

x = []
y = []
counter = 1

with open(sys.argv[1],'r') as csvfile:
    plots = csv.reader(csvfile)
    for row in plots:
        x.append(counter)
        y.append(float(row[0]))
        counter += 1

plt.plot(x,y)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

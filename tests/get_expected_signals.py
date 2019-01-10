import matplotlib.pyplot as plt
import numpy as np
from cluster_tests import get_signals
import sys

n = len(sys.argv)

plt.style.use('ggplot') #Change/Remove This If you Want
fig, ax = plt.subplots(figsize=(15, 10))

colors = ['null','red', 'blue', 'green', 'yellow']

for i in range(1,n):

    dir_signals = sys.argv[i]
    signals = get_signals(dir_signals, 100)

    avg = np.average(signals, axis=0)
    std = np.std(signals, axis=0)
    x = range(signals.shape[1])

    ax.plot(x, avg, alpha=0.5, color=colors[i], label=str(i), linewidth = 1.0)
    ax.fill_between(x, avg - std, avg + std, color=colors[i], alpha=0.4)
    ax.fill_between(x, avg - 2*std, avg + 2* std, color=colors[i], alpha=0.2)

ax.legend(loc='best')
ax.set_ylabel("Signal units?")
ax.set_xlabel("Time")
plt.show()
exit()
import matplotlib.pyplot as plt
import numpy as np

xy=np.loadtxt('temp.txt', unpack=True)

x=np.transpose(xy[0:1])
ax=np.transpose(xy[1:2])
ay=np.transpose(xy[2:3])
az=np.transpose(xy[3:4])
plt.title('Acc Raw Data')
plt.grid('k', linestyle='-', linewidth=0.1)
plt.plot(x, ax, 'b-', label='ax')
plt.plot(x, ay, 'r-', label='ay')
plt.plot(x, az, 'g-', label='az')
plt.legend(loc='upper right')
plt.show()

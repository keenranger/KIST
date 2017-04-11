import numpy as np
import matplotlib.pyplot as plt

mic_data=np.loadtxt('micdata.txt', unpack=True)

plt.plot(mic_data)
#print(np.fft.fft(mic_data))
#plt.plot(np.fft.fft(mic_data))
plt.show()

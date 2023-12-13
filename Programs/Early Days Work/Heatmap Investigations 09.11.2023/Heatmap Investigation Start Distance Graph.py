import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

X = np.load('datax.npy')
Y = np.load('datay.npy')
Z = np.load('dataz.npy')
T = np.load('datat.npy')

plt.contour(X,Y, Z, linewidths = 0.001, colors = 'k', levels = [-5])
plt.imshow(Z, cmap = 'jet', aspect = 'auto', interpolation = 'gaussian', extent = [min(T),max(T),30 , 160], vmin = -10, vmax = -2)
plt.xlabel('Time (s)', labelpad=20)
plt.ylabel('Initial Vehicle Separation (m)', labelpad=20)
plt.colorbar().set_label("Acceleration (ms$^{-2}$)")
plt.xticks(np.arange(0,1.1,0.1))
plt.show()


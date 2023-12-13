import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

X = np.load('datax.npy')
Y = np.load('datay.npy')
Z = np.load('dataz.npy')
T = np.load('datat.npy')

plt.contour(X,Y, Z, linewidths = 0.0001, colors = 'k', levels = [-5])
plt.imshow(Z, cmap = 'jet', aspect = 'auto', interpolation = 'gaussian', extent = [min(T), max(T), 1,5], vmin = -5, vmax = 2)
plt.xlabel('Time (s)', labelpad=20)
plt.ylabel('$b$ - Comfortable Deceleration', labelpad=20)
plt.colorbar().set_label("Acceleration (ms$^{-2}$)")
plt.xticks(np.arange(0,95,10))
plt.show()
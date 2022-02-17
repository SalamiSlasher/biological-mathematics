import matplotlib.pyplot as plt
import numpy as np

'''
plt.plot(range(0, 10))
Initial axes limits are 0, 10

scale_factor = 5

xmin, xmax = plt.xlim()
ymin, ymax = plt.ylim()

plt.xlim(xmin * scale_factor, xmax * scale_factor)
plt.ylim(ymin * scale_factor, ymax * scale_factor)

'''

scale_factor = 0.0099

xmin, xmax = plt.xlim()
ymin, ymax = plt.ylim()

plt.xlim(xmin * scale_factor, xmax * scale_factor)
#plt.ylim(ymin * scale_factor, ymax * scale_factor)

x = np.linspace(0, 0.15, 4096)
D = np.genfromtxt('RAND.data')
plt.plot(x, D[0], label=r'$D_{1, 1}$', scalex=10)
plt.plot(x, D[1], label=r'$D_{1, 2}$', scalex=10)
plt.plot(x, D[2], label=r'$D_{1, 3}$', scalex=10)
plt.plot(x, D[3], label=r'$D_{2, 2}$', scalex=10)
plt.plot(x, D[4], label=r'$D_{2, 3}$', scalex=10)
plt.plot(x, D[5], label=r'$D_{3, 3}$', scalex=10)
plt.legend()
plt.show()

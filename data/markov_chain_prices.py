import numpy as np
import sys
from scipy import interp
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
import time
import sqlite3
import itertools
import pandas as pd
from scipy.interpolate import interp1d
import mpl_toolkits.mplot3d.axes3d as p3

horizon = 24
num_interp = 20

data = pd.read_csv('/Users/mathildebadoual/code/ev_controller/data/price_demand.csv')

data_price = data['Price']

data_price_grid = np.linspace(0, max(data_price), num_interp)
# Interpolation function: interp(arg1, arg2, ...)
T = range(len(data_price))
t = np.mod(np.divide(T, 2), horizon / 2);

counts = np.zeros((num_interp, num_interp, horizon))
P = np.zeros((num_interp, num_interp, horizon))

for idx in range(len(data_price)-1):
    i = int(interp(data_price[idx], data_price_grid, range(num_interp)))
    j = int(interp(data_price[idx+1], data_price_grid, range(num_interp)))
    k = int(t[idx] * 2 + 1)-1
    counts[i, j, k] += 1

for i in range(num_interp):
    for k in range(horizon):
        # Compute fraction of times irradiance level goes from ii to jj in time step kk
        # out of ALL transitions out of level ii
        if sum(counts[i, :, k]) != 0:
            P[i, :, k] = counts[i, :, k] / sum(counts[i, :, k])

imagelist = [P[:, :, k] for k in range(P.shape[2])]

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')# make figure

row_names = [str(int(price)) for price in data_price_grid]
column_names = row_names

X, Y = np.meshgrid(range(num_interp), range(num_interp))
X = X.flatten('F')
Y = Y.flatten('F')
Z = np.zeros_like(X)

dx = 0.5 * np.ones_like(Z)
dy = dx.copy()

# make axesimage object
# the vmin and vmax here are very important to get the color map correct
im = ax.bar3d(X, Y, Z, dx, dy, imagelist[0].flatten())

# function to update figure
def updatefig(j):
    ax.cla()
    ax.set_zlim(0, 1)
    # set the data in the axesimage object
    im = ax.bar3d(X, Y, Z, dx, dy, imagelist[j].flatten())
    ax.w_yaxis.set_ticklabels(row_names)
    ax.w_xaxis.set_ticklabels(column_names)
    ax.set_xlabel('Past states')
    ax.set_ylabel('Next states')
    ax.set_zlabel('Probability')
    ax.set_title('Probability of moving from one state to another at hour ' + str(j) + ' of the day')
    # return the artists set
    return [im]
# kick off the animation
ani = animation.FuncAnimation(fig, updatefig, frames=range(len(imagelist)),
                              interval=1000)

ani.save('/Users/mathildebadoual/code/ev_controller/report/prices.mp4', writer='ffmpeg')

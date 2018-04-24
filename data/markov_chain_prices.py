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

horizon = 48
num_interp = 20

data = pd.read_csv('/Users/mathildebadoual/code/ev_controller/data/price_demand.csv')

data_price = data['Price']

data_price_grid = np.linspace(0, max(data_price), num_interp)
print(data_price_grid)
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
fig = plt.figure() # make figure

# make axesimage object
# the vmin and vmax here are very important to get the color map correct
im = plt.imshow(imagelist[0], cmap=plt.get_cmap('Reds'))

# function to update figure
def updatefig(j):
    # set the data in the axesimage object
    im.set_array(imagelist[j])
    # return the artists set
    return [im]
# kick off the animation
ani = animation.FuncAnimation(fig, updatefig, frames=range(len(imagelist)),
                              interval=1000)

ani.save('prices.mp4', writer='ffmpeg')

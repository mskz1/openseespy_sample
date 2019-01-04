import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import transforms
from matplotlib.path import Path
from matplotlib.patches import PathPatch

fig, ax = plt.subplots()
xdata, ydata = (0.2, 0.7), (0.5, 0.5)
ax.plot(xdata, ydata, "o")
ax.set_xlim((0, 1))

trans = (fig.dpi_scale_trans +
         transforms.ScaledTranslation(xdata[0], ydata[0], ax.transData))

# plot an ellipse around the point that is 150 x 130 points in diameter...
circle = mpatches.Ellipse((0, 0), 20 / 72, 10 / 72, angle=0, fill=None, transform=trans)
ax.add_patch(circle)

size = 9 / 72
# ox = self._x
# oy = self._y
ox = 0
oy = 0

# vertices = []
# codes = []
codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
vertices = [(ox, oy), (ox + size / 2, oy - size * 1.73 / 2), (ox - size / 2, oy - size * 1.73 / 2), (0, 0)]

vertices = np.array(vertices, float)
path = Path(vertices, codes)

trans = (fig.dpi_scale_trans +
         transforms.ScaledTranslation(xdata[1], ydata[1], ax.transData))

pathpatch = PathPatch(path, facecolor='None', edgecolor='k', transform=trans)
ax.add_patch(pathpatch)

plt.show()

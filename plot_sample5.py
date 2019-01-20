import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import transforms
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.lines as mlines
from scipy import signal, interpolate
import math
# fig, ax = plt.subplots()

from matplotlib.lines import Line2D

points = np.ones(3)  # Draw 3 points for each line
text_style = dict(horizontalalignment='right', verticalalignment='center',
                  fontsize=12, fontdict={'family': 'monospace'})
# marker_style = dict(linestyle=':', color='0.8', markersize=10,mfc="C0", mec="C0")


fig, ax = plt.subplots()

# marker_style.update(mec="None", markersize=15)
markers = ["$1$", r"$\frac{1}{2}$", "$f$", "$\u266B$",
           r"$\mathcircled{m}$", r"$\downarrow$", r"$\uparrow$"]

marker_style = dict(markersize=12, mfc="m", mec="m", markeredgewidth=0.01)
# line_style = dict(linestyle='--', color='m', linewidth=0.7)
line_style = dict(linestyle=(0, (10, 5)), color='m', linewidth=1.)


def div_line(p1, p2, n=5, len_limit=300):
    #  TODO 長さを計算？　最大長さをコントロール？
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    len = math.sqrt(dx ** 2 + dy ** 2)
    n_lim = math.ceil(len / len_limit)
    if n < n_lim:
        n = n_lim

    res_x = []
    res_y = []
    for i in range(n + 1):
        res_x.append(p1[0] + dx * i / n)
        res_y.append(p1[1] + dy * i / n)
    return res_x, res_y


# line = mlines.Line2D((0, 1000), (100, 100), marker=r"$\downarrow$", **line_style, **marker_style)
# ax.add_line(line)

xc, yc = div_line((0, 0), (3000, 200), n=5)
line = mlines.Line2D(xc, yc, marker=r"$\downarrow$", **line_style, **marker_style)
ax.add_line(line)

xc, yc = div_line((0, 500), (1000, 500), n=10)
line = mlines.Line2D(xc, yc, marker=r"$\downarrow$", **line_style, **marker_style)
ax.add_line(line)

xc, yc = div_line((0, 1000), (1600, 1000), n=5)
line = mlines.Line2D(xc, yc, marker=r"$\downarrow$", **line_style, **marker_style)
ax.add_line(line)

plt.axis('equal')

plt.show()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import transforms
from matplotlib.path import Path
from matplotlib.patches import PathPatch

fig, ax = plt.subplots()

# Path = mpatches.Path
path_data = [
    (Path.MOVETO, (1000, 1000)),
    (Path.LINETO, (2000, 1000)),
    (Path.LINETO, (2000, 2000)),
    (Path.LINETO, (1000, 2000)),
    (Path.CLOSEPOLY, (1000, 1000)),
]
codes, verts = zip(*path_data)
path = mpatches.Path(verts, codes)
patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)
ax.add_patch(patch)

path_data = [
    (Path.MOVETO, (0, 0)),
    (Path.LINETO, (2500, 0)),
    (Path.LINETO, (2500, 400)),
    (Path.LINETO, (0, 400)),
    (Path.CLOSEPOLY, (0, 0)),
]
codes, verts = zip(*path_data)
path = mpatches.Path(verts, codes)

trans = transforms.Affine2D().rotate_deg_around(0, 0, 45) + ax.transData

# patch = mpatches.PathPatch(path, facecolor='b', alpha=0.5, transform=trans)
patch = mpatches.PathPatch(path, facecolor='b', alpha=0.5)
patch.set_transform(trans)
ax.add_patch(patch)

# trans = (fig.dpi_scale_trans +
#          transforms.ScaledTranslation(0, 0, ax.transData))

# trans = ax.transData + transforms.Affine2D().rotate_deg_around(0, 0, 45)

# ax.set_xlim((-1000, 2000))
plt.axis('equal')

plt.show()

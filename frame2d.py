import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib import transforms


class Model:
    pass


class Node:
    def __init__(self, tag=0, x=0, y=0, loaded=False, supported=False):
        self._tag = tag
        self._x = x
        self._y = y
        self._loaded = loaded
        self._supported = supported

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    def plot(self, ax, disp_tag=False):
        ct_style = dict(color='k', linestyle='solid', linewidth=2., fill=True)
        text_style = dict(textcoords='offset points', color='k', size='x-small')

        ax.add_patch(mpatches.Circle((self._x, self._y), radius=1, **ct_style))
        if disp_tag:
            ax.annotate(str(self._tag), (self._x, self._y), xytext=(3, 3), **text_style)

    # def old_plot_support_pin(self, ax, view_range=1000):
    #     size = view_range * 0.02
    #     ox = self._x
    #     oy = self._y
    #     # vertices = []
    #     # codes = []
    #     codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
    #     vertices = [(ox, oy), (ox + size / 2, oy - size * 1.73 / 2), (ox - size / 2, oy - size * 1.73 / 2), (0, 0)]
    #
    #     vertices = np.array(vertices, float)
    #     path = Path(vertices, codes)
    #     pathpatch = PathPatch(path, facecolor='None', edgecolor='k')
    #     ax.add_patch(pathpatch)

    def plot_support_pin(self, ax, size=9 / 72):
        size = size
        # ox = 0
        # oy = 0
        # vertices = []
        # codes = []
        codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
        vertices = [(0, 0), (size / 2, -size * 1.73 / 2), (-size / 2, -size * 1.73 / 2), (0, 0)]

        vertices = np.array(vertices, float)
        path = Path(vertices, codes)

        trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(self._x, self._y, ax.transData))

        pathpatch = PathPatch(path, facecolor='None', edgecolor='k', transform=trans)
        ax.add_patch(pathpatch)

    # def old_plot_support_roller(self, ax, view_range=1000):
    #     size = view_range * 0.02
    #     xmin, xmax = ax.get_xlim()
    #     print(xmin, xmax)
    #     ox = self._x
    #     oy = self._y
    #     # vertices = []
    #     # codes = []
    #     codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
    #     vertices = [(ox, oy), (ox + size / 2, oy - size * 1.73 / 2), (ox - size / 2, oy - size * 1.73 / 2), (0, 0)]
    #
    #     codes += [Path.MOVETO] + [Path.LINETO] * 1 + [Path.CLOSEPOLY]
    #     vertices += [(ox + size / 2, oy - size * 1.73 / 2 - size / 4), (ox - size / 2, oy - size * 1.73 / 2 - size / 4),
    #                  (0, 0)]
    #     vertices = np.array(vertices, float)
    #     path = Path(vertices, codes)
    #     pathpatch = PathPatch(path, facecolor='None', edgecolor='k')
    #     ax.add_patch(pathpatch)

    def plot_support_roller(self, ax, size=9 / 72):
        size = size

        codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
        vertices = [(0, 0), (size / 2, - size * 1.73 / 2), (-size / 2, -size * 1.73 / 2), (0, 0)]

        codes += [Path.MOVETO] + [Path.LINETO] * 1 + [Path.CLOSEPOLY]
        vertices += [(size / 2, -size * 1.73 / 2 - size / 4), (-size / 2, -size * 1.73 / 2 - size / 4), (0, 0)]
        vertices = np.array(vertices, float)
        path = Path(vertices, codes)

        trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(self._x, self._y, ax.transData))

        pathpatch = PathPatch(path, facecolor='None', edgecolor='k', transform=trans)
        ax.add_patch(pathpatch)

    # def old_plot_support_fixed(self, ax, view_range=1000):
    #     size = view_range * 0.03
    #     ox = self._x
    #     oy = self._y
    #     support_patch = mpatches.Rectangle((ox - size * 0.5, oy - size * 1.0),
    #                                        size, size, zorder=9, hatch='////', fc='w', ec='m', alpha=0.5)
    #
    #     ax.add_patch(support_patch)

    def plot_support_fixed(self, ax, size=9 / 72):
        size = size
        # ox = self._x
        # oy = self._y
        trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(self._x, self._y, ax.transData))

        support_patch = mpatches.Rectangle((- size * 0.5, - size * 1.0),
                                           size, size, linewidth=1.,zorder=9, hatch='//////', fc='w', ec='k', alpha=1,
                                           transform=trans)

        ax.add_patch(support_patch)


class Element:
    def __init__(self, tag=0, node1=0, node2=0):
        self._tag = tag
        self._node1 = node1
        self._node2 = node2

    @property
    def node1(self):
        return self._node1

    @node1.setter
    def node1(self, node1):
        self._node1 = node1

    @property
    def node2(self):
        return self._node2

    @node2.setter
    def node2(self, node2):
        self._node2 = node2

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    def plot(self, ax, node1, node2, disp_tag=False):
        line_style = dict(color='b', linestyle='solid', linewidth=2., marker='.')
        text_style = dict(textcoords='offset points', color='b', size='x-small')

        ax.add_line(mlines.Line2D((node1.x, node2.x), (node1.y, node2.y), **line_style))
        if disp_tag:
            ax.annotate(str(self._tag), ((node1.x + node2.x) / 2, (node1.y + node2.y) / 2), xytext=(3, 3), **text_style)

    def plot_result(self):
        pass

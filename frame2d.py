import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Arc, RegularPolygon
from matplotlib import transforms
import math

NODE_R = 2 / 72
PIN_J_R = 3 / 72
ARROW_L = 24 / 72


def get_theta(p1, p2):
    """p1->p2の直線の、X軸からの傾き角度thetaを返す"""
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    dx = x2 - x1
    dy = y2 - y1
    return math.atan2(dy, dx)


def get_shortened_points(p1, p2, d=100):
    """直線の端部から距離dだけ縮めた座標を返す"""
    theta = get_theta(p1, p2)
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x11 = x1 + d * math.cos(theta)
    y11 = y1 + d * math.sin(theta)
    x21 = x2 - d * math.cos(theta)
    y21 = y2 - d * math.sin(theta)
    return (x11, y11), (x21, y21)


class Model:
    def __init__(self):
        self.nodes = {}
        self.elements = {}
        self.supports = {}

    def add_node(self, tag, x, y):
        self.nodes[tag] = Node(tag, x, y)

    def add_element(self, tag, node1, node2, pinned1=False, pinned2=False):
        self.elements[tag] = Element(tag, node1, node2, pinned1, pinned2)

    def get_node_by_tag(self, tag):
        return self.nodes[tag]

    def get_element_by_tag(self, tag):
        return self.elements[tag]

    def set_element_theta(self):
        """部材のX軸からの角度を設定"""
        for k, v in self.elements.items():
            n1 = self.get_node_by_tag(v.node1)
            n2 = self.get_node_by_tag(v.node2)
            v.theta = get_theta((n1.x, n1.y), (n2.x, n2.y))

    def _show_element_theta(self):
        for k, v in self.elements.items():
            print(v.theta)

    def add_support(self, tag, bcprop):
        """
        支点情報
        :param tag: 節点番号
        :param bcprop: 拘束情報 XYR '110'=pin, '010'=roller_x
        :return:
        """
        self.supports[tag] = bcprop

    def add_load_node(self, tag, px=0, py=0, m=0):
        """
        節点荷重を追加
        :param tag:
        :param px:
        :param py:
        :param m:
        :return:
        """
        node = self.get_node_by_tag(tag)
        node.loaded = True
        node.px = px
        node.py = py
        node.m = m

    def plot_model(self, ax, disp_tag=True):
        for k, v in self.nodes.items():
            v.plot(ax, disp_tag)

        for k, v in self.elements.items():
            n1 = self.get_node_by_tag(v.node1)
            n2 = self.get_node_by_tag(v.node2)
            v.plot(ax, n1, n2, disp_tag)

        for k, v in self.supports.items():
            node = self.get_node_by_tag(k)
            if v == '110':
                node.plot_support_pin(ax)
            elif v == '010':
                node.plot_support_roller(ax, 'X')
            elif v == '100':
                node.plot_support_roller(ax, 'Y')
            elif v == '111':
                node.plot_support_fixed(ax)


class Node:
    def __init__(self, tag=0, x=0, y=0, loaded=False, supported=False):
        """

        :param tag:
        :param x:
        :param y:
        :param loaded:
        :param supported:
        """
        self._tag = tag
        self._x = x
        self._y = y
        self._loaded = loaded
        self._supported = supported
        self.px = 0.  # 節点荷重x
        self.py = 0.
        self.m = 0.
        self.disp_x = 0.
        self.disp_y = 0.
        self.reac_x = 0.
        self.reac_y = 0.
        self.reac_M = 0.

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

    @property
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, loaded):
        self._loaded = loaded

    def drawCircleArrow(self, ax, radius, centX, centY, angle_, theta2_, color_='black'):
        # ========Line
        arc = Arc([centX, centY], radius, radius, angle=angle_,
                  theta1=0, theta2=theta2_, capstyle='round', linestyle='-', lw=2, color=color_)
        ax.add_patch(arc)

        # ========Create the arrow head
        endX = centX + (radius / 2) * np.cos(math.radians(theta2_ + angle_))  # Do trig to determine end position
        endY = centY + (radius / 2) * np.sin(math.radians(theta2_ + angle_))

        ax.add_patch(  # Create triangle as arrow head
            RegularPolygon(
                (endX, endY),  # (x,y)
                3,  # number of vertices
                radius / 9,  # radius
                math.radians(angle_ + theta2_),  # orientation
                color=color_
            )
        )
        # ax.set_xlim([centX - radius, centY + radius]) and ax.set_ylim([centY - radius, centY + radius])
        # Make sure you keep the axes scaled or else arrow will distort

    def plot(self, ax, disp_tag=False):
        """
        節点描画
        :param ax:
        :param disp_tag: 節点番号の表示/非表示
        """
        ct_style = dict(color='k', linestyle='solid', linewidth=1., fill=True, zorder=9)
        text_style = dict(textcoords='offset points', color='k', size='x-small', zorder=10)

        trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(self._x, self._y, ax.transData))
        ax.add_patch(mpatches.Circle((0, 0), radius=NODE_R, transform=trans, **ct_style))
        if disp_tag:
            ax.annotate(str(self._tag), (self._x, self._y), xytext=(4, 4), **text_style)

        # 節点荷重のプロット
        if self.loaded:
            line_style = dict(color='m', linestyle='solid', linewidth=2.)
            text_style = dict(textcoords='offset points', color='m', size='x-small')
            # arrow_style = dict(color='m', arrowstyle='simple', mutation_scale=7)
            arrow_style = dict(color='m', arrowstyle='->', linewidth=2, mutation_scale=12)
            px_v = abs(self.px)
            py_v = abs(self.py)
            m_v = abs(self.m)
            if self.px > 0.:  # 右矢印
                arrow = mpatches.FancyArrowPatch((NODE_R + 1 / 72, 0), (ARROW_L, 0), transform=trans, **arrow_style)
                ax.add_patch(arrow)
                ax.annotate("px=" + str(px_v), (self._x, self._y), xytext=(ARROW_L * 72, 0), **text_style)
            elif self.px < 0.:  # 左矢印
                arrow = mpatches.FancyArrowPatch((-NODE_R - 1 / 72, 0), (-ARROW_L, 0), transform=trans, **arrow_style)
                ax.add_patch(arrow)
                ax.annotate("px=" + str(px_v), (self._x, self._y), xytext=(-ARROW_L * 72, 0),
                            horizontalalignment='right', **text_style)

            if self.py > 0.:  # 上矢印
                arrow = mpatches.FancyArrowPatch((0, NODE_R + 1 / 72), (0, ARROW_L), transform=trans, **arrow_style)
                ax.add_patch(arrow)
                ax.annotate("py=" + str(py_v), (self._x, self._y), xytext=(0, ARROW_L * 72), rotation=90,
                            rotation_mode='anchor', **text_style)
            elif self.py < 0.:  # 下矢印
                arrow = mpatches.FancyArrowPatch((0, -NODE_R - 1 / 72), (0, -ARROW_L), transform=trans, **arrow_style)
                ax.add_patch(arrow)
                ax.annotate("py=" + str(py_v), (self._x, self._y), xytext=(0, -ARROW_L * 72), rotation=90,
                            horizontalalignment='right', rotation_mode='anchor', **text_style)

            if self.m > 0.:
                # TODO 2019-0113
                # arrow = mpatches.FancyArrowPatch((0, ARROW_L), (ARROW_L,0), transform=trans, connectionstyle='angle3,angleA=0,angleB=-90',**arrow_style)
                # arrow = mpatches.FancyArrowPatch((0, ARROW_L), (0,-ARROW_L), transform=trans, connectionstyle='arc,angleA=0,armA=30,angleB=180,armB=30,rad=-3',**arrow_style)
                # arrow = mpatches.FancyArrowPatch((0, ARROW_L), (0, -ARROW_L), transform=trans, connectionstyle='arc3,rad=-0.9',**arrow_style)
                # ax.add_patch(arrow)
                self.drawCircleArrow(ax, 300, self.x, self.y, 75, 180, color_='m')
                pass

    def plot_support_pin(self, ax, size=9 / 72):
        """
        ピン支点の描画
        :param ax:
        :param size: 作図サイズ（ポイント）
        """
        size = size
        codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
        vertices = [(0, 0), (size / 2, -size * 1.73 / 2), (-size / 2, -size * 1.73 / 2), (0, 0)]

        # vertices = np.array(vertices, float)
        path = Path(vertices, codes)
        trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(self._x, self._y, ax.transData))
        pathpatch = PathPatch(path, facecolor='None', edgecolor='k', transform=trans)
        ax.add_patch(pathpatch)

    def plot_support_roller(self, ax, direc='X', size=9 / 72):
        """ローラー支点の描画
        :param ax:
        :param direc:ローラーの方向 'X' or 'Y'
        :param size: 作図サイズ（ポイント）
        """
        size = size
        codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
        if direc == 'X':
            vertices = [(0, 0), (size / 2, - size * 1.73 / 2), (-size / 2, -size * 1.73 / 2), (0, 0)]
        else:
            vertices = [(0, 0), (size * 1.73 / 2, size / 2), (size * 1.73 / 2, -size / 2), (0, 0)]

        codes += [Path.MOVETO] + [Path.LINETO] * 1 + [Path.CLOSEPOLY]
        if direc == 'X':
            vertices += [(size / 2, -size * 1.73 / 2 - size / 4), (-size / 2, -size * 1.73 / 2 - size / 4), (0, 0)]
        else:
            vertices += [(size * 1.73 / 2 + size / 4, size / 2), (size * 1.73 / 2 + size / 4, -size / 2), (0, 0)]

        # vertices = np.array(vertices, float)
        path = Path(vertices, codes)

        trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(self._x, self._y, ax.transData))

        pathpatch = PathPatch(path, facecolor='None', edgecolor='k', transform=trans)
        ax.add_patch(pathpatch)

    def plot_support_fixed(self, ax, size=9 / 72):
        """
        固定支点の描画
        :param ax:
        :param size: 作図サイズ（ポイント）
        """
        size = size
        w = 1.2 * size
        h = 0.7 * size
        trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(self._x, self._y, ax.transData))

        support_patch = mpatches.Rectangle((-w * 0.5, -h * 1.0), w, h, linewidth=0.9, zorder=2, hatch='//////', fc='w',
                                           ec='k', alpha=1, transform=trans)
        ax.add_patch(support_patch)
        # 左右端、下端を白線で上描き
        codes = [Path.MOVETO] + [Path.LINETO] * 3
        vertices = [(w / 2, 0), (w / 2, -h), (-w / 2, -h), (-w / 2, 0)]
        path = Path(vertices, codes)
        pathpatch = PathPatch(path, facecolor='None', edgecolor='w', linewidth=1., transform=trans, zorder=3)
        ax.add_patch(pathpatch)


class Element:
    def __init__(self, tag=0, node1=0, node2=0, pinned1=False, pinned2=False):
        """

        :param tag:
        :param node1:節点番号
        :param node2:節点番号
        :param pinned1:
        :param pinned2:
        """
        self._tag = tag
        self._node1 = node1
        self._node2 = node2
        self._pinned1 = pinned1
        self._pinned2 = pinned2
        self.resM1 = 0.
        self.resN1 = 0.
        self.resQ1 = 0.
        self.resM2 = 0.
        self.resN2 = 0.
        self.resQ2 = 0.
        self._theta = 0.

    def set_theta(self):
        # _node1 は節点番号
        self._theta = get_theta((self._node1.x, self._node1.y), (self._node2.x, self._node2.y))

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, theta):
        self._theta = theta

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

    @property
    def pinned1(self):
        return self._pinned1

    @pinned1.setter
    def pinned1(self, pinned):
        self._pinned1 = pinned

    @property
    def pinned2(self):
        return self._pinned2

    @pinned2.setter
    def pinned2(self, pinned):
        self._pinned2 = pinned

    def plot(self, ax, node1, node2, disp_tag=False):
        # line_style = dict(color='b', linestyle='solid', linewidth=2., marker='.')
        line_style = dict(color='b', linestyle='solid', linewidth=2.)
        text_style = dict(textcoords='offset points', color='b', size='x-small')

        ax.add_line(mlines.Line2D((node1.x, node2.x), (node1.y, node2.y), **line_style))

        if disp_tag:
            ax.annotate(str(self._tag), ((node1.x + node2.x) / 2, (node1.y + node2.y) / 2), xytext=(3, 3), **text_style)

        # ct_style = dict(color='b', linestyle='solid', linewidth=1., fill=True, zorder=9)
        ct_style = dict(ec='b', fc='w', linestyle='solid', linewidth=1., fill=True, zorder=9)
        if self.pinned1:
            theta = self.theta
            dx = (NODE_R + PIN_J_R) * math.cos(theta)
            dy = (NODE_R + PIN_J_R) * math.sin(theta)

            trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(node1.x, node1.y, ax.transData))
            ax.add_patch(mpatches.Circle((dx, dy), radius=PIN_J_R, transform=trans, **ct_style))
        if self.pinned2:
            theta = self.theta
            dx = (NODE_R + PIN_J_R) * math.cos(theta)
            dy = (NODE_R + PIN_J_R) * math.sin(theta)

            trans = (ax.get_figure().dpi_scale_trans + transforms.ScaledTranslation(node2.x, node2.y, ax.transData))
            ax.add_patch(mpatches.Circle((-dx, -dy), radius=PIN_J_R, transform=trans, **ct_style))

    def plot_result(self):
        pass

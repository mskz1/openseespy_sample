import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

fig, ax = plt.subplots()

x = [0, 1]
y = [0, 0]

ax.plot(x, y)

dy = 5 / 72

i = 1  # 0 for dx

tmp = ax.transData.transform([(0, 0), (1, 1)])
tmp = tmp[1, i] - tmp[0, i]  # 1 unit in display coords
tmp = 1 / tmp  # 1 pixel in display coords
tmp = tmp * dy * ax.get_figure().get_dpi()  # shift pixels in display coords

ax.plot(x, y)

ax.annotate("", [0, tmp], [1, tmp],
            size=10,
            arrowprops=dict(arrowstyle='<|-|>'))

plt.show()

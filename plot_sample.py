import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

fig, ax = plt.subplots()

x = [0, 1]
y = [0, 0]

# Plot horizontal line
ax.plot(x, y)

dy = 5 / 72

offset = transforms.ScaledTranslation(0, dy, ax.get_figure().dpi_scale_trans)
verttrans = ax.transData + offset

# Plot horizontal line 5 points above (works!)
ax.plot(x, y, transform=verttrans)

# Draw arrow 5 points above line (doesn't work--not vertically translated)
ax.annotate("", (0, 0), (1, 0),
            size=10,
            transform=verttrans,
            arrowprops=dict(arrowstyle='<|-|>'))

plt.show()

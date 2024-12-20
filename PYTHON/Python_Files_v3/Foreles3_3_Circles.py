import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle

fig = plt.figure(figsize=(5,8))

ax1 = fig.add_axes((0.1, 0.05, 0.8, 0.40))
ax2 = fig.add_axes((0.1, 0.55, 0.8, 0.40))


circle = mpatches.Circle((0.5,0.5), 0.2, color='red')
ax1.add_patch(circle)

circle2 = mpatches.Circle((0.5,0.4), 0.3, color='blue')

ax2.add_patch(circle2)


plt.title('Colored Circle')

plt.show()
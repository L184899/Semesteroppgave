import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RadioButtons

xvals = np.linspace(1,10, 50)
ycos = [math.cos(x) for x in xvals]
ysin = [math.sin(x) for x in xvals]
fig = plt.figure(figsize=(8,5))

ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
axRadio = fig.add_axes((0.7, 0.8, 0.2, 0.2))

lines = ax.plot(xvals, ycos, color="red")
def on_velg(funk):
    if funk == 'Cos':
        lines[0].set_color('red')
        lines[0].set_ydata(ycos)
    if funk == 'Sin':
        lines[0].set_color('blue')
        lines[0].set_ydata(ysin)
    plt.draw()

radio_button = RadioButtons(axRadio, ('Cos', 'Sin'))
radio_button.on_clicked(on_velg)
plt.show()
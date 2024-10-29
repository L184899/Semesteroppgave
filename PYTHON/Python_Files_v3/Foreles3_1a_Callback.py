import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from datetime import  datetime as dt

fig = plt.figure(figsize=(4,3))

def on_getTime(event):
    text = f"Min={dt.now().minute}: Sec={dt.now().second}"
    axtime.set_title(text)
    plt.draw()

axtime = fig.add_axes((0.40, 0.05, 0.3, 0.2))
buttonTime = Button(axtime, label="Update time")

buttonTime.on_clicked(on_getTime)
plt.show()
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
import matplotlib.patches as mpatches

#Generater random data for a year
# centervals are values average values for each month
# samedata = false, new data each time program is called
import random
from random import randint
def GenereateRandomYearDataList(intencity:float, seed:int=0) -> list[int]:
    """
    :param intencity: Number specifying size, amplitude
    :param seed: If given, same data with seed is generated
    :return:
    """
    if seed != 0:
        random.seed(seed)
    centervals = [200,150,100, 75,75,75, 50, 75, 100, 150, 200, 250, 300]
    centervals = [x * intencity for x in centervals]
    nox = centervals[0]
    inc = True
    noxList = []
    for index in range(1,365):
        if randint(1, 100) > 50:
            inc = not inc
        center = centervals[int(index / 30)]
        dx = min(2.0, max(0.5, nox / center ))
        nox =  nox + randint(1,5) / dx if inc else nox - randint( 1, 5) * dx
        nox = max(10, nox)
        noxList.append(nox)
    return noxList

krnon_nox_year = GenereateRandomYearDataList(intencity=1.0, seed = 2)
nord_nox_year = GenereateRandomYearDataList(intencity=.3, seed = 1)

#create figure and 3 axis
fig = plt.figure(figsize=(13, 5))

axNox = fig.add_axes((0.05, 0.05, 0.45, 0.9))

quarterYear =  int(input("Kvartal 1-4  (0=Hele Året)  : "))

def get_interval():
    num_labels = 12
    xlabels = ['J' ,'F' ,'M' ,'A' ,'M' ,'J', 'J', 'A', 'S', 'O', 'N', 'D']
    xticks = np.linspace(15, 345, num_labels)
    days_interval = (1, 365)
    if quarterYear == 1:
        xticks = [15,45,75]
        xlabels = ['Jan', 'Feb', 'Mars']
        days_interval = (0,90)
    if quarterYear == 2:
        xticks = [15,45,75]
        xlabels = ['April', 'Mai', 'Juni']
        days_interval = (90, 180)
    if quarterYear == 3:
        xticks = [15, 45, 75]
        xlabels = ['July', 'Aug', 'Sept']
        days_interval = (180, 270)
    if quarterYear == 4:
        xticks = [15, 45, 75]
        xlabels = ['Okt', 'Nov', 'Des']
        days_interval = (270, 360)
    axNox.set_xticks(xticks)
    axNox.set_xticklabels(xlabels)
    axNox.set_title("NOX År" if quarterYear == 0 else f"NOK Kvartal {quarterYear}")
    return days_interval

def plot_graph():

    days_interval = get_interval()
    nord_nox = nord_nox_year[days_interval[0]:days_interval[1]]
    kron_nox = krnon_nox_year[days_interval[0]:days_interval[1]]
    days = len(nord_nox)
    list_days = np.linspace(1, days, days)

    l1, = axNox.plot(list_days, nord_nox, 'blue')
    l2, = axNox.plot(list_days, kron_nox, 'red')


    lines = [l1, l2]
    axNox.legend(lines, ["Nordnes", "Kronstad"])
    axNox.grid(linestyle='--')

    plt.draw()

plot_graph()
plt.show()


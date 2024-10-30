import math
from cProfile import label

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import Slider
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

kron_nox_year = GenereateRandomYearDataList(intencity=1.0, seed = 2)
nord_nox_year = GenereateRandomYearDataList(intencity=.3, seed = 1)

kron_asph_year = GenereateRandomYearDataList(intencity=1.3, seed = 3)
nord_asph_year = GenereateRandomYearDataList(intencity=.6, seed = 4)



#create figure and 3 axis
fig = plt.figure(figsize=(13, 5))

axNok = fig.add_axes((0.1, 0.05, 0.45, 0.9))
axInterval = fig.add_axes((0.45, 0.5, 0.1, 0.25))
axData = fig.add_axes((0.45, 0.20 , 0.1, 0.25))
axBergen = fig.add_axes((0.5, 0.05, 0.5, 0.9))
axSliderStart = fig.add_axes((0.1 , 0.05 , 0.45, 0.05))
axSliderEnd = fig.add_axes((0.1 , 0.09 , 0.45, 0.05))

axInterval.patch.set_alpha(0.5)
axData.patch.set_alpha(0.5)

coordinates_Nordnes = (50, 300)
coordinates_Kronstad = (500, 900)
coordinates_Festplassen = (320, 500)
days_interval = (1,365)
marked_point = (0,0)
current_data_type = "NOX"



def on_day_interval(kvartal):
    global days_interval, marked_point
    axNok.cla()
    days_interval = (1,365)
    if kvartal == '1. Kvartal':
        days_interval = (1,90)
    if kvartal == '2. Kvartal':
        days_interval = (90, 180)
    if kvartal == '3. Kvartal':
        days_interval = (180,270)
    if kvartal == '4. Kvartal':
        days_interval = (270,365)
    marked_point = (0, 0)

    plot_graph()


def on_click(event) :
    global marked_point
    if ax := event.inaxes:
        if ax == axBergen:
            marked_point = (event.xdata, event.ydata)
            plot_graph()

#estimate NOX value based on the two measuring stations
def CalcPointValue(valN, valK):
    distNordnes = math.dist(coordinates_Nordnes, marked_point)
    distKronstad = math.dist(coordinates_Kronstad, marked_point)
    distNordnesKronstad = math.dist(coordinates_Nordnes, coordinates_Kronstad)
    val = (1 - distKronstad /(distKronstad+distNordnes)) * valK  + (1 - distNordnes /(distKronstad+distNordnes))* valN
    val = val * ( distNordnesKronstad / (distNordnes + distKronstad) ) ** 4

    return val
def CalcFestValue(valN, valK):
    distNordnes = math.dist(coordinates_Nordnes, coordinates_Festplassen)
    distKronstad = math.dist(coordinates_Kronstad, coordinates_Festplassen)
    distNordnesKronstad = math.dist(coordinates_Nordnes, coordinates_Kronstad)
    val = (1 - distKronstad /(distKronstad+distNordnes)) * valK  + (1 - distNordnes /(distKronstad+distNordnes))* valN
    val = val * ( distNordnesKronstad / (distNordnes + distKronstad) ) ** 4

    return val

# Make two circles in Nordnes and Kronstad
def draw_circles_stations():
    circle = mpatches.Circle((50,300), 20, color='blue')
    axBergen.add_patch(circle)
    circle = mpatches.Circle((500, 900), 20, color='red')
    axBergen.add_patch(circle)
    circle = mpatches.Circle((320, 510), 20, color='green')
    axBergen.add_patch(circle)

def draw_label_and_ticks():
    num_labels = 12
    xlabels = ['J' ,'F' ,'M' ,'A' ,'M' ,'J', 'J', 'A', 'S', 'O', 'N', 'D']
    xticks = np.linspace(15, 345, num_labels)
    if days_interval[1] == 90:
        xticks = [15,45,75]
        xlabels = ['Jan', 'Feb', 'Mars']
    if days_interval[1] == 180:
        xticks = [15,45,75]
        xlabels = ['April', 'Mai', 'Juni']
    if days_interval[1] == 270:
        xticks = [15, 45, 75]
        xlabels = ['July', 'Aug', 'Sept']
    if days_interval[0] == 270:
        xticks = [15, 45, 75]
        xlabels = ['Okt', 'Nov', 'Des']
    axNok.set_xticks(xticks)
    axNok.set_xticklabels(xlabels)

# Funksjoner for å oppdatere grafen
def on_data_type_change(label):
    global current_data_type
    current_data_type = label
    plot_graph()

    days_interval = (1, 365)
def on_slider_update(val):
    global days_interval
    start_day = int(Slider_intervall_start.val)
    end_day = int(Slider_intervall_end.val)
    if start_day < end_day:
        days_interval = (start_day, end_day)
        plot_graph()


def plot_graph():
    axNok.cla()
    axBergen.cla()

    if current_data_type == "NOX":
        nord_data = nord_nox_year
        kron_data = kron_nox_year

    else:
        nord_data = nord_asph_year
        kron_data = kron_asph_year

    nord_nox = nord_data[days_interval[0]:days_interval[1]]
    kron_nox = kron_data[days_interval[0]:days_interval[1]]
    days = len(nord_nox)
    list_days = np.linspace(1, days, days)

#draw the marked point & the orange graph
    l4 = None
    if marked_point != (0,0):
        nox_point = [CalcPointValue(nord_nox[i], kron_nox[i])  for i in range(days)]
        l4, = axNok.plot(list_days, nox_point, 'darkorange')
        circle = mpatches.Circle((marked_point[0], marked_point[1]), 20, color='orange')
        axBergen.add_patch(circle)
    if coordinates_Festplassen != (0,0):
        nox_point = [CalcFestValue(nord_nox[i], kron_nox[i])  for i in range(days)]
        l3, = axNok.plot(list_days, nox_point, color='green')


    l1, = axNok.plot(list_days, nord_nox, 'blue')
    l2, = axNok.plot(list_days, kron_nox, 'red')
    axData.set_title(f"{current_data_type} verdier")
    axInterval.set_title("Intervall")

    kronavg = np.mean(kron_nox)
    nordavg = np.mean(nord_nox)
    festavg = np.mean([CalcFestValue(nord_nox[i], kron_nox[i])  for i in range(days)])
    markavg = np.mean([CalcPointValue(nord_nox[i], kron_nox[i])  for i in range(days)])

    lines = [l1, l2, l3] if l4 is None else [l1, l2, l3, l4]
    axNok.legend(lines, [f"Nordnes Gjennomsnitt: {nordavg:.2f}", f"Krontsad Gjennomsnitt: {kronavg:.2f}", f"Festplassen Gjennomsnitt: {festavg:.2f}", f"Markert plass Gjennomsnitt: {markavg:.2f}"], loc='upper left')
    axNok.grid(linestyle='--')
    draw_label_and_ticks()

    #Plot Map of Bergen
    axBergen.axis('off')
    img = mpimg.imread('Bergen2.png')
    img = axBergen.imshow(img)
    axBergen.set_title("Kart Bergen")
    draw_circles_stations()
    plt.draw()

plot_graph()
# draw radiobutton interval
listFonts = [12] * 5
listColors = ['yellow'] * 5
radio_button = RadioButtons(axInterval, ('År',
                                          '1. Kvartal',
                                          '2. Kvartal',
                                          '3. Kvartal',
                                          '4. Kvartal'),
                            label_props={'color': listColors, 'fontsize' : listFonts},
                            radio_props={'facecolor': listColors,  'edgecolor': listColors},
                            )
axInterval.set_facecolor('darkblue')
radio_button.on_clicked(on_day_interval)

# Radioknapp for å bytte mellom NOX og Asfaltstøv
listFonts = [10] * 2
listColors = ['yellow'] * 2
radio_button_data = RadioButtons(axData, ('NOX', 'Asfaltstøv'),
                            label_props = {'color': listColors, 'fontsize': listFonts},
                            radio_props = {'facecolor': listColors, 'edgecolor': listColors},
                            )
axData.set_facecolor('darkblue')
radio_button_data.on_clicked(on_data_type_change)

intervalmin:int = 1
intervalmax:int = 365

Slider_intervall_start = Slider(axSliderStart, label = 'start', valmin = 1 , valmax = 365 , valinit = intervalmin , valstep= 1)
Slider_intervall_end = Slider(axSliderEnd, label = 'end', valmin = 1 , valmax = 365 , valinit = intervalmax , valstep = 1)

Slider_intervall_start.on_changed(on_slider_update)
Slider_intervall_end.on_changed(on_slider_update)
# noinspection PyTypeChecker
plt.connect('button_press_event', on_click)

plt.show()


import math
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, TextBox, Slider
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
from Hjelpemetoder import GenereateRandomYearDataList


kron_nox_year = GenereateRandomYearDataList(intencity=1.0, seed = 2)
nord_nox_year = GenereateRandomYearDataList(intencity=.3, seed = 1)


#create figure and 3 axis
fig = plt.figure(figsize=(13, 5))

axNok = fig.add_axes((0.05, 0.05, 0.45, 0.9))
axInterval = fig.add_axes((0.50, 0.5, 0.1, 0.25))
axBergen = fig.add_axes((0.5, 0.05, 0.5, 0.9))

axTextBoxStart = fig.add_axes((0.05, 0.038, 0.45, 0.05))
axTextBoxSlutt = fig.add_axes((0.50, 0.3, 0.1, 0.05))

axInterval.patch.set_alpha(0.5)

coordinates_Nordnes = (61, 266)
coordinates_Kronstad = (637, 1120)
days_interval = (1,365)
marked_point = (0,0)
nord_nox = nord_nox_year[days_interval[0]:days_interval[1]]
days = len(nord_nox)

def update_range():
    slider_intervall.valmin = days_interval[0]
    slider_intervall.valmax = days_interval[1]-1

def on_day_interval(kvartal):
    global days_interval, marked_point
    axNok.cla()
    days_interval = (1,365)
    if kvartal == '1. Kvartal':
        days_interval = (1,90)
        update_range()
    if kvartal == '2. Kvartal':
        days_interval = (90, 180)
        update_range()
    if kvartal == '3. Kvartal':
        days_interval = (180,270)
        update_range()
    if kvartal == '4. Kvartal':
        days_interval = (270,365)
        update_range()
    marked_point = (0, 0)
    plot_graph()

def on_click(event) :
    global marked_point
    if ax := event.inaxes:
        if ax == axBergen:
            marked_point = (event.xdata, event.ydata)
            plot_graph()


#estimate NOX value based on the two measuring stations
def calc_point_value(val_n, val_k):
    distNordnes = math.dist(coordinates_Nordnes, marked_point)
    distKronstad = math.dist(coordinates_Kronstad, marked_point)
    distNordnesKronstad = math.dist(coordinates_Nordnes, coordinates_Kronstad)
    val = (1 - distKronstad /(distKronstad+distNordnes)) * val_k  + (1 - distNordnes /(distKronstad+distNordnes))* val_n
    val = val * ( distNordnesKronstad / (distNordnes + distKronstad) ) ** 4

    return val


# Make two circles in Nordnes and Kronstad
def draw_circles_stations():
    circle = mpatches.Circle((61,266), 20, color='blue')
    axBergen.add_patch(circle)
    circle = mpatches.Circle((637, 1120), 20, color='red')
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

def plot_graph():
    axNok.cla()
    axBergen.cla()
    nord_nox = nord_nox_year[days_interval[0]:days_interval[1]]
    kron_nox = kron_nox_year[days_interval[0]:days_interval[1]]
    days = len(nord_nox)
    list_days = np.linspace(1, days, days)

    averageList = []
    averageList.extend(nord_nox)
    averageList.extend(kron_nox)
    averageNOX = round(statistics.mean(averageList), 2)
    averageKron = round(statistics.mean(kron_nox), 2)
    averagePercent = round((averageNOX/averageKron) * 100, 2)
    NOXStreng1 = "Gjennomsnittlig NOX er: " + str(averageNOX)
    NOXStreng2 = "det er " + str(averagePercent) + "%" + " i forhold til Kronstad"

#draw the marked point & the orange graph
    l3 = None
    if marked_point != (0,0):
        nox_point = [calc_point_value(nord_nox[i], kron_nox[i])  for i in range(days)]
        l3, = axNok.plot(list_days, nox_point, 'darkorange')
        circle = mpatches.Circle((marked_point[0], marked_point[1]), 20, color='orange')
        axBergen.add_patch(circle)

    l1, = axNok.plot(list_days, nord_nox, 'blue')
    l2, = axNok.plot(list_days, kron_nox, 'red')
    l4, = axNok.plot(0, 0, 'white')
    l5, = axNok.plot(0, 0, 'white')
    axNok.set_xlim(1, days)
    axNok.relim()
    axNok.autoscale_view()
    axNok.set_title("NOX verdier")
    axInterval.set_title("Intervall")

    lines = [l1, l2, l4, l5] if l3 is None else [l1, l2, l3, l4, l5]
    axNok.legend(lines, ["Nordnes", "Kronstad", NOXStreng1, NOXStreng2]) if l3 is None \
        else axNok.legend(lines, ["Nordnes", "Kronstad", "Markert plass", NOXStreng1, NOXStreng2])
    axNok.grid(linestyle='--')
    draw_label_and_ticks()

    #Plot Map of Bergen
    axBergen.axis('off')
    img = mpimg.imread('Malestasjoner.png')
    axBergen.imshow(img)
    axBergen.set_title("Kart Bergen")
    draw_circles_stations()
    plt.draw()


plot_graph()
"""
text_box_start = TextBox(axTextBoxStart, "Startdag:", textalignment="center", initial="1")
labelStart = text_box_start.ax.get_children()[0]
labelStart.set_position((0.5, 1.5))
labelStart.set_verticalalignment('top')
labelStart.set_horizontalalignment('center')

text_box_slutt = TextBox(axTextBoxSlutt, "Sluttdag:", textalignment="center", initial="365")
labelSlutt = text_box_slutt.ax.get_children()[0]
labelSlutt.set_position((0.5, 1.5))
labelSlutt.set_verticalalignment('top')
labelSlutt.set_horizontalalignment('center')
"""

slider_intervall = Slider(ax = axTextBoxStart,
                          valmin=days_interval[0],
                          valmax=days_interval[1]-1,
                          label = "Intervall",
                          valinit=1,
                          valfmt='%0.0f',
                          orientation="horizontal")
labelStart = slider_intervall.ax.get_children()[4]
labelStart.set_position((0.5, 0.7))
labelStart.set_verticalalignment('top')
labelStart.set_horizontalalignment('center')

def update(val):
    global days
    global days_interval
    val = int(slider_intervall.val)
    days_interval = val, days_interval[1]
    fig.canvas.draw_idle()
    axNok.set_xlim(1, days)
    plot_graph()
    plt.draw()

slider_intervall.on_changed(update)

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
# noinspection PyTypeChecker
plt.connect('button_press_event', on_click)

plt.show()


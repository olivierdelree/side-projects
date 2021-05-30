"""
Created 30/05/2021 at 17:20 GMT by grump
"""

import threading
import re
from subprocess import Popen, PIPE

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

series = pd.Series(data=[0], index=['00:00:00'])


def main():
    # Creating a thread to gather the ping information and store it in `series`
    thread = threading.Thread(target=get_ping_info, daemon=True)
    thread.start()

    # Generate the figure and its axis and create the animation of the ping
    # over time
    figure = plt.figure(figsize=(16, 9), num='PingPlotter', tight_layout=True)
    axes = figure.add_subplot(1, 1, 1)
    plt.xticks(rotation='vertical')
    plt.ylim((0, 100))
    plt.plot(series.index[0], series.iloc[0], scalex=True, c='black', aa=True)
    animation = FuncAnimation(fig=figure, func=animate, interval=1000)
    plt.show()


def get_ping_info():
    global series
    command = 'cmd /c "ping 8.8.8.8 -t"'
    process = Popen(command, shell=True, stdout=PIPE, bufsize=1,
                    universal_newlines=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break

        match = re.search('time=(.+)ms', line)
        if match:
            temporary_series = pd.Series(data=[int(match[1])],
                                         index=[pd.Timestamp.now().strftime(
                                             '%H:%M:%S')])
            series = series.append(temporary_series)


def animate(_):
    if (series.index[0] == '00:00:00') and (series.iloc[0] == 0):
        series.drop(index='00:00:00', inplace=True)
        return

    timeframe = 60
    if len(series) > timeframe:
        x = series.index[(len(series) - timeframe):len(series)]
        y = series.iloc[(len(series) - timeframe):len(series)]
    else:
        x = series.index
        y = series.values

    plt.clf()
    plt.xticks(rotation='vertical')
    plt.plot(x, y, scalex=True, scaley=True, c='black', aa=True)


if __name__ == '__main__':
    main()

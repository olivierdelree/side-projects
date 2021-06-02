"""
This is a simple simulation of Conway's Game of Life using matplotlib.

Usage:
    game_of_life.py [options]

Options:
    -h, --help      Shows this help screen.
    -r <speed>, --refresh-speed <speed>
                    Sets the refresh speed of the plot in milliseconds.
                    [default: 500]
    -s <size>, --size <size>
                    Size of the board to use. For sizes larger than
                    50, the refresh-speed is very likely to be heavily
                    impacted. [default: 100]
    -p <probability>, --probability <probability>
                    The probability of any cell being live when
                    generating the board. [default: 0.1]

------------------------------------------------------------------------

Created 01/06/2021 at 21:32 GMT by grump

The rules to Conway's Game of Life are as follow:
    1. Any live cell with fewer than two live neighbours dies, as if by
       underpopulation.
    2. Any live cell with two or three live neighbours lives on to the
       next generation.
    3. Any live cell with more than three live neighbours dies, as if by
       overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live
       cell, as if by reproduction.
"""

from PyQt5 import QtGui

from docopt import docopt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Make the animation actually animated with PyCharm
matplotlib.use('Qt5Agg')

# Create a figure, change background to black, and set axes to white
figure = plt.figure(figsize=(9, 9), tight_layout=True, facecolor='black',
                    num='The Game of Life')
axes = figure.add_subplot(1, 1, 1)
axes.tick_params(axis='both', which='both', top=False, right=False,
                 bottom=False, left=False, labelbottom=False, labelleft=False)
axes.set_facecolor('black')
for spine in axes.spines:
    axes.spines[spine].set_color('white')
# Set the window icon and figure position
plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon('icon.png'))
plt.get_current_fig_manager().window.setGeometry(20, 50, 1000, 1000)

board = []


def main(interval, size, probability):
    global board
    size, interval = int(size), int(interval)
    probability = float(probability)

    axes.set_xlim(size - 0.5, size + 0.5)
    axes.set_ylim(size - 0.5, size + 0.5)

    board = generate_random_board((size, size), probability)

    animation = FuncAnimation(figure, animate, interval=interval, fargs=[size])
    plt.show()


def animate(i, size):
    global board
    axes.clear()                                # Clear the previous plot
    axes.set_xlim(-0.5, size - 0.5)
    axes.set_ylim(-0.5, size - 0.5)

    board = generate_next_board(board)
    df = translate_to_coordinates(board)

    # Add a grid
    grid_ticks = np.arange(-0.5, size - 0.5, 1)
    axes.set_xticks(grid_ticks)
    axes.set_yticks(grid_ticks)
    axes.grid(b=True, which='major', color='white', linewidth=0.5)

    sns.scatterplot(x='x_coord', y='y_coord', data=df, color='white',
                    marker='s')


def generate_next_board(current_board):
    # Generate the next board using the current one
    dimensions = current_board.shape
    next_board = np.zeros(dimensions)
    # Get the neighbour count for each point and determine its state
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            neighbours = count_neighbours(current_board, (i, j))

            if not current_board[i, j]:     # Cell is dead
                if neighbours == 3:         # Does it have exactly 3 neighbours
                    next_board[i, j] = 1
            else:                           # Cell is alive
                if 2 <= neighbours <= 3:    # Does it have between 2 and 3
                    next_board[i, j] = 1    # neighbours (both inclusive)

    return next_board


def generate_random_board(dimensions, probability):
    random_board = np.zeros(dimensions)
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            random_board[i, j] = np.random.choice([0, 1], p=[1 - probability,
                                                             probability])

    return random_board


def count_neighbours(board, point):
    x, y = point
    neighbours = 0
    for i in range(max(0, x - 1), x + 2):
        for j in range(max(0, y - 1), y + 2):
            try:
                if board[i, j]:
                    neighbours += 1
            except IndexError:
                continue

    # Adjust for the cell counting itself if it is alive
    if board[point]:
        neighbours -= 1
    return neighbours


def translate_to_coordinates(board):
    # Generates a pd.DataFrame from a NumPy array for plotting
    coordinates = np.nonzero(board)
    return pd.DataFrame({'x_coord': coordinates[0], 'y_coord': coordinates[1]})


if __name__ == '__main__':
    arguments = docopt(__doc__.split('-' * 72)[0])
    main(arguments['--refresh-speed'], arguments['--size'], arguments[
        '--probability'])

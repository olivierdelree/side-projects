"""
This is a simple simulation of Conway's Game of Life using matplotlib.

Usage:
    game_of_life.py [options]

Options:
    -h, --help      Shows this help screen.
    -r <speed>, --refresh-speed <speed>
                    Sets the refresh speed of the plot in milliseconds.
                    [default: 200]
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

scale_factor = 0

board = []


def main(interval, size, probability):
    global board
    global scale_factor

    # Casting arguments to proper types
    size, interval = int(size), int(interval)
    probability = float(probability)

    scale_factor = (10 / size)

    # Create a figure, change background to black, and set axes to white
    figure = plt.figure(figsize=(9, 9), tight_layout=True, facecolor='black',
                        num='The Game of Life')
    axes = figure.add_subplot(1, 1, 1)

    # Set the window icon and figure position
    plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon('icon.png'))
    plt.get_current_fig_manager().window.setGeometry(20, 50, 1000, 1000)

    # Adding a grid and formatting axes to make the plot look more like a board
    # Grid
    grid_ticks = np.arange(-0.5, size - 0.5, 1)
    axes.set_xticks(grid_ticks)
    axes.set_yticks(grid_ticks)
    axes.grid(which='major', c='grey', lw=(10 * scale_factor), zorder=10.0)
    # Limits
    axes.set_xlim(-0.5, size - 0.5)
    axes.set_ylim(-0.5, size - 0.5)
    # Axes appearance
    axes.tick_params(axis='both', which='both', top=False, right=False,
                     bottom=False, left=False, labelbottom=False,
                     labelleft=False)
    axes.set_facecolor('black')
    for spine in axes.spines:
        axes.spines[spine].set_color('grey')
        axes.spines[spine].set_linewidth(10 * scale_factor)

    # Generating and plotting the first board
    board = generate_random_board((size, size), probability)
    generate_seaborn_scatter_from_board(board)

    # Creating animation object to avoid garbage collection of the animation
    animation = FuncAnimation(figure, animate, fargs=[axes], interval=interval)
    plt.show()


def animate(i, axes):
    global board
    # Clear the previous cells
    axes.get_children()[0].remove()

    board = generate_next_board(board)
    generate_seaborn_scatter_from_board(board)


def generate_next_board(current_board):
    # Generate the next board using the current one
    dimensions = current_board.shape
    next_board = np.zeros(dimensions)
    # Get the neighbour count for each point and determine its state
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            # The neighbour count is initialised at -1 if the cell is alive
            # because it will end up counting itself later on
            neighbours = 0 - current_board[i, j]
            # Check a 3x3 matrix centered on the current point for neighbours
            for x in range(max(0, i - 1), i + 2):
                for y in range(max(0, j - 1), j + 2):
                    try:
                        if current_board[x, y]:
                            neighbours += 1
                    except IndexError:
                        continue
            if current_board[i, j]:  # Cell is alive
                if 2 <= neighbours <= 3:  # Does it have between 2 and 3
                    next_board[i, j] = 1  # neighbours (both inclusive)
            else:  # Cell is dead
                if neighbours == 3:  # Does it have exactly 3 neighbours
                    next_board[i, j] = 1

    return next_board


def generate_seaborn_scatter_from_board(board):
    coordinates = np.nonzero(board)
    df = pd.DataFrame({'x_coord': coordinates[0], 'y_coord': coordinates[1]})

    sns.scatterplot(x='x_coord', y='y_coord', data=df, color='white',
                    marker='s', s=(60 * scale_factor)**2)


def generate_random_board(dimensions, probability):
    random_board = np.zeros(dimensions)
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            random_board[i, j] = np.random.choice([0, 1], p=[1 - probability,
                                                             probability])

    return random_board


if __name__ == '__main__':
    arguments = docopt(__doc__.split('-' * 72)[0])
    main(arguments['--refresh-speed'], arguments['--size'], arguments[
        '--probability'])

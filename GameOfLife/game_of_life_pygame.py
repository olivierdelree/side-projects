"""
This is a simple simulation of Conway's Game of Life using numpy and
Pygame.

Usage:
    game_of_life_pygame.py [options]

Options:
    -h, --help      Shows this help screen.
    -t <speed>, --tick-rate <speed>
                    Sets the tick-rate of the plot in ticks/second.
                    [default: 100]
    -s <size>, --board-size <size>
                    Size of the board to use. The height and width will
                    both use the same value. [default: 100]
    -p <probability>, --probability <probability>
                    The probability of any cell being live when
                    generating the board. [default: 0.15]

------------------------------------------------------------------------

Created 01/01/2022 at 12:52 GMT
"""

import sys
import time

from docopt import docopt
import pygame
import numpy as np


BACKGROUND_COLOUR = (0, 0, 0)
CELL_COLOUR = (255, 255, 255)
GRID_COLOUR = (185, 185, 185)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
WINDOW = pygame.display.set_mode((WINDOW_WIDTH + 1, WINDOW_HEIGHT + 1))


def main(arguments):
    interval = int(arguments['--tick-rate'])
    board_size = (int(arguments['--board-size']),
                  int(arguments['--board-size']))
    probability = float(arguments['--probability'])

    # Initialising the first default state
    pygame.init()
    WINDOW.fill(BACKGROUND_COLOUR)
    board = generate_random_board(board_size, probability)

    # Starting the main loop which draws the game every tick
    for i in range(0, 100):
        draw_board(board)

        # Checks if the user has requested to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        board = generate_next_board(board)
        # pygame.time.delay(int(1000 / interval))


def generate_random_board(grid_size, probability):
    random_board = np.zeros(grid_size)
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            random_board[i, j] = np.random.choice([0, 1], p=[1 - probability,
                                                             probability])
    return random_board


def generate_next_board(board):
    grid_size = board.shape
    next_board = np.zeros(grid_size)

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            # Avoids a live cell counting itself
            neighbours = 0 - board[i, j]

            # Counts neighbours in a 3x3 grid centered around the current cell
            for x in range(max(0, i - 1), i + 2):
                for y in range(max(0, j - 1), j + 2):
                    try:
                        if board[x, y]:
                            neighbours += 1
                    except IndexError:
                        continue
            # Decides the future state of the cell based on its neighbour count
            if board[i, j]:
                if 2 <= neighbours <= 3:
                    next_board[i, j] = 1
            else:
                if neighbours == 3:
                    next_board[i, j] = 1

    return next_board


def draw_board(board):
    grid_size = board.shape
    block_size = WINDOW_HEIGHT / grid_size[0]

    # Draws the cells first
    for x in range(0, grid_size[0]):
        for y in range(0, grid_size[1]):
            rect = pygame.Rect(x * block_size, y * block_size, block_size,
                               block_size)
            if board[x, y]:
                pygame.draw.rect(WINDOW, GRID_COLOUR, rect)
            else:
                pygame.draw.rect(WINDOW, BACKGROUND_COLOUR, rect)

    # Draws a grid second
    for x in range(0, grid_size[0] + 1):
        pygame.draw.line(WINDOW, CELL_COLOUR,
                         (grid_size[1] * block_size, x * block_size),
                         (0, x * block_size), 1)
    for y in range(0, grid_size[1] + 1):
        pygame.draw.line(WINDOW, CELL_COLOUR, (y * block_size, 0),
                         (y * block_size, grid_size[0] * block_size), 1)


if __name__ == '__main__':
    start_time = time.time()
    arguments = docopt(__doc__.split('-' * 72)[0])
    main(arguments)
    execution_time = (time.time() - start_time)
    print('Execution time: ' + str(execution_time))

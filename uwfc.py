from collections import namedtuple
import argparse
import random
import numpy as np
import tqdm


def print_board(board):
    print('\n'.join(''.join(el.tile or '*' for el in row) for row in board), end='\n\n')

def print_entropies(board):
    print('\n'.join(''.join(str(el.entropy) for el in row) for row in board), end='\n\n')

def find_lowest_entropies(board):
    entropies = np.vectorize(lambda t: t.entropy)(board)
    indices = np.where(entropies == entropies.min())
    return list(zip(*indices))

def update_entropies(board, tiles):
    w, h = board.shape
    for i in range(w):
        for j in range(h):
            tile: Tile = board[i, j]
            for poss in tile.possibilities.values():
                poss.clear()
            if not tile.tile:
                if i > 0:
                    up: Tile = board[i-1, j]
                    if up.tile:
                        for tl in tiles:
                            if tl.sides.up == up.sides.down:
                                tile.possibilities['up'].add(tl)
                    else:
                        tile.possibilities['up'].update(tiles)
                try:
                    right: Tile = board[i, j+1]
                    if right.tile:
                        for tl in tiles:
                            if tl.sides.right == right.sides.left:
                                tile.possibilities['right'].add(tl)
                    else:
                        tile.possibilities['right'].update(tiles)
                except:
                    ...
                try:
                    down: Tile = board[i+1, j]
                    if down.tile:
                        for tl in tiles:
                            if tl.sides.down == down.sides.up:
                                tile.possibilities['down'].add(tl)
                    else:
                        tile.possibilities['down'].update(tiles)
                except:
                    ...
                if j > 0:
                    left: Tile = board[i, j-1]
                    if left.tile:
                        for tl in tiles:
                            if tl.sides.left == left.sides.right:
                                tile.possibilities['left'].add(tl)
                    else:
                        tile.possibilities['left'].update(tiles)
            else:
                tile.entropy = 9
            
            tile.update_entropy()

Sides = namedtuple('Side', ('up', 'right', 'down', 'left'))

class Tile:
    def __init__(self, tile=None, sides: Sides=None):
        self.tile = tile
        self.sides = sides
        self.entropy = 5
        self.possibilities = {
            'up': set(),
            'right': set(),
            'down': set(),
            'left': set()
        }
        self.allowed = []

    def update_entropy(self):
        values = [val for val in self.possibilities.values() if val]
        self.allowed = values[0].intersection(*values) if values else []
        self.entropy = len(self.allowed) if values else 9

tiles = [
    Tile(' ', Sides(0, 0, 0, 0)),
    Tile('╠', Sides(1, 1, 1, 0)),
    Tile('╦', Sides(0, 1, 1, 1)),
    Tile('╣', Sides(1, 0, 1, 1)),
    Tile('╩', Sides(1, 1, 0, 1)),
    Tile('╔', Sides(0, 1, 1, 0)),
    Tile('╗', Sides(0, 0, 1, 1)),
    Tile('╚', Sides(1, 1, 0, 0)),
    Tile('╝', Sides(1, 0, 0, 1)),
    Tile('╬', Sides(1, 1, 1, 1)),
    Tile('║', Sides(1, 0, 1, 0)),
    Tile('═', Sides(0, 1, 0, 1))
]

def main(width, height, n_iter):
    for _ in range(n_iter):
        shape = height, width
        board = np.ndarray(shape, Tile)

        for i in range(shape[0]):
            for j in range(shape[1]):
                board[i, j] = Tile()

        for i in tqdm.tqdm(range(shape[0] * shape[1])):
            update_entropies(board, tiles)
            lowest_entropy_idx = random.choice(find_lowest_entropies(board))
            board[lowest_entropy_idx] = random.choice(tuple(board[lowest_entropy_idx].allowed))

        update_entropies(board, tiles)
        print_board(board)


parser = argparse.ArgumentParser(description='Create pattern with wave function collapse.')
parser.add_argument('--width', default=10, type=int, help='width of generated pattern')
parser.add_argument('--height', default=10, type=int, help='height of generated pattern')
parser.add_argument('--n-iter', default=1, type=int, help='how many patterns generates')

args = parser.parse_args()
main(**vars(args))
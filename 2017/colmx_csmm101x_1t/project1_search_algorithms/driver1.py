

import sys
import math

class Directions:
    UP = 'Up'
    DOWN = 'Down'
    LEFT = 'Left'
    RIGHT = 'Right'

def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True


class Board():
    '''
    Board that represent the tiles that can be moved along for
    the game play
    '''

    def __init__(self, tile_list):

        self.board_tile_xy_ = {}
        self.board_xy_tile_ = {}
        self.n_ = int(math.sqrt(len(tile_list)))

        if is_square(self.n_):
            print("Invalid game tiles length")
            return

        if tile_list.count(0) > 1:
            print("Invalid game setup, too many zero tiles")
            return

        row = 0
        col = 0
        for tile in tile_list:
            self.board_tile_xy_[tile] = (row,col)
            self.board_xy_tile_[(row,col)] = tile

            col = col + 1
            if(col % self.n_ == 0):
                col = 0
                row = row + 1

    # returns the possible moves for a tile, which means
    # directions that can be used to put the current tile in a
    # 0 position
    def next_moves(self, tile):
        row,col = self.board_tile_xy_[tile]
        moves = []

        if col+1 < self.n_ and self.board_xy_tile_[row,col+1] == 0:
            moves.append(Directions.RIGHT)

        elif col-1 >= 0 and self.board_xy_tile_[row,col-1] == 0:
            moves.append(Directions.LEFT)

        elif row+1 < self.n_ and self.board_xy_tile_[row+1,col] == 0:
            moves.append(Directions.DOWN)

        elif row-1 >= 0 and self.board_xy_tile_[row-1,col] == 0:
            moves.append(Directions.UP)

        return moves

    # on the board the tiles that can be moved to an empty spot
    # which is a 0 tile
    def movable_tiles(self):
        row,col = self.board_tile_xy_[0]
        tiles = []

        if col+1 < self.n_:
            tiles.append(self.board_xy_tile_[row,col+1])

        if col-1 >= 0:
            tiles.append(self.board_xy_tile_[row,col-1])

        if row+1 < self.n_:
            tiles.append(self.board_xy_tile_[row+1,col])

        if row-1 >= 0:
            tiles.append(self.board_xy_tile_[row-1,col])

        return tiles

    def print_(self):
        print("Board start --------")
        print("size:",self.n_)
        for row in range(self.n_):
            col_string = "\t".join([str(self.board_xy_tile_[row,col]) for col in range(self.n_)])
            print(col_string)
        print("movable_tiles",self.movable_tiles())
        print("Board end --------")

    # this method is used to move a tile by performing a valid
    # action provided
    def move_tile(self, tile, direction):

        # 0 is the empty space we dont move that
        # we move only non zero tiles
        if tile == 0:
            return

        (row, col) = self.board_tile_xy_[tile]
        next_moves = self.next_moves(tile)
        if not next_moves:
            return

        if direction == Directions.UP and direction in next_moves and row-1 >= 0:
            self.board_tile_xy_[tile] = (row-1,col)
            self.board_tile_xy_[0] = (row,col)
            self.board_xy_tile_[(row-1,col)] = tile
            self.board_xy_tile_[(row,col)] = 0

        elif direction == Directions.DOWN and direction in next_moves and row+1 >= 0:
            self.board_tile_xy_[tile] = (row+1,col)
            self.board_tile_xy_[0] = (row,col)
            self.board_xy_tile_[(row+1,col)] = tile
            self.board_xy_tile_[(row,col)] = 0

        elif direction == Directions.RIGHT and direction in next_moves and col+1 >= 0:
            self.board_tile_xy_[tile] = (row,col+1)
            self.board_tile_xy_[0] = (row,col)
            self.board_xy_tile_[(row,col+1)] = tile
            self.board_xy_tile_[(row,col)] = 0

        elif direction == Directions.LEFT and direction in next_moves and col-1 >= 0:
            self.board_tile_xy_[tile] = (row,col-1)
            self.board_tile_xy_[0] = (row,col)
            self.board_xy_tile_[(row,col-1)] = tile
            self.board_xy_tile_[(row,col)] = 0


def main_search():
    _,search_algo, tile_string = sys.argv
    board = Board([int(tile) for tile in tile_string.strip().split(',')])

    # test code
    board.print_()
    board.move_tile(3,Directions.UP)
    board.move_tile(5,Directions.UP)
    board.move_tile(5,Directions.RIGHT)
    board.move_tile(5,Directions.LEFT)
    board.print_()

if __name__ == "__main__":
    main_search()


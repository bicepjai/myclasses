

import sys
import math
import copy
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

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

    def __init__(self, tile_list = None):

        self.n_ = len(tile_list)
        if not is_square(self.n_) or self.n_ == 1:
            print("Invalid game tiles length ", self.n_)
            return

        self.rc_ = int(math.sqrt(self.n_))
        self.zero_tile_ = None

        if tile_list.count(0) > 1:
            print("Invalid game setup, too many zero tiles")
            return

        if tile_list != None:
            self.board_ = tile_list
            self.zero_tile_ = tile_list.index(0)
        else:
            self.board_ = [tile for tile in range(self.n_)]
            self.zero_tile_ = 0

        self.hashed_tuple = tuple(self.board_)

    def get_possible_moves(self):
        '''
        returns list of tuples that contains (Direction,New Board Config)
        '''
        new_boards = []
        for direction in Direction:
            board = None

            if(direction == Direction.UP and self.zero_tile_ - self.rc_ > 0):
                    board = self.board_[:]
                    board[self.zero_tile_] = board[self.zero_tile_ - self.rc_]
                    board[self.zero_tile_ - self.rc_] = 0
            elif(direction == Direction.DOWN and self.zero_tile_ + self.rc_ < self.n_):
                    board = self.board_[:]
                    board[self.zero_tile_] = board[self.zero_tile_ + self.rc_]
                    board[self.zero_tile_ + self.rc_] = 0

            elif(direction == Direction.LEFT and self.zero_tile_ % self.rc_ != 0 ):
                    board = self.board_[:]
                    board[self.zero_tile_] = board[self.zero_tile_ - 1]
                    board[self.zero_tile_ - 1] = 0

            elif(direction == Direction.RIGHT and self.zero_tile_ % self.rc_ != self.rc_ - 1 ):
                    board = self.board_[:]
                    board[self.zero_tile_] = board[self.zero_tile_ + 1]
                    board[self.zero_tile_ + 1] = 0

            if(board):
                new_boards.append((direction,board))

        return new_boards

    def __eq__(self, other):
        '''
        Compare 2 boards with equal sign
        '''
        return all(e1 == e2 for e1, e2 in zip(other.board_, self.board_))

    def __str__(self):
        '''
        print Board details for debug
        '''
        return ','.join(map(str,self.board_)) + " -----------------\n" + "\n".join(map(str,self.get_possible_moves())) + "\n"

    def __hash__(self):
        return hash(self.hashed_tuple)

class Node:
    '''
    while preforming search to encapsulate some more properties along with the board
    we use Node which can be used in the search algorithms
    '''
    def __init__(self, board, action = None):
        self.board_ = board
        self.action_ = action
        self.hashed_tuple = (board,action)

    def get_neighbors(self):
        '''
        gather and form new neighboring nodes so that, these new Nodes
        can be used to branch
        '''
        neighbors = []
        for (action, new_board) in self.board_.get_possible_moves():
            neighbors.append(Node(Board(new_board), action))
        return neighbors

    def __eq__(self, other):
        '''
        Compare 2 Nodes with equal sign
        '''
        return other.board_ == self.board_

    def __str__(self):
        return str(self.action_) + " => " + str(self.board_)

    def __hash__(self):
        return hash(self.hashed_tuple)

class Search:
    '''
    search class can be initialized with 4 types of search algorithms
        bfs (Breadth-First Search)
        dfs (Depth-First Search)
        ast (A-Star Search)
        ida (IDA-Star Search)

        takes in 2 arguments that are Node Objects which are root and goal Nodes
    '''

    def __init__(self, root, goal, algo_str = None):

        self.supported_algos_ = ["dfs","bfs","ast","ida"]

        if not algo_str:
            self.search_algo_ = "dfs"
        else:
            self.search_algo_ = algo_str.lower()
            if algo_str.lower() not in self.supported_algos_:
                raise ValueError('Unsupported search algorithm, use one of ' + str(self.supported_algos_))

        self.root_ = root
        self.goal_ = goal

        # project evaluation requirements
        self.path_to_goal_       = None
        self.cost_of_path_       = None
        self.nodes_expanded_     = None
        self.fringe_size_        = None
        self.max_fringe_size_    = None
        self.search_depth_       = None
        self.max_search_depth_   = None
        self.running_time_       = None
        self.max_ram_usage_      = None

    def dfs(self):
        '''
        depth first search algorithm
        '''
        frontier = [copy.deepcopy(self.root_)]
        explored = set()
        while frontier:

            print("frontier =======",len(frontier))
            # print("\n".join(map(str,frontier)))
            node = frontier.pop(0)
            explored.add(node)
            print("\n current_node:\n" + str(node))
            print("=============")

            if node == self.goal_:

                print("goal state reached")
                return True

            for neighbor in node.get_neighbors():
                if neighbor not in explored:
                    frontier.append(neighbor)

    def results(self):
        '''
            path_to_goal: the sequence of moves taken to reach the goal
            cost_of_path: the number of moves taken to reach the goal
            nodes_expanded: the number of nodes that have been expanded
            fringe_size: the size of the frontier set when the goal node is found
            max_fringe_size: the maximum size of the frontier set in the lifetime of the algorithm
            search_depth: the depth within the search tree when the goal node is found
            max_search_depth:  the maximum depth of the search tree in the lifetime of the algorithm
            running_time: the total running time of the search instance, reported in seconds
            max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes
        '''
        print("\n")
        print("path_to_goal: {}".     format(self.path_to_goal_))
        print("cost_of_path: {}".     format(self.cost_of_path_))
        print("nodes_expanded: {}".   format(self.nodes_expanded_))
        print("fringe_size: {}".      format(self.fringe_size_))
        print("max_fringe_size: {}".  format(self.max_fringe_size_))
        print("search_depth: {}".     format(self.search_depth_))
        print("max_search_depth: {}". format(self.max_search_depth_))
        print("running_time: {}".     format(self.running_time_))
        print("max_ram_usage: {}".    format(self.max_ram_usage_))
        print("\n")

def main():
    _,search_algo, tile_string = sys.argv

    start_tile_config = [int(tile) for tile in tile_string.strip().split(',')]
    goal_tile_config  = [tile for tile in range(len(start_tile_config))]
    root = Node(Board(start_tile_config))
    goal = Node(Board(goal_tile_config))

    print("Root: " + str(root))
    print("Goal: " + str(goal))

    search = Search(root, goal, search_algo)
    search.dfs()
    search.results()


if __name__ == "__main__":
    main()


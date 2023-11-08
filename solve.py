"""The main script to solve the problem"""
# PYTHONHASHSEED=0
# import sys


import numpy as np
import psutil

import datamanager
from chessboard import Board

# sys.setrecursionlimit(sys.getrecursionlimit()+1500)

# The Terms and Variables Definition use in the code
#
# boards:
#   Recode the relation of symmetry board positions
#
#   {
#       representative_board_hash: None,
#       symmetry_board_hash: representative_board_hash
#       , ...
#   }
#
#   The value is 'None,' representing that it is representative of all
#   symmetry board positions
#
#
# board_state:
#   Record all board position (only representative board) that have been occur.
#   key: hash of the board position
#   value:
#       True: O win
#       False: O lose
#       None: Not finish the tree yet
#


boards_o = {}
board_state_o = {}
boards_x = {}
board_state_x = {}


class Status:
    def __init__(self) -> None:
        self.n = 0

    def print_now(self, board):
        if len(board_state_o) // 1000 > self.n:
            self.n += 1
            print(len(board_state_o), len(board_state_o))
            self.check_memory_use(board)

    def check_memory_use(self, board):
        if psutil.virtual_memory()[2] >= 95:
            datamanager.save(
                board, boards_o, board_state_o, boards_x, board_state_x, False
            )
            print("The system ran out of memory")
            exit(1)


status = Status()


def o_turns(board: Board):
    status.print_now(board)

    next_chess = board.available_move(1)
    results = []
    boards_next = []  # the movement that not win or tie
    for movement in next_chess:
        if movement[0] == 0:
            board_next = board.copy()
            board_next.put(movement[1], 1)
        else:
            board_next = board.copy()
            board_next.move(*movement[1], 1)
        if have_similar(board_next, boards_o):
            state = find_state(board_next, boards_o, board_state_o)
            results.append(state)
            if state:
                return any(results)
            continue
        else:
            win_status = board_next.check_win()
            if win_status == 1:
                ha = similar(board_next, boards_o)
                board_state_o[ha] = True
                results.append(True)
                return any(results)
            elif win_status in (3, 2):
                ha = similar(board_next, boards_o)
                board_state_o[ha] = False
                results.append(False)
            else:
                boards_next.append(board_next)
    for board_next in boards_next:
        if have_similar(board_next, boards_o):
            state = find_state(board_next, boards_o, board_state_o)
            results.append(state)
            if state:
                return any(results)
            continue
        else:
            ha = similar(board_next, boards_o)
            board_state_o[ha] = None
            r = x_turns(board_next)
            results.append(r)
            board_state_o[ha] = r

    return any(results)


def x_turns(board: Board):
    next_chess = board.available_move(2)
    results = []
    boards_next = []  # the movement that not win or tie
    for movement in next_chess:
        if movement[0] == 0:
            board_next = board.copy()
            board_next.put(movement[1], 2)
        else:
            board_next = board.copy()
            board_next.move(*movement[1], 2)
        if have_similar(board_next, boards_x):
            state = find_state(board_next, boards_x, board_state_x)
            results.append(state)
            if not state:
                return all(results)
            continue
        else:
            win_status = board_next.check_win()
            if win_status in (3, 2):
                ha = similar(board_next, boards_x)
                board_state_x[ha] = False
                results.append(False)
                return all(results)
            elif win_status == 1:
                ha = similar(board_next, boards_x)
                board_state_x[ha] = True
                results.append(True)
            else:
                boards_next.append(board_next)
    for board_next in boards_next:
        if have_similar(board_next, boards_x):
            state = find_state(board_next, boards_x, board_state_x)
            results.append(state)
            if not state:
                return all(results)
            continue
        else:
            ha = similar(board_next, boards_x)
            board_state_x[ha] = None
            r = o_turns(board_next)
            results.append(r)
            board_state_x[ha] = r
    return all(results)


def similar(board: Board, boards) -> int:
    """Find all symmetry chess position and update the relation to `boards`

    Returns
    -------
    int
        hash of input board
    """
    b = board.board.copy()
    hashs = []
    for i in range(4):
        br = np.rot90(b, i, axes=(1, 2))
        hashs.append(hash(br.tobytes()))
        hashs.append(hash(np.flip(br, 1).tobytes()))
    boards.update({hashs[0]: None})
    for h in set(hashs) - {hashs[0]}:
        boards.update({h: hashs[0]})
    return hashs[0]


def have_similar(board: Board, boards) -> bool:
    """Check if the board was record in the `boards`"""
    return hash(board.board.tobytes()) in boards


def find_state(board: Board, boards, board_state):
    """Find the recoded state of the board

    Returns
    -------
    bool or None
    """
    board_hash = hash(board.board.tobytes())
    while True:
        if boards[board_hash] is None:
            break
        board_hash = boards[board_hash]
    return board_state[board_hash]


if __name__ == "__main__":
    board = Board()
    # board.put(0, 1)
    # board.put(3, 2)
    # board.put(4, 2)
    # board.put(6, 1)
    # board.show()
    # print(hash(board.board.tobytes()))

    result = o_turns(board)
    # result = x_turns(board)
    print("O will win:", result)
    print("finished!")
    datamanager.save(board, boards_o, board_state_o,
                     boards_x, board_state_x, True)

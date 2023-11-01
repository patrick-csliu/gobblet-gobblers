"""The main script to solve the problem"""

# import sys

import numpy as np

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


boards = {}
board_state = {}


def print_board_n():
    if len(board_state)//100 > print_board_n.n:
        print_board_n.n += 1
        print(len(board_state))


print_board_n.n = 0


def o_turns(board: Board):
    print_board_n()
    next_chess = board.available_move(1)
    results = []
    for movement in next_chess:
        if movement[0] == 0:
            board_next = board.copy()
            board_next.put(movement[1], 1)
        else:
            board_next = board.copy()
            board_next.move(*movement[1], 1)
        if have_similar(board_next):
            results.append(find_state(board_next))
            continue
        else:
            ha = similar(board_next)
            win_status = board_next.check_win()
            if win_status == 1:
                board_state[ha] = True
                results.append(True)
                break
            elif win_status in (3, 2):
                board_state[ha] = False
                results.append(False)
            else:
                board_state[ha] = None
                r = x_turns(board_next)
                results.append(r)
                board_state[ha] = r
    return any(results)


def x_turns(board: Board):
    next_chess = board.available_move(2)
    results = []
    for movement in next_chess:
        if movement[0] == 0:
            board_next = board.copy()
            board_next.put(movement[1], 2)
        else:
            board_next = board.copy()
            board_next.move(*movement[1], 2)
        if have_similar(board_next):
            results.append(find_state(board_next))
            continue
        else:
            ha = similar(board_next)
            win_status = board_next.check_win()
            if win_status == 2:
                board_state[ha] = False
                results.append(False)
                break
            elif win_status in (3, 1):
                board_state[ha] = True
                results.append(True)
            else:
                board_state[ha] = None
                r = o_turns(board_next)
                results.append(r)
                board_state[ha] = r
    return all(results)


def similar(board: Board) -> int:
    """Find all symmetry chess position and update the relation to `boards` 

    Returns
    -------
    int
        hash of input board
    """
    b = board.board.copy()
    hashs = []
    for i in range(4):
        br = np.rot90(b, i)
        hashs.append(hash(br.tobytes()))
        hashs.append(hash(np.flip(br, 1).tobytes()))
    boards.update({hashs[0]: None})
    for h in set(hashs[1:]):
        boards.update({hashs[i]: hashs[0]})
    return hashs[0]


def have_similar(board: Board) -> bool:
    """Check if the board was record in the `boards`
    """
    return hash(board.board.tobytes()) in boards


def find_state(board: Board):
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
    result = o_turns(board)
    print("O will win:", result)
    print("finished!")
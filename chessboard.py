"""A checss board class for Gobblet Gobblers

Provide operations for the game
"""

from __future__ import annotations

import time

import numpy as np
from IPython.display import clear_output

#
# [Position]
# Layer 1     Layer 2     Layer 3
# (Large)     (Medium)    (Small)
# 0 | 1 | 2   9 | 10| 11  18| 19| 20
# ---------   ---------   ---------
# 3 | 4 | 5   12| 13| 14  21| 22| 23
# ---------   ---------   ---------
# 6 | 7 | 8   15| 16| 17  24| 25| 26
#
#
# [Player]
# Player 1 : O
# Player 2 : X
#

winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]              # Diagonals
]


class Board:
    """Chess board

    board:
        array[layer, row, column]

    """

    def __init__(self, board: np.ndarray | Board = None, history=[]):
        if board is None:
            self.board = np.zeros((3, 3, 3), dtype=np.int8)
        elif isinstance(board, Board):
            self.board = board.board.copy()
        else:
            self.board = board
        self.history = history
        self.chess = self.chess_left()  # the unused chess

    def __getitem__(self, key):
        return self.board[key]

    def __repr__(self):
        return self._show_top_size()

    def _show_top(self) -> str:
        board_str = [[' ', ' ', ' '] for i in range(3)]
        for row in range(3):
            for col in range(3):
                for i in range(3):
                    if self.board[i][row][col] == 1:
                        board_str[row][col] = 'O'
                        break
                    elif self.board[i][row][col] == 2:
                        board_str[row][col] = 'X'
                        break
                    else:
                        pass
        line = '-' * 9
        board_lines = [" | ".join(row) for row in board_str]
        board_lines.insert(2, line)
        board_lines.insert(1, line)
        return "\n" + "\n".join(board_lines)

    def _show_layer(self) -> str:
        def layer(i):
            board_str = [[' ', ' ', ' '] for i in range(3)]
            for row in range(3):
                for col in range(3):
                    if self.board[i][row][col] == 1:
                        board_str[row][col] = 'O'
                    elif self.board[i][row][col] == 2:
                        board_str[row][col] = 'X'
                    else:
                        pass
            line = '-' * 9
            board_lines = [" | ".join(row) for row in board_str]
            board_lines.insert(2, line)
            board_lines.insert(1, line)
            return "\n" + "\n".join(board_lines)

        s = ""
        for i in range(3):
            s += layer(i) + '\n' + '+'*9
        return s

    def _show_top_size(self) -> str:
        size = ['₃', '₂', '₁']
        board_str = [['  ', '  ', '  '] for i in range(3)]
        for row in range(3):
            for col in range(3):
                for i in range(3):
                    if self.board[i][row][col] == 1:
                        board_str[row][col] = 'O' + size[i]
                        break
                    elif self.board[i][row][col] == 2:
                        board_str[row][col] = 'X' + size[i]
                        break
                    else:
                        pass
        line = '-' * 12
        board_lines = [" | ".join(row) for row in board_str]
        board_lines.insert(2, line)
        board_lines.insert(1, line)
        return "\n" + "\n".join(board_lines)

    def show(self, t='ts'):
        """Display the status of the game

        Parameters
        ----------
        t : str, optional
            type, available:
                't': top,
                'ts': top and size,
                'l': layer
            by default 'ts'
        """
        if t == 'ts':
            print(self._show_top_size())
        elif t == 't':
            print(self._show_top())
        elif t == 'l':
            print(self._show_layer())
        else:
            raise Exception('Invalid value for parameter "t". Supported values '
                            'are: "t" (top), "ts" (top and size), and "l" (layer).')

    def copy(self) -> Board:
        """Return Board copy"""
        return Board(np.copy(self.board), history=self.history.copy())

    def pos2ind(self, pos: int) -> tuple:
        """Convert position to index of board
        """
        return pos//9, pos//3 % 3, pos % 3

    def ind2pos(self, ind):
        """Convert index of board to position
        """
        return ind[0]*9 + ind[1]*3 + ind[2]

    def chess_left(self) -> np.ndarray:
        """Count the left chess and raise error if input invalid

        Returns
        -------
        np.ndarray
            left chess array:
            [
                [first_layer, second_layer, third_layer], # player 1
                [first_layer, second_layer, third_layer], # player 2
            ]

        """
        if (np.count_nonzero(self.board > 2) or
                np.count_nonzero(self.board < 0)):
            raise Exception("Invalid board")
        chess = np.array([[2, 2, 2], [2, 2, 2]], dtype=np.int8)
        for i in range(3):
            for player in range(1, 3):
                n = np.count_nonzero(self.board[i] == player)
                if n > 2:
                    raise Exception("Exceeding the limit of two chess pieces"
                                    " for a player.")
                chess[player-1][i] -= n
        return chess

    def is_legal_put(self, pos: int, player: int) -> bool:
        """Check if the position is valid for the player to perform a 'put' action

        Returns
        -------
        bool
            True: Valid
            False: Invalid
        """
        ind = self.pos2ind(pos)
        if np.cumsum(self.board[:, ind[1], ind[2]], 0, dtype=bool)[ind[0]]:
            print("A chess piece already occupies this position or the chess "
                  "is not bigger than the existing chess. Cannot place here.")
            return False
        if self.chess[player-1][pos//9] == 0:
            print("Exceeding the limit of two chess pieces for a player. "
                  "No more chess pieces available for this player.")
            return False
        return True

    def is_legal_move(self, pre_pos: int, pos: int, player: int) -> bool:
        """Check if the position is valid for the player to perform a 'move' action

        Parameters
        ----------
        pre_pos : int
            selected position
        pos : int
            destination position
        player : int

        Returns
        -------
        bool
            True: Valid
            False: Invalid
        """
        if pre_pos == pos:
            print("pre_pos cannot be equal to pos.")
            return False
        pre_ind = self.pos2ind(pre_pos)
        ind = self.pos2ind(pos)
        if pre_ind[0] != ind[0]:
            print("The layers must be the same.")
            return False
        if self.board[pre_ind] != player:
            print("There is no chess here, or it's not your chess.")
            return False
        for i in range(pre_ind[0]):  # Can use np.cumsum
            if self.board[i][pre_ind[1]][pre_ind[2]] > 0:
                print("There is a chess piece on top of the selected chess piece.")
                return False

        for i in range(ind[0]+1):  # Can use np.cumsum
            if self.board[i][ind[1]][ind[2]] > 0:
                print("The selected chess piece is not bigger than the "
                      "destination chess piece.")
                return False
        return True

    def put(self, pos: int, player: int):
        """Put action

        Parameters
        ----------
        pos : int
            destination position
        player : int
        """
        if self.is_legal_put(pos, player):
            self.board[self.pos2ind(pos)] = player
            self.chess[player-1][pos//9] -= 1
            self.history.append((30, pos))

    def move(self, pre_pos: int, pos: int, player: int):
        """Move action

        Parameters
        ----------
        pre_pos : int
            selected position
        pos : int
            destination position
        player : int
        """
        if self.is_legal_move(pre_pos, pos, player):
            self.board[self.pos2ind(pos)] = player
            self.board[self.pos2ind(pre_pos)] = 0
            self.history.append((pre_pos, pos))

    def check_win(self) -> int:
        """Return the state of chess

        Returns
        -------
        int
            0: no one win and tie
            1: player 1 win
            2: player 2 win
            3: tie
        """
        top = np.zeros((3, 3), dtype=np.int8)
        for row in range(3):
            for col in range(3):
                for i in range(3):
                    if self.board[i][row][col] == 1:
                        top[row][col] = 1
                        break
                    elif self.board[i][row][col] == 2:
                        top[row][col] = 2
                        break
                    else:
                        pass

        def player_win(player):
            for combo in winning_combinations:
                if all(top[i//3][i % 3] == player for i in combo):
                    return True
            return False
        p1_is_win = player_win(1)
        p2_is_win = player_win(2)
        if p1_is_win and p2_is_win:
            return 3
        elif p1_is_win:
            return 1
        elif p2_is_win:
            return 2
        else:
            return 0

    def available_move(self, player: int) -> list:
        """Return all available move for the player

        Parameters
        ----------
        player : int

        Returns
        -------
        list
            Two type of tuple:
            1. put action:
                (0, position)
            2. move action
                (1, (selected_position, destination_position))
        """
        available = []
        chess_valid = ~np.cumsum(self.board.astype(bool), 0, dtype=bool)
        # unused chess to each available position
        for i in range(3):
            if self.chess[player-1][i] == 0:
                continue
            for row in range(3):
                for col in range(3):
                    if chess_valid[i][row][col]:
                        available.append((0, self.ind2pos((i, row, col))))
        # move chess
        top = np.full((3, 3), 3, dtype=np.int8)
        for row in range(3):
            for col in range(3):
                for i in range(3):
                    if self.board[i][row][col] == player:
                        top[row][col] = i
                        break
                    if self.board[i][row][col] > 0:
                        break
        # top = np.full((3, 3), 3, dtype=np.int8)
        # for layer in range(2, -1, -1):
        #     top[self.board[layer]>0] = 3
        #     top[self.board[layer]==player] = layer
        for row in range(3):
            for col in range(3):
                layer = top[row][col]
                if layer == 3:
                    continue
                for row2 in range(3):
                    for col2 in range(3):
                        if (chess_valid[layer][row2][col2] and
                                (not row == row2 or not col == col2)):
                            available.append(
                                (
                                    1,
                                    (self.ind2pos((layer, row, col)),
                                     self.ind2pos((layer, row2, col2)))
                                )
                            )
        return available


class BoardHistory:
    def __init__(self, board: Board):
        self.board = board
        self.history_len = len(board.history)

    def goto(self, n: int):
        if n < self.history_len:
            pass
        else:
            return None
        board = Board()
        player = 1
        for movement in self.board.history[:n+1]:
            if movement[0] == 30:
                board.put(movement[1], player)
            else:
                board.move(*movement, player)
            player = -player + 3
        return board

    def show(self, n: int):
        self.goto(n).show()

    def play(self, n: int = 0):
        board = self.goto(n)
        while True:
            # clear_output(wait=False)
            # time.sleep(0.1)
            print('n =', n)
            print(board.history[-1])
            print('next:', (n+1) % 2 + 1)
            print('left:', board.chess)
            board.show()
            _input = input()
            n += 1
            if n > self.history_len - 1:
                break
            elif _input == 'q':
                break
            else:
                movement = self.board.history[n]
                player = n % 2 + 1
                if movement[0] == 30:
                    board.put(movement[1], player)
                else:
                    board.move(*movement, player)


if __name__ == "__main__":
    # test_board = np.array([
    #     [
    #         [1, 2, 2],
    #         [0, 1, 0],
    #         [0, 0, 0],
    #     ],
    #     [
    #         [0, 0, 0],
    #         [1, 0, 0],
    #         [2, 0, 0],
    #     ],
    #     [
    #         [2, 0, 0],
    #         [0, 0, 1],
    #         [2, 0, 0],
    #     ],
    # ])
    # test_board = np.array([
    #     [
    #         [0, 2, 2],
    #         [0, 1, 0],
    #         [0, 0, 0],
    #     ],
    #     [
    #         [0, 0, 0],
    #         [1, 0, 0],
    #         [2, 0, 0],
    #     ],
    #     [
    #         [2, 0, 0],
    #         [0, 0, 1],
    #         [2, 0, 0],
    #     ],
    # ])
    test_board = np.array([
        [
            [1, 2, 2],
            [0, 1, 0],
            [0, 0, 0],
        ],
        [
            [0, 0, 0],
            [0, 0, 0],
            [2, 0, 0],
        ],
        [
            [2, 0, 0],
            [0, 0, 1],
            [2, 0, 0],
        ],
    ])
    board = Board(test_board)
    board.show()
    board.show('l')
    board.show('t')
    print("chess left:\n", board.chess)
    print('='*20)

    board.is_legal_put(8, 1)
    board.is_legal_put(25, 1)
    board.is_legal_put(13, 2)
    print('='*20)

    print('Win:', board.check_win())
    board.put(16, 1)
    board.show()
    for i in board.available_move(2):
        print(i)
    board.is_legal_move(2, 2, 2)
    board.is_legal_move(2, 0, 2)
    board.is_legal_move(2, 16, 2)
    board.is_legal_move(16, 17, 2)
    board.is_legal_move(18, 19, 2)

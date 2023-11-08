import pickle
from datetime import datetime
from pathlib import Path


def save(board_now, boards_o, board_state_o, boards_x, board_state_x, is_finish):
    date_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory_path = Path("data") / Path(date_time_str)
    directory_path.mkdir(parents=True, exist_ok=True)

    info_file = directory_path / "information.txt"
    with open(info_file, "w") as file:
        file.write(
            f"is_finish: {is_finish}\n"
            f"len(boards_o): {len(boards_o)}\n"
            f"len(board_state_o): {len(board_state_o)}\n"
            f"len(boards_x): {len(boards_x)}\n"
            f"len(board_state_x): {len(board_state_x)}\n"
        )

    with open(directory_path / "board_now.pkl", "wb") as file:
        pickle.dump(board_now, file)
    with open(directory_path / "boards_o.pkl", "wb") as file:
        pickle.dump(boards_o, file)
    with open(directory_path / "board_state_o.pkl", "wb") as file:
        pickle.dump(board_state_o, file)
    with open(directory_path / "boards_x.pkl", "wb") as file:
        pickle.dump(boards_x, file)
    with open(directory_path / "board_state_x.pkl", "wb") as file:
        pickle.dump(board_state_x, file)

    print("Data:", directory_path)


if __name__ == "__main__":
    import chessboard

    with open("data/2023-11-06_05-02-54/all_wins.pkl", "rb") as file:
        boards = pickle.load(file)
    his = chessboard.BoardHistory(boards[0])
    his.play()

# PYTHONHASHSEED=0
# import pickle
# import chessboard
# import numpy as np

# with open("data/2023-11-06_03-28-15/board_state.pkl", "rb") as file:
#     board_state = pickle.load(file)
# with open("data/2023-11-06_03-28-15/boards.pkl", "rb") as file:
#     boards = pickle.load(file)

# def find_state(board):
#     """Find the recoded state of the board

#     Returns
#     -------
#     bool or None
#     """
#     board_hash = hash(board.board.tobytes())
#     while True:
#         if boards[board_hash] is None:
#             break
#         board_hash = boards[board_hash]
#     return board_state[board_hash]

# board = chessboard.Board()
# next_chess = board.available_move(1)
# board.put(next_chess[0][1], 1)
# s = find_state(board)
# print(s)

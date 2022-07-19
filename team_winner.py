import random
from typing import Dict, Tuple

import numpy as np

# from check_submission import check_submission
from game_mechanics import (
    Connect4Env,
    choose_move_randomly,
    get_empty_board,
    get_piece_longest_line_length,
    get_top_piece_row_index,
    has_won,
    is_column_full,
    load_dictionary,
    place_piece,
    play_connect_4_game,
    save_dictionary,
)

TEAM_NAME = "Team Name"  # <---- Enter your team name here!
assert TEAM_NAME != "Team winner", "Please change your TEAM_NAME!"


def to_feature_vector(state: np.ndarray) -> Tuple:
    """
    TODO: Write this function to convert the state to a feature vector.

    We suggest you use functions in game_mechanics.py to make a handcrafted
     feature vector based on the state of the board.

    Feature vectors are covered in Tutorial 6 (don't need 4 or 5 to do 6!)

    Args:
        state: board state as a np array. 1's are your pieces. -1's your
                opponent's pieces & 0's are empty.

    Returns: the feature for this state, as designed by you.
    """
    raise NotImplementedError("You need to implement the to_feature_vector() function! :)")


def train() -> Dict:
    """
    TODO: Write this function to train your algorithm.

    Returns:
        Value function dictionary used by your agent. You can
         structure this how you like, but choose_move() expects
         {feature_vector: value}. If you structure it another
         way, you'll have to tweak choose_move().
    """
    pass


def choose_move(board, value_func):  # <- DO NOT CHANGE THIS LINE :)
    """Simple rules based solution.

    A good RL solution should beat me
    """
    possible_moves = range(board.shape[1])

    moves_with_full_cols_removed = []
    for move in possible_moves:
        if not is_column_full(board, move):
            moves_with_full_cols_removed.append(move)

    # 1 Check no moves where we win immediately
    for move in moves_with_full_cols_removed:
        # Copy to stop the moves we make affect the original board state
        copy_board = board.copy()
        # Let's look at the board when we place a piece at `move`
        copy_board, row_idx = place_piece(copy_board, move, 1)
        # Has that `move` won the game?
        if has_won(copy_board, move):
            print("1")
            return move

    # 2 Blocking - Take moves where we lose if we don't go there
    for move in moves_with_full_cols_removed:
        copy_board = board.copy()
        copy_board, row_idx = place_piece(copy_board, move, -1)
        if has_won(copy_board, move):
            print("2")
            return move

    # 3 Avoiding them winning on top - Avoid moves where they win by placing on top
    # [1, 2, 3, 4, 6, 7]
    for move in moves_with_full_cols_removed:
        # Copy to keep the original board clean
        copy_board = board.copy()

        # Make our move
        copy_board, row_idx = place_piece(copy_board, move, 1)
        if not is_column_full(copy_board, move):
            # They move on top of us!
            copy_board, row_idx = place_piece(copy_board, move, -1)

            # Checking - have THEY won by placing on top of us?
            if has_won(copy_board, move):
                print("3 - removing", move)
                moves_with_full_cols_removed.remove(move)
    # [1, 2, 3, 7]

    # 4 Prefer the center columns
    if 3 in moves_with_full_cols_removed or 4 in moves_with_full_cols_removed:
        center_cols = []
        # Try
        if 3 in moves_with_full_cols_removed:
            center_cols.append(3)
        if 4 in moves_with_full_cols_removed:
            center_cols.append(4)
        print("4")
        return random.choice(center_cols)

    # 5 Random!
    print("5")
    return random.choice(moves_with_full_cols_removed)  # <- this is the bug


if __name__ == "__main__":

    ## Example workflow, feel free to edit this! ###
    my_value_fn = train()
    save_dictionary(my_value_fn, TEAM_NAME)

    # check_submission()  # <---- Make sure I pass! Or your solution will not work in the tournament!!

    my_value_fn = load_dictionary(TEAM_NAME)

    # Code below plays a single game of Connect 4 against a random
    #  opponent, think about how you might want to adapt this to
    #  test the performance of your algorithm.
    def choose_move_no_value_fn(state: np.ndarray) -> int:
        """The arguments in play_connect_4_game() require functions that only take the state as
        input.

        This converts choose_move() to that format.
        """
        return choose_move(state, my_value_fn)

    play_connect_4_game(
        your_choose_move=choose_move_no_value_fn,
        opponent_choose_move=choose_move_randomly,
        game_speed_multiplier=1,
        render=True,
        verbose=True,
    )

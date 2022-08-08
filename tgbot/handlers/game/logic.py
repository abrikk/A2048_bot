import numpy as np

from tgbot.constants import CLASSIC_NUMBERS, CLASSIC_CONTROLLERS, VITALII_CONTROLLERS, EMOJI_NUMBERS
from tgbot.handlers.game.exceptions import BoardNotModifiedError


digit_to_emoji: dict = {
    '0': "0️⃣", '1': "1️⃣", '2': "2️⃣", '3': "3️⃣", '4': "4️⃣",
    '5': "5️⃣", '6': "6️⃣", '7': "7️⃣", '8': "8️⃣", '9': "9️⃣",
}


def num_to_emoji(n: int | str) -> str:
    return ''.join([digit_to_emoji.get(d, " ") for d in str(n)])


def get_start_board(size: int) -> np.ndarray:
    board = np.zeros([size, size], dtype=int)
    rng = np.random.default_rng()
    random_fields = rng.choice(board.size, size=2, replace=False)
    random_numbers = rng.choice([2, 4], size=2, p=[0.9, 0.1])

    for i, n in zip(random_fields, random_numbers):
        board.ravel()[i] = n

    return board


def prepare_board(board_dict: dict, numbers_style: str = CLASSIC_NUMBERS) -> dict:
    new_board_dict: dict = {}
    for key, value in board_dict.items():
        if key in ("score", "game_over", "max_num", "moves_made"):
            continue
        if numbers_style == CLASSIC_NUMBERS:
            new_board_dict[key] = [(key, str(v).replace("0", " ")) for v in value]
        elif numbers_style == EMOJI_NUMBERS:
            new_board_dict[key] = [(key, num_to_emoji(str(v).replace("0", " "))) for v in value]
        else:
            new_board_dict[key] = [(key, int_to_roman(str(v).replace("0", " "))) for v in value]

    return new_board_dict


def get_actions(style: str = CLASSIC_CONTROLLERS) -> dict:
    if style == CLASSIC_CONTROLLERS:
        # classic controllers
        directions: list[list[tuple]] = [
            [("empty", " "), ("vertical_up", "⬆️"), ("empty", " ")],
            [("horizontal_left", "⬅️"), ("vertical_down", "⬇️"), ("horizontal_right", "➡️")],
            False
        ]
    elif style == VITALII_CONTROLLERS:
        # vitalii's controllers
        directions: list[list[tuple]] = [
            [("empty", " "), ("vertical_up", "⬆️"), ("empty", " ")],
            [("horizontal_left", "⬅️"), ("empty", " "), ("horizontal_right", "➡️")],
            [("empty", " "), ("vertical_down", "⬇️"), ("empty", " ")]
        ]
    else:
        # mill controllers
        directions: list[list[tuple]] = [
            [("vertical_up", "⬆️"), ("horizontal_right", "➡️")],
            [("horizontal_left", "⬅️"), ("vertical_down", "⬇️")],
            False
        ]

    return {"first_line": directions[0], "second_line": directions[1], "third_line": directions[2]}


def convert_dict_to_matrix(board_dict: dict) -> np.ndarray:
    board: dict = {k: v for k, v in board_dict.items() if k not in ("score", "game_over", "max_num", "moves_made")}
    board_matrix: np.ndarray = np.zeros([len(board), len(board)], dtype=int)

    for i, row in enumerate(sorted(board.items())):
        board_matrix[i] = row[1]

    return board_matrix


def convert_matrix_to_dict(board: np.ndarray) -> dict:
    board_dict: dict = {}
    for i, line in enumerate(board, start=1):
        board_dict["fields_" + str(i)] = line

    return board_dict


def move_number_fields(array: np.ndarray, score: int = 0, direction: str = "horizontal_left") -> tuple[np.ndarray, int] or tuple[False, int]:
    """
    Moves all number fields in the given direction and adding random number of 2 (90%) or 4 (10%) to the board.

    :param array: the game board
    :param score: the current score
    :param direction: the chosen direction (defaults to left)
    :return: tuple[board, score] or tuple[False, score] if the game is over
    :raises BoardNotModifiedError: if the game board was not modified
    """

    # deep copying the array to check if there was a change in the end
    array_copy = array.copy()

    # adapting the array to the direction
    if direction == "vertical_up":
        array = array.transpose()
    elif direction == "vertical_down":
        array = np.fliplr(array.transpose())
    elif direction == "horizontal_right":
        array = np.fliplr(array)

    # moving the zeros
    for line_index, row in enumerate(array):
        start_from = 0

        while start_from < len(row):
            array[line_index] = np.array(move_zeros(row))

            for index, n in enumerate(row[start_from:]):
                if n != 0 and len(array[line_index]) != index + 1 and n == array[line_index, index + 1]:
                    array[line_index, index] += array[line_index, index + 1]
                    array[line_index, index + 1] = 0
                    score += array[line_index, index]
                    continue
                else:
                    start_from += 1

    if np.array_equal(array_copy, array if direction == "horizontal_left" else array.base) and not is_game_over(array):
        raise BoardNotModifiedError()

    empty_fields: np.ndarray = np.where(array == 0)
    empty_fields_indices: list[tuple] = list(zip(empty_fields[0], empty_fields[1]))

    if len(empty_fields_indices) == 0 and is_game_over(array):
        # no empty fields left -> game over
        return False, score

    # adding a random number to the empty field
    rng = np.random.default_rng()
    rnd_fld = rng.choice(np.random.permutation(empty_fields_indices), shuffle=False)

    array[rnd_fld[0], rnd_fld[1]] = rng.choice([2, 4], p=[0.9, 0.1])

    return array if direction == "horizontal_left" else array.base, score


def is_game_over(array: np.ndarray) -> bool:
    if np.any(array == 0):
        return False

    deployed_array = np.vstack((array, array.transpose()))

    for row in deployed_array:
        for i, n in enumerate(row):

            if len(row) == i + 1:
                break

            if n == row[i + 1]:
                return False

    return True


def move_zeros(array):
    return np.array([i for i in array if i != 0] + [i for i in array if i == 0])


def when_not(key: str):
    def f(data, _whenable, _manager):
        return not data.get(key)

    return f


def int_to_roman(num: int | str) -> str:
    try:
        num = int(num)
    except ValueError:
        return " "

    m = ["", "M", "MM", "MMM", "Mↁ", "ↁ", "ↁM", "ↁMM", "ↁMMM", "Mↂ",
         "ↂ", "ↂM", "ↂMM", "ↂMMM", "ↂMↁ", "ↂↁ", "ↂↁM", "ↂↁMM", "ↂↁMMM", "ↂMↂ", "ↂↂ",
         "ↂↂM", "ↂↂMM", "ↂↂMMM", "ↂↂMↁ", "ↂↂↁ", "ↂↂↁM", "ↂↂↁMM", "ↂↂↁMMM", "ↂↂMↂ", "ↂↂↂ",
         "ↂↂↂM", "ↂↂↂMM", "ↂↂↂMMM", "ↂↂↂMↁ", "ↂↂↂↁ", "ↂↂↂↁM", "ↂↂↂↁMM", "ↂↂↂↁMMM", "ↂↂↂMↂ", "ↂↇ",
         "ↂↇM", "ↂↇMM", "ↂↇMMM", "ↂↇMↁ", "ↂↇↁ", "ↂↇↁM", "ↂↇↁMM", "ↂↇↁMMM", "ↂↇMↂ", "ↇ",
         "ↇM", "ↇMM", "ↇMMM", "ↇMↁ", "ↇↁ", "ↇↁM", "ↇↁMM", "ↇↁMMM", "ↇMↂ", "ↇↂ",
         "ↇↂM", "ↇↂMM", "ↇↂMMM", "ↇↂMↁ", "ↇↂↁ", "ↇↂↁM", "ↇↂↁMM", "ↇↂↁMMM", "ↇↂMↂ", "ↇↂↂ"]
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = (thousands + hundreds + tens + ones)

    return ans

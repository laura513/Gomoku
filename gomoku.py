"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""


def is_empty(board):
    # returns True if there's no stones on board
    for i in range(len(board)):
        for k in range(len(board[0])):
            if board[i][k] == "w" or board[i][k] == "b":
                # If there's any stones, return False
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    open_start = False
    open_end = False
    y_start = y_end - d_y * (length - 1)
    x_start = x_end - d_x * (length - 1)

    if y_end == 0 or x_end == 0 or y_end == len(board) - 1 or x_end == len(board) - 1:
        open_end = False
        # Check before the start of the sequence
        if 0 <= y_start - d_y < len(board) and 0 <= x_start - d_x < len(board[0]):
            if board[y_start - d_y][x_start - d_x] == " ":
                open_start = True
        else:
            # If the start is at the border, we consider it closed at the start
            open_start = False
    else:
        # Check after the end of the sequence
        if 0 <= y_end + d_y < len(board) and 0 <= x_end + d_x < len(board[0]):
            if board[y_end + d_y][x_end + d_x] == " ":
                open_end = True
        else:
            # If the end is at the border, we consider it closed at the end
            open_end = False

        if 0 <= y_start - d_y < len(board) and 0 <= x_start - d_x < len(board[0]):
            if board[y_start - d_y][x_start - d_x] == " ":
                open_start = True
        else:
            # If the start is at the border, we consider it closed at the start
            open_start = False
    if open_start and open_end:
        return "OPEN"
    elif open_start or open_end:
        return "SEMIOPEN"
    else:
        return "CLOSED"


def has_length(board, col, c, d, length, d_y, d_x):
    # Check to see if there is a sequence with length 'length' start at c, d)
    for i in range(length):
        if board[c + i*d_y][d + i*d_x] == col:
            continue
        else:
            return False
    # Check to see if this sequence is longer than length 'length'
    last_y = c - d_y
    last_x = d - d_x
    # Check the one before the sequence
    if 0 <= last_y < len(board) and 0 <= last_x < len(board[0]):
        if board[last_y][last_x] == col:
            return False
    next_y = c + length*d_y
    next_x = d + length*d_x
    # Check the one after the sequence
    if 0 <= next_y < len(board) and 0 <= next_x < len(board[0]):
        if board[next_y][next_x] == col:
            return False
    return True


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_count = 0
    for k in range(len(board)):
        # Check every number in the row
        c = y_start + k*d_y
        d = x_start + k*d_x
        if 0 <= c + (length-1)*d_y < len(board) and 0 <= d + (length-1)*d_x < len(board[0]):
            # Only complete sequences count, call the helper function has_length
            if has_length(board, col, c, d, length, d_y, d_x):
                # If has length, difine y_end and x_end to use in is_bounded
                y_end, x_end = c + (length-1)*d_y, d + (length-1)*d_x
                if is_bounded(board , y_end, x_end, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_count += 1
    return open_seq_count, semi_open_count


def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    # Check horizontal sequences
    for i in range(len(board)):
        result = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]

    # Check vertical sequences
    for j in range(len(board[0])):
        result = detect_row(board, col, 0, j, length, 1, 0)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]

    # Check diagonal sequences from top-left to bottom-right
    for i in range(len(board)):
        result = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]

    # Start from 1 to avoid double-counting the top-left corner
    for j in range(1, len(board[0])):
        result = detect_row(board, col, 0, j, length, 1, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]

    # Check diagonal sequences from bottom-left to top-right
    for i in range(len(board)):
        result = detect_row(board, col, i, 0, length, -1, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]

    # Initialize max_score with a value less than any possible score
    for j in range(1, len(board[0])):
        result = detect_row(board, col, len(board) - 1, j, length, -1, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]

    return open_seq_count, semi_open_seq_count


def search_max(board):
    # Initialize max_score with a value less than any possible score
    max_score = -100000
    lst = list(range(len(board)))
    move_y, move_x = -1, -1
    # The first move take by the computer should be in the middle
    if is_empty(board):
        # Integer division for center
        move_y, move_x = len(board) // 2, len(board[0]) // 2
        return move_y, move_x
    else:
        for i in range(len(board)):
            for k in range(len(board[0])):
                 # Only consider empty positions
                if board[i][k] == " ":
                    # Create a deep copy of the board
                    fake_board = [row[:] for row in board]
                    fake_board[i][k] = "b"
                    fake_score = score(fake_board)
                    if max_score < fake_score:
                        # The first best move is chosen if scores are equal
                        max_score = fake_score
                        move_y, move_x = i, k
    print(move_y, move_x)
    return move_y, move_x


def is_win(board):
    board_size = len(board)
    # Directions to look: horizontal, vertical, diagonal down-right, diagonal up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for y in range(board_size):
        for x in range(board_size):
            if board[y][x] != " ":
                for d_y, d_x in directions:
                    # Check for five in a row in each direction.
                    count = 0
                    for i in range(5):
                        new_y = y + i * d_y
                        new_x = x + i * d_x
                        if 0 <= new_y < board_size and 0 <= new_x < board_size:
                            if board[new_y][new_x] == board[y][x]:
                                count += 1
                            else:
                                break
                        else:
                            # Out of bounds
                            break
                    if count == 5:
                        if board[y][x] == "b":
                            return "Black won"
                        elif board[y][x] == "w":
                            return "White won"

    # Check for draw
    for y in range(board_size):
        for x in range(board_size):
            # If there's an empty space, continue playing
            if board[y][x] == " ":
                return "Continue playing"

    # If no empty space and no won, it's a draw
    return "Draw"

### Starter codes
def score(board):
    # Computes and return the score for the position of the board, assume black
    # just moved
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])



def print_board(board):
    # Print the board
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    # Make a square board that's sz x sz
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    # Analysis the position of the board by computing the number of
    # open and semi-open sequences on both colors
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))



def play_gomoku(board_size):
    # Interacts with the AI engine by calling search_max()
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        print(game_res)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return(game_res)


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    # put a sequence of colors on board, facilitates the testing of AI
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

### Tests
def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print(detect_row(board, "w", 0,x,length,d_y,d_x))
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print(detect_rows(board, col, length))
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print(search_max(board))
        print("TEST CASE for search_max FAILED")

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

           # Expected output:
           #    *0|1|2|3|4|5|6|7*
           #    0 | | | | |w|b| *
           #    1 | | | | | | | *
           #    2 | | | | | | | *
           #    3 | | | | |b| | *
           #    4 | | | |b| | | *
           #    5 | |w|b| | | | *
           #    6 | |w| | | | | *
           #    7 | |w| | | | | *
           #    *****************
           #
           #
           # Black stones:
           # Open rows of length 2: 0
           # Semi-open rows of length 2: 0
           # Open rows of length 3: 0
           # Semi-open rows of length 3: 1
           # Open rows of length 4: 0
           # Semi-open rows of length 4: 0
           # Open rows of length 5: 0
           # Semi-open rows of length 5: 0
           # White stones:
           # Open rows of length 2: 0
           # Semi-open rows of length 2: 0
           # Open rows of length 3: 0
           # Semi-open rows of length 3: 1
           # Open rows of length 4: 0
           # Semi-open rows of length 4: 0
           # Open rows of length 5: 0
           # Semi-open rows of length 5: 0



def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

if __name__ == '__main__':
    play_gomoku(8)
    # easy_testset_for_main_functions()
    # some_tests()

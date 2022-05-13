import chess  # get access to the chess library
import time
from pythonosc import udp_client  # get access to Sonic Pi

global fen  # variable to hold board state

duration = 1  # amount of time between moves

board = chess.Board()  # create board object
board.reset_board()  # set the board to the starting state (redundant)

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)  # connects Python to Sonic Pi


def read_file(file):  # process the text file containing the moves for the game
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        line.rstrip()
    return lines


def parse_fen():  # take FEN and parse it out into a format that I can use
    temp = ['', '', '', '', '', '', '', '']
    counter = 0
    for i in range(len(fen)):
        if fen[i] != '/':
            temp[counter] += fen[i]
        else:
            counter += 1

    squares = [['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0']]

    for i in range(8):
        counter = 0
        for j in range(len(temp[i])):
            if not temp[i][j].isdigit():
                squares[i][counter] = temp[i][j]
            else:
                counter += (int(temp[i][j]) - 1)
            counter += 1

    return squares


def translate_to_osc(squares):  # take the parsed results and send them to Sonic Pi
    for x in range(len(squares)):
        for y in range(len(squares[x])):
            if squares[x][y] != '0':  # determine synth sound
                if squares[x][y] == 'p' or squares[x][y] == 'P':
                    message = "/trigger/sine"
                elif squares[x][y] == 'b' or squares[x][y] == 'B':
                    message = "/trigger/saw"
                elif squares[x][y] == 'n' or squares[x][y] == 'N':
                    message = "/trigger/square"
                elif squares[x][y] == 'r' or squares[x][y] == 'R':
                    message = "/trigger/pulse"
                elif squares[x][y] == 'q' or squares[x][y] == 'Q':
                    message = "/trigger/supersaw"
                elif squares[x][y] == 'k' or squares[x][y] == 'K':
                    message = "/trigger/chiplead"
                else:
                    message = " "
                if y == 0:  # determine pitch
                    sender.send_message(message, [4 * (8 - x), 100, duration])
                elif y == 1:
                    sender.send_message(message, [6 * (8 - x), 100, duration])
                elif y == 2:
                    sender.send_message(message, [7 * (8 - x), 100, duration])
                elif y == 3:
                    sender.send_message(message, [9 * (8 - x), 100, duration])
                elif y == 4:
                    sender.send_message(message, [11 * (8 - x), 100, duration])
                elif y == 5:
                    sender.send_message(message, [13 * (8 - x), 100, duration])
                elif y == 6:
                    sender.send_message(message, [14 * (8 - x), 100, duration])
                elif y == 7:
                    sender.send_message(message, [16 * (8 - x), 100, duration])


game = read_file('game')

k = 0

while not board.is_game_over():  # as long as the game is still going, loop through the indented lines
    nextMove = game[k].rstrip()  # get the next move
    print(nextMove)
    board.push_san(nextMove)  # make that move on the board object
    fen = board.board_fen()  # store the board state
    translate_to_osc(parse_fen())  # parse the board state and send it to Sonic Pi
    k += 1
    time.sleep(duration)  # wait for a set amount of time

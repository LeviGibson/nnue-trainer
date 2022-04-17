import chess
import hashlib
import random

infile = open("analysed.pgn")
outfile = open("chessDataUnshuffled.csv", 'w')

usedKeys = []

def is_quiet_position(board : chess.Board):
    if board.is_check(): return 0
    for move in list(board.legal_moves):
        if board.is_capture(move): return 0
    return 1

numFeatures = 0
for lineId, line in enumerate(infile):

    print(numFeatures)
    if numFeatures > 160000000:
        break
    
    line = line.replace('{', '')
    line = line.replace('}', '')
    line = line.replace(']', '')
    line = line.replace('[', '')
    line = line.replace('.', '')
    line = line.replace('?', '')
    line = line.replace('!', '')
    line = line.replace('%eval ', '')
    line = line.split('  ')


    for id, obj in enumerate(line):
        if 'clk' in obj:
            line[id] = obj.split(' ')[0]
        elif ' ' in obj:
            line[id] = obj.split(' ')[1]

    moves = []
    evals = []

    for obj in line:
        try:
            if obj[0] != '#':
                int(obj)
            evals.append(obj)
        except:
            moves.append(obj)

    evals = evals[1:]
    board = chess.Board()
    id = 0
    for smove, eval in zip(moves, evals):
        move = board.parse_san(smove)
        fen = board.fen()

        if (not board.is_capture(move)) and len(list(board.generate_pseudo_legal_captures())) < 4 and (not board.gives_check(move)):
            outfile.write("{},{}\n".format(fen, str(eval)))
            numFeatures+=1
            if numFeatures % 1000 == 0:print(numFeatures)

        board.push(move)

        id+=1


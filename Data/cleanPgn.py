import chess
import hashlib
import random

infile = open("analysed.pgn")
outfile = open("chessData.csv", 'w')

usedKeys = []

def is_quiet_position(board : chess.Board):
    if board.is_check(): return 0
    for move in list(board.legal_moves):
        if board.is_capture(move): return 0
    return 1

for lineId, line in enumerate(infile):
    if lineId % 10000 == 0:print(lineId)
    
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
        if ' ' in obj:
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

    board = chess.Board()
    id = 0
    for smove, eval in zip(moves, evals):
        board.push_san(smove)

        fen = board.fen()
        if id < 6:
            key = hashlib.md5(bytes(fen, encoding='ascii')).digest()
            if key in usedKeys:
                continue
            usedKeys.append(key)

        if is_quiet_position(board) or random.randint(0, 50) == 0:
            outfile.write("{},{}\n".format(fen, str(eval)))

        id+=1

import chess
import hashlib
import numpy as np

infile = open("analysed.pgn")
outfile = open("chessDataUnshuffled.csv", 'w')

HASH_SIZE = 100000
hash = np.zeros((HASH_SIZE,), bool)

def is_quiet_position(board : chess.Board):
    if board.is_check(): return 0
    for move in list(board.legal_moves):
        if board.is_capture(move): return 0
    return 1

numFeatures = 0
for lineId, line in enumerate(infile):

    print(numFeatures)
    if numFeatures > 41000000:
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

    #lichess analysed games do not include the evaluation of the starting position
    #so it is just added here (cp=0.20)
    evals = [20]
    moves = []

    for obj in line:
        try:
            if obj[0] != '#':
                int(obj)
            evals.append(obj)
        except:
            moves.append(obj)

    #the position after the final move of the game is not looked at
    #but it's included in lichess analyzed games
    evals.pop()

    board = chess.Board()
    id = 0
    padding = 0
    for smove, eval in zip(moves, evals):
        move = board.parse_san(smove)
        fen = board.fen()

        if padding:
            padding-=1
            id+=1
            board.push(move)
            continue

        if id < 6:
            key = int(hashlib.sha256(fen.encode('utf-8')).hexdigest(), 16) % HASH_SIZE
            if hash[key]:
                board.push(move)
                id+=1
                continue
            hash[key] = True

        if (not board.is_capture(move)) and len(list(board.generate_pseudo_legal_captures())) < 4 and (not board.gives_check(move)):
            padding = 8
            outfile.write("{},{}\n".format(fen, str(eval)))
            numFeatures+=1
            if numFeatures % 1000 == 0:print(numFeatures)

        board.push(move)

        id+=1


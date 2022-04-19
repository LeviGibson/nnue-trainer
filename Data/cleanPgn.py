import chess
import hashlib
import random
import numpy as np

infile = open("analysed.pgn")
outfile = open("chessDataUnshuffled.csv", 'w')

numFeatures = 0
for lineId, line in enumerate(infile):

    try:
        if lineId % 1000 == 0:
            print(numFeatures)
        # if numFeatures > 41000000:
        #     break
        
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
        padding = random.randint(0, 8)

        for smove, eval in zip(moves, evals):
            move = board.parse_san(smove)

            if padding:
                padding-=1
                id+=1
                board.push(move)
                continue

            if (not board.is_capture(move)) and (not board.gives_check(move)) and len(list(board.generate_pseudo_legal_captures())) < 4:
                fen = board.fen()
                padding = 8
                outfile.write("{},{}\n".format(fen, str(eval)))
                numFeatures+=1

            board.push(move)

            id+=1
    except:
        print("ERROR")

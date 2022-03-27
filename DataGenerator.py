import numpy as np
import chess
import halfkp
import chess.pgn
import hashlib
import random

infile = open("data.pgn", 'r')

def result_to_int(res):
    if res == '1-0': return 1
    if res == '0-1': return 0
    if res == '1/2-1/2': return .5
    print("nope")
    print(res)
    exit(1)

def generate(rows, fname):
    labels = []
    fens = []

    gamesProcessed = 0
    featureCount = 0

    while gamesProcessed < rows:
        game = chess.pgn.read_game(infile)
        moves = game.mainline_moves()
        board = chess.Board()
        gameResult = result_to_int(game.headers['Result'])
        featureIndexes = []
        for i in range(10):
            featureIndexes.append(random.randint(0, len(list(moves))))

        for mid, move in enumerate(moves):
            if mid in featureIndexes:
                feature = np.packbits(halfkp.get_halfkp_indeicies(board))
                np.save(fname + "features/{}".format(featureCount), feature)
                labels.append(gameResult)
                fens.append(board.fen())
                featureCount+=1

            board.push(move)

        gamesProcessed+=1
        print(gamesProcessed)

    np.save(fname + "labels", np.array(labels))
    np.save(fname + "fens", np.array(fens))

generate(40000, "train_")
generate(1000, "val_")

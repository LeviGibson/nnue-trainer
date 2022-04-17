import numpy as np
from chess import Board
import halfkp
from math import pow
from npy_append_array import NpyAppendArray

infile = open("Data/chessData.csv", 'r')

def result_to_int(res):
    if res == '1-0': return 1
    if res == '0-1': return 0
    if res == '1/2-1/2': return .5
    print("nope")
    print(res)
    exit(1)

def generate(rows, fname):
    # features = []
    labels = []
    # fens = []

    features = NpyAppendArray(fname + "features.npy")

    for lineId in range(rows):
        if lineId % 1000 == 0:
            print(lineId)

        line = infile.readline().split(',')
        if line[1][0:1] == '#-':
            line[1] = 0
        elif line[1][0] == '#':
            line[1] = 1
        else:
            line[1] = float(line[1])/100
            line[1] = 1/(1+pow(2, -line[1]))

        board = Board(line[0])
        
        feature = halfkp.get_halfkp_indeicies(board)
        features.append(np.array([feature]))
        labels.append(line[1])

    np.save(fname + "labels", np.array(labels))
    # labels = 0
    # np.save(fname + "fens", np.array(fens))
    # fens = 0
    # np.save(fname + "features", np.array(features))
    # features = 0
    # np.save(fname + "fens", np.array(fens))

generate(40000000, "train_")
generate(20000, "val_")
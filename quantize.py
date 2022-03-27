import tensorflow as tf
from halfkp import get_halfkp_indeicies
import chess
from chess import Board
import numpy as np
from halfkp import flipPers
import struct

def load_params():
    weights, biases = [], []

    model = tf.keras.models.load_model("production/")
    params = model.get_weights()

    for p in params:
        if len(p.shape) == 2:
            weights.append(p)
        else:
            biases.append(p)

    return weights, biases

weights, biases = load_params()

def activation(x):
    x[x < 0] = 0
    return x

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def propogate(a):
    global weights, biases
    for w,b in zip(weights,biases):
        if b.shape == (1,):
            a = np.matmul(w.T,a) + b
        else:
            a = activation(np.matmul(w.T,a))//64
            # print(a)
    return a

for id, w in enumerate(weights):
    weights[id] = (w*64).astype(int)

for id, b in enumerate(biases):
    biases[id] = (b*64).astype(int)

# indicies = get_halfkp_indeicies(Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
# ip = propogate(indicies)
# print(ip)

outfile = open("network.nnom", "wb")

#print(weights[0])

#for i in range(98304):
#    for j in range(512):
#        if weights[0][i][j]:print(i, j)

for i in weights[0].flatten():
    outfile.write(struct.pack('<h', round(i)))

for i in weights[1].transpose().flatten():
    outfile.write(struct.pack('<h', round(i)))

for i in b[0].flatten():
    outfile.write(struct.pack('<h', round(i)))

b[1] *= 2

for i in b[1].flatten():
    outfile.write(struct.pack('<i', round(i)))

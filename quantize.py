import tensorflow as tf
from halfkp import get_halfkp_indeicies
import chess
from chess import Board
import numpy as np
from halfkp import flipPers
import struct
from math import pow

np.set_printoptions(suppress=True)

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
    x //= 127
    x[x < 0] = 0
    x[x > 127] = 127
    return x

def f_activation(x):
    x[x < 0] = 0
    x[x > 1] = 1
    return x

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def propogate(a):
    global weights, biases

    a = a.reshape(2, -1)
    a = np.array([np.matmul(weights[0].T,a[0]) + biases[0], np.matmul(weights[0].T,a[1]) + biases[0]]).reshape((512,))
    a[a < 0] = 0
    a[a > 127] = 127
    # print(a)

    for w,b in zip(weights[1:],biases[1:]):
        if b.shape == (1,):
            a = ((np.matmul(w.T,a) + b) )
            # a = a.astype(float) / 128
            # print(a)
            # a = (np.matmul(w.T,a) + b) / 128
            # a = a[0]
            # return 1/(1+pow(2.71828, -a))
        else:
            a = activation(np.matmul(w.T,a) + b)
            print(a)
            print()
    return a

def f_propogate(a):
    global weights, biases

    a = a.reshape(2, -1)
    a = np.array([np.matmul(weights[0].T,a[0]) + biases[0], np.matmul(weights[0].T,a[1]) + biases[0]]).reshape((512,))
    a = f_activation(a)
    print(a)

    for w,b in zip(weights[1:],biases[1:]):
        if b.shape == (1,):
            a = np.matmul(w.T,a) + b
            a = a[0]
            return 1/(1+pow(2.71828, -a))
        else:
            a = f_activation(np.matmul(w.T,a) + b)
            print(a)
            print()
    return a

def quantize():
    weights[0] /= 4
    for id, w in enumerate(weights):
        weights[id] = (w*127).astype(int)

    for id, b in enumerate(biases):
        biases[id] = (b*127).astype(int)

def propogate_all():
    indicies = get_halfkp_indeicies(Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
    ip = propogate(indicies)
    print(ip)

def write():
    outfile = open("network.nnue", "wb")

    for i in weights[0].flatten():
        outfile.write(struct.pack('<h', i))

    for i in weights[1].flatten():
        outfile.write(struct.pack('<b', i))

    for i in weights[2].flatten():
        outfile.write(struct.pack('<b', i))

    for i in weights[3].flatten():
        outfile.write(struct.pack('<b', i))

    for i in biases[0]:
        outfile.write(struct.pack('<h', i))

    for i in biases[1]:
        outfile.write(struct.pack('<i', i))

    for i in biases[2]:
        outfile.write(struct.pack('<i', i))

    for i in biases[3]:
        outfile.write(struct.pack('<i', i))


quantize()
# propogate_all()
write()
# indicies = get_halfkp_indeicies(Board("k1n5/6pR/p1p1Rp2/2B3P1/2p5/P7/1PP5/1K6 w - - 3 42"))

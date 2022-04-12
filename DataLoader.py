import tensorflow.keras as keras
import numpy as np
import math
import random

class DataLoader(keras.utils.Sequence):

    def __init__(self, batch_size, name, shuffle=True):
        self.labels = np.load(name + "_labels.npy", mmap_mode='r')
        self.features = np.load(name + "_features.npy", mmap_mode='r')
        # self.fens = np.load(name + "_fens.npy")
        self.batch_size = batch_size
        self.index_transformation = list(range(len(self.labels)))
        if shuffle: self.randomise()
        self.name = name

    def randomise(self):
        for i in range(len(self.index_transformation)):
            target = random.randint(0, len(self.index_transformation)-1)
            self.index_transformation[target], self.index_transformation[i] = self.index_transformation[i], self.index_transformation[target]

    def __len__(self):
        return math.floor(len(self.labels) / self.batch_size)

    def __getitem__(self, idx):
        x = (np.zeros((self.batch_size, 12*64*64), bool), 
            np.zeros((self.batch_size, 12*64*64), bool))
            
        y = np.zeros((self.batch_size,))
        for i in range(self.batch_size):
            index = self.index_transformation[i+(idx*self.batch_size)]
            
            ids = self.features[index]
            for id in ids:
                if id != 0:
                    if id >= 49152:
                        x[1][i][id - 49152] = True
                    else:
                        x[0][i][id] = True
            
            y[i] = self.labels[index]

        return x, y

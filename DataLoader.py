import tensorflow.keras as keras
import numpy as np
import math
import random

class DataLoader(keras.utils.Sequence):

    def __init__(self, batch_size, name, shuffle=True):
        if not shuffle:
            self.labels = np.load(name + "_labels.npy", mmap_mode='r')
            self.features = np.load(name + "_features.npy", mmap_mode='r')
        else:
            self.labels = np.load(name + "_labels_shuffled.npy", mmap_mode='r')
            self.features = np.load(name + "_features_shuffled.npy", mmap_mode='r')

        self.batch_size = batch_size
        self.name = name

    def __len__(self):
        return math.floor(len(self.labels) / self.batch_size)

    def __getitem__(self, idx):
        x = (np.zeros((self.batch_size, 6*64), bool), 
            np.zeros((self.batch_size, 6*64), bool))
            
        y = np.zeros((self.batch_size,))
        for i in range(self.batch_size):
            index = i+(idx*self.batch_size)
            
            ids = self.features[index]
            ids = ids[ids > 0]
            h2 = ids[ids >= 384] - 384
            h1 = ids[ids < 384]

            np.add.at(x[0][i], h1, h1.astype(bool))
            np.add.at(x[1][i], h2, h2.astype(bool))

            # for id in ids:
            #     if id != 0:
            #         if id >= 49152:
            #             x[1][i][id - 49152] = True
            #         else:
            #             x[0][i][id] = True
            
            y[i] = self.labels[index]

        return x, y

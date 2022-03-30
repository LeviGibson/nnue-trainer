import tensorflow.keras as keras
import numpy as np
import math
import random

class DataLoader(keras.utils.Sequence):

    def __init__(self, batch_size, name):
        self.labels = np.load(name + "_labels.npy")
        self.fens = np.load(name + "_fens.npy")
        self.batch_size = batch_size
        self.index_transformation = list(range(len(self.labels)))
        self.randomise()
        self.name = name

    def randomise(self):
        for i in range(len(self.index_transformation)):
            target = random.randint(0, len(self.index_transformation)-1)
            self.index_transformation[target], self.index_transformation[i] = self.index_transformation[i], self.index_transformation[target]

    def __len__(self):
        return math.floor(len(self.labels) / self.batch_size)

    def __getitem__(self, idx):
        x = [[], []]
        y = np.zeros((self.batch_size,))
        for i in range(self.batch_size):
            index = self.index_transformation[i+(idx*self.batch_size)]
            
            tx = np.load(self.name + "_features/{}.npy".format(index)).reshape(2, -1)
            x[0].append(tx[0])
            x[1].append(tx[1])
            y[i] = self.labels[index]

        x = (np.array(x[0]), np.array(x[1]))
        return x, y
    
    def getfen(self, idx):
        x = []
        for i in range(self.batch_size):
            index = self.index_transformation[i+(idx*self.batch_size)]
            x.append(self.fens[index])

        return x

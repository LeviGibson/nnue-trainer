import halfkp
from chess import Board
import numpy as np

ids = halfkp.get_halfkp_indeicies(Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
h1 = ids[ids >= 49152] - 49152
h2 = ids[ids < 49152]

features = np.zeros((2, 49152), bool)
np.add.at(features[0], h1, h1.astype(bool))
np.add.at(features[1], h2, h2.astype(bool))

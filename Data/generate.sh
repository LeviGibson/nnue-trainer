#!/bin/bash
/opt/pypy3.8/bin/pypy3 ./cleanPgn.py
shuf chessDataUnshuffled.csv >> chessData.csv
cd ..
/opt/pypy3.8/bin/pypy3 ./DataGenerator.py

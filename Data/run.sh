#!/bin/bash
sudo ls
sudo ls
wget https://database.lichess.org/standard/lichess_db_standard_rated_2022-02.pgn.bz2
pbzip2 -d ./lichess_db_standard_rated_2022-02.pgn.bz2
mv ./lichess_db_standard_rated_2022-02.pgn ./data.pgn
/opt/pypy3.8/bin/pypy3 ./findAnalysedGames.py
/opt/pypy3.8/bin/pypy3 ./cleanPgn.py
sudo poweroff

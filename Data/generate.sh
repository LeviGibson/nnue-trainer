#!/bin/bash

wget -O raw.pgn.bz2 https://database.lichess.org/standard/lichess_db_standard_rated_2022-03.pgn.bz2
pbzip2 -d raw.pgn.bz2 -v
mv *.pgn data.pgn
/opt/pypy3.8/bin/pypy3 ./findAnalysedGames.py
rm data.pgn
/opt/pypy3.8/bin/pypy3 ./cleanPgn.py
shuf chessDataUnshuffled.csv >> 1.csv
rm chessDataUnshuffled.csv
rm all.txt
cat *.csv >> all.txt

# wget -O raw.pgn.bz2 https://database.lichess.org/standard/lichess_db_standard_rated_2022-02.pgn.bz2
# pbzip2 -d raw.pgn.bz2 -v
# mv *.pgn data.pgn
# /opt/pypy3.8/bin/pypy3 ./findAnalysedGames.py
# rm data.pgn
# /opt/pypy3.8/bin/pypy3 ./cleanPgn.py
# shuf chessDataUnshuffled.csv >> 1.csv
# rm chessDataUnshuffled.csv
# rm all.txt
# cat *.csv >> all.txt

# wget -O raw.pgn.bz2 https://database.lichess.org/standard/lichess_db_standard_rated_2022-01.pgn.bz2
# pbzip2 -d raw.pgn.bz2 -v
# mv *.pgn data.pgn
# /opt/pypy3.8/bin/pypy3 ./findAnalysedGames.py
# rm data.pgn
# /opt/pypy3.8/bin/pypy3 ./cleanPgn.py
# shuf chessDataUnshuffled.csv >> 1.csv
# rm chessDataUnshuffled.csv
# rm all.txt
# cat *.csv >> all.txt
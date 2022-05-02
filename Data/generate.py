import wget
import os
import subprocess
import findAnalysedGames
import cleanPgn

urls = ["https://database.lichess.org/standard/lichess_db_standard_rated_2022-03.pgn.bz2", 
    "https://database.lichess.org/standard/lichess_db_standard_rated_2022-02.pgn.bz2", 
    "https://database.lichess.org/standard/lichess_db_standard_rated_2022-01.pgn.bz2"]

for urlId, url in enumerate(urls):
    filename = wget.download(url)
    os.rename(filename, "data.pgn.bz2")

    with subprocess.Popen(["pbzip2", "-d", './data.pgn.bz2'], shell=True) as process:
        process.wait()

    findAnalysedGames.run()
    os.remove("data.pgn")

    cleanPgn.run()

    with subprocess.Popen(["shuf", "./chessDataUnshuffled.csv", ">>", "{}.csv".format(urlId)], shell=True) as process:
        process.wait()

    os.remove("chessDataUnshuffled.csv")

import wget
import os
import subprocess
import findAnalysedGames
import cleanPgn

filesMade = 2

urls = [
    "https://database.lichess.org/standard/lichess_db_standard_rated_2022-04.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2022-03.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2022-02.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2022-01.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-12.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-11.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-10.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-09.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-08.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-07.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-06.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-05.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-04.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-03.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-02.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2021-01.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-12.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-11.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-10.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-09.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-08.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-07.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-06.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-05.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-04.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-03.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-02.pgn.bz2",
    "https://database.lichess.org/standard/lichess_db_standard_rated_2020-01.pgn.bz2",]

for urlId, url in enumerate(urls):
    # filename = wget.download(url)
    # os.rename(filename, "data.pgn.bz2")

    with subprocess.Popen(["pbzip2 -d ./data.pgn.bz2 -v -k"], shell=True) as process:
        process.wait()

    findAnalysedGames.run()
    os.remove("data.pgn")

    cleanPgn.run()

    with subprocess.Popen(["shuf ./chessDataUnshuffled.csv >> {}.csv".format(urlId + filesMade)], shell=True) as process:
        process.wait()

    os.remove("analysed.pgn")
    os.remove("chessDataUnshuffled.csv")

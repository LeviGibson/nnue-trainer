def run():
    infile = open("data.pgn")
    outfile = open("analysed.pgn", 'w')
    gamesFound = 0
    print("finding analysed games")

    pgn = ""
    for id, line in enumerate(infile):
        if line[0] != "[":
            if "%eval" in line:
                gamesFound+=1
                outfile.write(line)

if __name__ == '__main__':
    run()
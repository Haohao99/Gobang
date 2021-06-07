import socket
import sys
import threading
from board import Board
import pickle
import time

class client_thread(threading.Thread):
    def __init__(self, client, gameIndex):
        threading.Thread.__init__(self)
        self.client = client
        self.gameIndex = gameIndex
    def run(self):
        global gameList, currentId, gameNum
        currentBoard = gameList[self.gameIndex]
        if gameNum % 2 == 0:
            currentId = "w"
        else:
            currentId = "b"
        currentBoard.start_user = currentId
        data_string = pickle.dumps(currentBoard)
        if currentId == "b":
            currentBoard.ready = True
            currentBoard.startTime = time.time()
        self.client.send(data_string)
        gameNum += 1
        while True:
            if self.gameIndex not in gameList:
                break
            try:
                incomingData = self.client.recv(8192 * 3)
                rawData = incomingData.decode("utf-8")
                if not incomingData:
                    break
                else:
                    if rawData == "B_win":
                        currentBoard.winner = "b"
                    if rawData == "W_win":
                        currentBoard.winner = "w"
                    if rawData.count("choose") > 0:
                        data = rawData.split(" ")
                        col = int(data[1])
                        row = int(data[2])
                        color = data[3]
                        currentBoard.select(col, row, color)
                    if rawData.count("playerName") == 1:
                        name = rawData.split(" ")[1]
                        if currentId == "b":
                            currentBoard.plater2 = name
                        elif currentId == "w":
                            currentBoard.player1 = name
                    if currentBoard.ready:
                        if currentBoard.turn == "w":
                            currentBoard.time1 = 900 - (time.time() - currentBoard.startTime) - currentBoard.storedTime1
                        else:
                            currentBoard.time2 = 900 - (time.time() - currentBoard.startTime) - currentBoard.storedTime2
                    dumpedData = pickle.dumps(currentBoard)
                self.client.sendall(dumpedData)
            except Exception as e:
                print(e)
        gameNum -= 1
        try:
            del gameList[self.gameIndex]
        except:
            pass
        self.client.close()


if __name__ == '__main__':
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = "127.0.0.1"
    port = int(sys.argv[1])
    server_ip = socket.gethostbyname(server)
    try:
        serverSocket.bind((server, port))
    except socket.error as e:
        print(str(e))
    serverSocket.listen()
    gameNum = 0
    gameList = {0: Board(11, 11)}
    while True:
        if gameNum < 4:
            client, addr = serverSocket.accept()
            gameIndex = -1
            for game in gameList.keys():
                if gameList[game].ready == False:
                    gameIndex = game
            if gameIndex == -1:
                try:
                    gameIndex = list(gameList.keys())[-1] + 1
                    gameList[gameIndex] = Board(11, 11)
                except:
                    gameIndex = 0
                    gameList[gameIndex] = Board(11, 11)
            thread = client_thread(client, gameIndex)
            thread.start()



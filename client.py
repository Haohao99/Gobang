import socket
import sys
import pygame
import os
import time
import pickle


def choose(index):
    x = index[0]
    y = index[1]
    if boardSize[0] < x < boardSize[0] + boardSize[2]:
        if boardSize[1] < y < boardSize[1] + boardSize[3]:
            divX = x - boardSize[0]
            divY = y - boardSize[1]
            i = int(divX / (boardSize[2] / 11))
            j = int(divY / (boardSize[3] / 11))
            return i, j
    return -1, -1

def drawGame(screen, currentBoard, player1Time, player2Time, color, ready):
    screen.blit(board, (0, 0))
    currentBoard.draw(screen)
    textfont = pygame.font.SysFont("arial", 28)
    player1Name = textfont.render(currentBoard.player1 + "\'s Time Remaining: ", 1, (192, 192, 192))
    screen.blit(player1Name, (660, 110))
    player1t = textfont.render(str(int(player2Time))+" seconds", 1, (192, 192, 192))
    screen.blit(player1t, (680, 145))
    player2Name = textfont.render(currentBoard.plater2 + "\'s Time Remaining: ", 1, (192, 192, 192))
    screen.blit(player2Name, (660, 500))
    player2t = textfont.render(str(int(player1Time))+" seconds", 1, (192, 192, 192))
    screen.blit(player2t, (680, 535))
    if not ready:
        show = "Waiting..."
        textfont = pygame.font.SysFont("arial", 80)
        txt = textfont.render(show, 1, (255, 0, 0))
        screen.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    textfont = pygame.font.SysFont("arial", 30)
    if color == "b":
        turntxt = textfont.render("You are white", 1, (255, 0, 0))
        screen.blit(turntxt, (700, 300))
    else:
        turntxt = textfont.render("You are black", 1, (255, 0, 0))
        screen.blit(turntxt, (700, 300))
    if currentBoard.turn == color:
        turntxt = textfont.render("Your turn", 1, (255, 0, 0))
        screen.blit(turntxt, (730, 350))
    else:
        turntxt = textfont.render("His/Her turn", 1, (255, 0, 0))
        screen.blit(turntxt, (730, 350))
    pygame.display.update()


def end_screen(text):
    background_colour = (255, 255, 255)
    (width, height) = (1000, 675)
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text, 1, (255, 0, 0))
    screen.fill(background_colour)
    screen.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def send(client,data, pick=False):
    reply = None
    start_time = time.time()
    while time.time() - start_time < 5:
        try:
            if pick:
                client.send(pickle.dumps(data))
            else:
                client.send(str.encode(data))
            reply = client.recv(4096 * 8)
            try:
                reply = pickle.loads(reply)
                break
            except Exception as e:
                print(e)
        except socket.error as e:
            print(e)
    return reply

def main(name):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = int(sys.argv[1])
    addr = (host, port)
    client.connect(addr)
    chessBoard = client.recv(4096 * 8)
    chessBoard = pickle.loads(chessBoard)

    color = chessBoard.start_user
    count = 0

    chessBoard = send(client,"playerName " + name)

    clock = pygame.time.Clock()
    run = True

    while run:

        p1Time = chessBoard.time1
        p2Time = chessBoard.time2
        if count == 60:
            chessBoard = send(client,"get")
            count = 0
        else:
            count += 1
        clock.tick(30)

        try:
            drawGame(screen, chessBoard, p1Time, p2Time, color, chessBoard.ready)
        except Exception as e:
            print(e)
            break

        if p1Time <= 0:
            chessBoard = send(client,"B_win")
        elif p2Time <= 0:
            chessBoard = send(client,"W_win")

        if chessBoard.check_mate("b"):
            end_screen("White is the Winner!")
            chessBoard = send(client,"winner b")
            run = False
        elif chessBoard.check_mate("w"):
            end_screen("Black is the winner")
            chessBoard = send(client,"winner w")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                if color == chessBoard.turn and chessBoard.ready:
                    pos = pygame.mouse.get_pos()
                    i, j = choose(pos)
                    chessBoard = send(client,"choose " + str(i) + " " + str(j) + " " + color)
    client.close()


if __name__ == '__main__':
    pygame.font.init()
    board = pygame.transform.scale(pygame.image.load(os.path.join("img", "gobang_board.png")), (1000, 675))
    boardSize = (80, 80, 510, 510)
    width = 1000
    height = 675
    name = input("Please enter your name: ")
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Gobang")
    pygame.display.update()
    main(name)



import socket
import pickle
import random
import threading
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

clients = []
isRunning = True
snakes = []  # Snake connections
recvCount = 0
initPos = [9]
BUFFER = 1024

recvLock = threading.Lock()  # Threading Locks
snakeLock = threading.Lock()


def setIsRunningFlag():
    global isRunning
    isRunning = False


def snakeWins():
    with snakeLock:
        win = []

        for sn in snakes:
            if sn['ALIVE'] == 1:
                win.append(sn)

        if len(win) == 1:  # One snake dies, other is declared winner
            iid = win[0]['ID']
            snakes[iid]['WIN'] = 1
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Game Over!\n")
            print("Snake", iid, "won!\n")
            print("Thank you for playing! Server closing.")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        elif len(win) == 0:  # Head on collision where no one wins (no snakes left)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Game Over!\n")
            print("All snakes are dead! Nobody wins.\n")
            print("Thank you for playing! Server closing.")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        else:
            return 0
        return 0


def snakeLoss():
    body = []

    with snakeLock:
        for sn in snakes:
            body.append([sn['ID'], sn['IN_POS']])

        for head in body:
            for belly in body:
                if head[1][0] == belly[1][0] and head[0] != belly[0] and snakes[head[0]]['ALIVE'] == 1:  # Head on collision detection
                    hurt1 = belly[0]
                    hurt2 = head[0]
                    snakes[hurt1]['ALIVE'] = 0
                    snakes[hurt2]['ALIVE'] = 0

                    for cl in clients:  # Communicates dead snakes
                        try:
                            cl.send(pickle.dumps(snakes))
                        except:
                            pass
                    return 2

                elif head[1][0] in belly[1][1:] and head[0] != belly[0] and snakes[belly[0]]['ALIVE'] == 1:  # Collision detection
                    hurt = (belly[0])
                    # kill = head[0]
                    snakes[hurt]['ALIVE'] = 0
                    for cl in clients:
                        try:
                            cl.send(pickle.dumps(snakes))
                        except:
                            pass
                    return 0
    return 0


def updateData():
    global recvCount

    with recvLock:  # Adding players as they join
        recvCount += 1

        if recvCount == 2:  # Once two players have join, begin broadcasting
            for sn in snakes:
                if sn['IN_POS'][0] == sn['FOOD']:  # When snake eats the food
                    snakes[sn['ID']]['SCORE'] += 1  # Add here to lengthen snake (maybe)
                    food = [random.randint(1, 18), random.randint(1, 28)]  # Changing food location
                    for s in snakes:
                        iid = s['ID']
                        snakes[iid]['FOOD'] = food
                    break

            out = snakeLoss()
            snakeWins()  # Print winners

            if out == 0:  # If no ones dead
                for cl in clients:
                    try:
                        cl.send(pickle.dumps(snakes))
                    except:
                        pass
                recvCount = 0
                return

            elif out == 1:  # If one is dead
                recvCount = 0
                return

            elif out == 2:  # If both are dead
                recvCount = 0
                return
        return  # Threads haven't responded yet


def initSnake(snake, c):  # Snake initialization
    if snake['INIT'] == 1:  # Check if snake hasn't been initialized yet
        return

    else:
        global snakes
        with snakeLock:
            while True:
                r = random.randint(2, 18)  # Place snake in a random starting position
                if r not in initPos:
                    initPos.append(r)
                    break

            idx = len(snakes)
            snake['IN_POS'] = [[r, 10], [r, 9], [r, 8], [r, 7], [r, 6]]  # Snake variables
            snake['KEY'] = KEY_RIGHT
            snake['CHAR'] = str(idx)
            snake['ID'] = idx
            snake['INIT'] = 1
            snake['ALIVE'] = 1
            snake['FOOD'] = [initPos[0], 10]
            snakes.append(snake)  # Create data for client snakes
            c.send(pickle.dumps(idx))


def clientThreads(cl):  # Threading function
    clients.append(cl)

    while True:  # Receiving client data
        try:
            data = cl.recv(BUFFER)
            snake = pickle.loads(data)
        except:
            break

        initSnake(snake, cl)  # Initializes snake

        snake['IN_POS'].insert(0, [snake['IN_POS'][0][0] + (snake['KEY'] == KEY_DOWN and 1) + (  # Movements
                                     snake['KEY'] == KEY_UP and -1),
                                     snake['IN_POS'][0][1] + (snake['KEY'] == KEY_LEFT and -1) +
                                    (snake['KEY'] == KEY_RIGHT and 1)]
                                )

        print("Snake: ", snake['ID'], "Coordinate: ",
              snake['IN_POS'])  # Print snake coordinates (Sometimes it prints too fast and prints out of order)

        if snake['IN_POS'][0][0] == 0 or snake['IN_POS'][0][0] == 19 or snake['IN_POS'][0][1] == 0 or snake['IN_POS'][0][1] == 29:  # Border collision control
            snake['ALIVE'] = 0
            with snakeLock:
                try:
                    snakes[snake['ID']] = snake
                    cl.send(pickle.dumps(snakes))
                except:
                    pass

        with snakeLock:
            snakes[snake['ID']] = snake

        updateData()
        setIsRunningFlag()

    cl.close()  # Close connection


def runServer():
    players = 2  # Default server parameters
    host = '194.195.215.115'  # Linode server machine IP hardcoded
    port = 5000

    serversoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP Socket Server
    serversoc.bind((host, port))
    serversoc.listen(players)
    print("Listening on", port)

    playerCount = 0

    while isRunning:  # Accepts players as they join, ensures only 2 players are playing at a time
        commsoc, addr = serversoc.accept()
        print('Snake',playerCount, 'has joined the game.')
        playerCount = playerCount + 1
        t = threading.Thread(target=clientThreads, args=(commsoc,))  # Starting threads
        t.start()
    if not isRunning:  # Closes server once game is finished and results are returned
        serversoc.close()


if __name__ == '__main__':
    runServer()

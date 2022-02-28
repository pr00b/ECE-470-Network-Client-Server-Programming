import socket
import curses
import pickle
from curses import KEY_RIGHT

host = '194.195.215.115'  # Default server parameters with Linode server machine IP hardcoded
port = 5000
commsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP Client
commsoc.connect((host, port))

BUFFER = 1024  # Default buffer size
msg = ""  # Empty message

snake = {  # Host snake
    "IN_POS": [[0, 0]],
    "KEY": KEY_RIGHT,
    "ALIVE": 0,
    "WIN": 0,
    "SCORE": 0,
    "FOOD": [],
    "CHAR": '0',
    "INIT": 0,
    "ID": 0
        }

def gameLoop():
    global snake
    global msg
    
    curses.initscr() # Setting up game window with curses
    window = curses.newwin(20, 30, 0, 0)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)
    window.nodelay(1)

    set_id = True

    while True:
        window.addstr(0, 15, 'Score : ' + str(snake['SCORE']) + ' ')  # Game window
        window.addstr(0, 5, 'Snake ' + str(snake['ID']))

        window.timeout(200)  # Snake movement delay (default: 125, for demo: 200)

        prevKey = snake['KEY']  # Default key if no movements are made (snake moves to the right)
        event = window.getch()  # Getting key entries by users
        snake['KEY'] = snake['KEY'] if event == -1 else event

        toSend = pickle.dumps(snake)
        commsoc.send(toSend)

        if set_id:  # Sets up host snake
            iid = commsoc.recv(BUFFER)
            snake['ID'] = pickle.loads(iid)
            set_id = 0

        data = commsoc.recv(BUFFER)
        snakes = pickle.loads(data)
        snake = snakes[snake['ID']]

        if snake['ALIVE'] == 0:  # Loser message
            msg = "Loser!"
            break

        if snake['WIN'] == 1:  # Winner message
            msg = "Winner!"
            break

        if len(snake['FOOD']) > 0:  # Food placement
            window.addch(snake['FOOD'][0], snake['FOOD'][1], '*')

        for sn in snakes:  # Snake rendering
            if sn['ALIVE'] == 0:
                for x in sn['IN_POS']:
                    window.addch(x[0], x[1], ' ')
            else:
                last = sn['IN_POS'].pop()
                window.addch(last[0], last[1], ' ')
                window.addch(sn['IN_POS'][0][0], sn['IN_POS'][0][1], '#')

    curses.endwin()
    commsoc.close()

def printGameOver():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")  # Game stats once the game ends
    print("Game Over!\n")
    print(msg, "\n")
    print("Your score = " + str(snake['SCORE']), "\n")
    print("Thank you for playing!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

if __name__ == '__main__':
    gameLoop()
    printGameOver()

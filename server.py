#!/usr/bin/env python3

import sqlalchemy as sql
import game2048
import save
import signal
import socket
import sys
import colors as c
from socketserver import TCPServer, BaseRequestHandler, ThreadingMixIn

# IP (network interface) and port to listen on
# 0.0.0.0 means on any interface
IP = '0.0.0.0'
# PORT = 1337
PORT = 23

sqlEngine = sql.create_engine("sqlite:///database.sqlite")
sqlMetadata = sql.MetaData(sqlEngine)

class sqlTablesHolder():
    # concepts = sql.Table("concepts", sqlMetadata, sql.Column('id', sql.Integer, primary_key=True, nullable=False), sql.Column('message_id', sql.String(32)), sql.Column('channel_id', sql.String(32)), sql.Column('guild_id', sql.String(32)), sql.Column('title', sql.String(1024)), sql.Column('desc', sql.String(2048)), sql.Column('author_id', sql.String(32)), sql.Column('votes', sql.Integer), sql.Column('updated', sql.dialects.mysql.TINYINT(1), nullable=False, server_default="0"))
    pass

sqlTables = sqlTablesHolder()

sqlMetadata.create_all()

# Ctrl+C Handler
# Lets the program shut down gracefully (without throwing exception)
# when user hits Ctrl+C
def signal_handler(*_):
    print("\nCtrl+C")
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

# Sets TCP keepalive values on the socket, which is used to detect if
# the client disappears without sending a FIN or RST packet
def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """
    Source: https://stackoverflow.com/a/14855726/6423456
    Set TCP keepalive on an open socket.
    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

class MyRequestHandler(BaseRequestHandler):
    @staticmethod
    def parseEnvironOption(cmd):
        cmd = cmd[3:]
        key = []
        value = []
        current = None
        output = {}
        escaping = False
        for b in cmd:
            if escaping == True:
                if current == "k":
                    key.append(b)
                elif current == "v":
                    value.append(b)
                continue
            if b == 0 or b == 3:
                if current == "v":
                    output[bytearray(key).decode("utf-8","replace")] = bytearray(value).decode("utf-8","replace")
                    key = []
                    value = []
                current = "k"
            elif b == 1:
                if current == "k":
                    output[bytearray(key).decode("utf-8","replace")] = bytearray().decode("utf-8","replace")
                current = "v"
                value = []
            elif b == 2:
                escaping == True
            else:
                if current == "k":
                    key.append(b)
                elif current == "v":
                    value.append(b)
        output[bytearray(key).decode("utf-8","replace")] = bytearray(value).decode("utf-8","replace")
        key = []
        value = []
        return output

    def requestOptions(self):
        self.options["linemode"] = None
        self.request.sendall(b'\xff\xfd\x22') # IAC DO LINEMODE

        self.options["naws"] = None
        self.request.sendall(b'\xff\xfd\x1f') # IAC DO naws

        self.options["terminal-type"] = None
        self.request.sendall(b'\xff\xfd\x18') # IAC DO naws

        self.options["new-environ"] = None
        self.request.sendall(b'\xff\xfd\x27') # IAC DO NEW-ENVIRON


    def requestCharMode(self, state):
        self.charMode = state
        if self.options.get("linemode", None) == None:
            self.request.sendall(b'\xff\xfd\x22') # IAC DO LINEMODE
        elif self.options.get("linemode", 0) == True:
            if state:
                self.request.sendall(b'\xff\xfa\x22\x01\x02\xff\xf0')
            else:
                self.request.sendall(b'\xff\xfa\x22\x01\x03\xff\xf0')
        else:
            self.options["linemode"] = None
            self.request.sendall(b'\xff\xfd\x22') # IAC DO LINEMODE


    def handleTelnetCommands(self, data):
        commands = data.split(b'\xff') # IAC
        for cmd in commands:
            if len(cmd) < 1:
                continue
            if cmd[0] == 251: # WILL
                if len(cmd) < 2:
                    continue
                if cmd[1] == 34: # LINEMODE
                    if self.charMode:
                        self.request.sendall(b'\xff\xfa\x22\x01\x02\xff\xf0') # IAC SB LINEMODE MODE 2 IAC SE
                    else:
                        self.request.sendall(b'\xff\xfa\x22\x01\x03\xff\xf0') # IAC SB LINEMODE MODE 3 IAC SE
                    # print("%s entered character mode" % (self.client_address, ))
                    self.options["linemode"] = True
                elif cmd[1] == 31: # naws
                    self.options["naws"] = True
                elif cmd[1] == 24: # terminal-type
                    self.options["terminal-type"] = True
                    self.request.sendall(b'\xff\xfa\x18\x01\xff\xf0')
                elif cmd[1] == 0x27:
                    self.options["new-environ"] = True
                    self.request.sendall(b'\xff\xfa\x27\x01\xff\xf0') # IAC SB NEW-ENVIRON SEND IAC SE
                else:
                    self.request.sendall(b'\xff\xfe'+cmd[1:2]) # DON'T

            elif cmd[0] == 252: # WON'T
                if len(cmd) < 2:
                    continue
                if cmd[1] == 34: # LINEMODE
                    # print("%s refused character mode" % (self.client_address, ))
                    self.options["linemode"] = False
                elif cmd[1] == 31: # naws
                    self.options["naws"] = False
                elif cmd[1] == 24: # terminal-type
                    self.options["terminal-type"] = False
                elif cmd[1] == 39: # new-environ
                    self.options["new-environ"] = False
                else:
                    self.request.sendall(b'\xff\xfe'+cmd[1:2]) # DON'T
            elif cmd[0] == 253: # DO
                if len(cmd) < 2:
                    continue
                if cmd[1] == 31: # naws
                    self.options["naws"] = True
                    self.request.sendall(b'\xff\xfb'+cmd[1:2]) # WILL
                else:
                    self.request.sendall(b'\xff\xfc'+cmd[1:2]) # WON'T

            elif cmd[0] == 253: # DON'T
                if len(cmd) < 2:
                    continue
                if cmd[1] == 31: # naws
                    self.options["naws"] = False
                    self.request.sendall(b'\xff\xfb'+cmd[1:2]) # WILL
                else:
                    self.request.sendall(b'\xff\xfc'+cmd[1:2]) # WON'T

            elif cmd[0] == 250: # Sub-negotiation
                if len(cmd) < 2:
                    continue
                if cmd[1] == 31: # naws
                    if len(cmd) < 6:
                        continue
                    self.terminal["width"] = int(cmd[2:4].hex(), 16)
                    self.terminal["height"] = int(cmd[4:6].hex(), 16)
                    print("%s sent terminal size: %s LINES, %s ROWS" % (self.client_address,self.terminal["height"], self.terminal["width"] ))
                elif cmd[1] == 24: # terminal-type
                    if len(cmd) < 3:
                        continue
                    if cmd[2] == 0:
                        print("%s sent terminal-type: %s" % (self.client_address, cmd[3:].decode("utf-8", "ignore")))
                        self.terminal["type"] = cmd[3:].decode("utf-8", "ignore")
                        # self.request.sendall(b'\xff\xfa\x18\x01\xff\xf0')
                elif cmd[1] == 39: # new-ENVIRON
                    if len(cmd) < 6:
                        continue
                    if cmd[2] == 0 or cmd[2] == 2:

                        self.environ.update(self.parseEnvironOption(cmd))
                        print("%s sent environmental data: %s" % (self.client_address, self.environ))

            elif cmd[0] == 244: # Interrupt Process
                print("%s closed telnet" % (self.client_address, ))
                return False
        return True

    def write(self, text):
        self.request.sendall(text.replace("\n", "\r\n").encode())

    def clear(self):
        some_str = "1b5b481b5b4a"
        self.request.sendall(bytes.fromhex(some_str))

    def handle(self):
        self.sqlConn = sqlEngine.connect()
        self.environ = {}
        self.options = {
        }
        self.charMode = True
        self.terminal = {"width": 80, "height": 24}
        self.status = {
            "menu": True
        }

        print("%s connected" % (self.client_address,))

        self.requestOptions()
        # self.requestCharMode(False)
        # self.clear()

        # self.clear()
        # menu = f"\x1b\x5b\x48\x1b\x5b\x4a\n\n{c.FG_GREEN}Welcome to the minigame HUB! Pick one game by pressing \nthe according number on your keyboard{c.RESET}\n\n\n [1] The 2048 game\n\n [q] Quit\n\n "
        menu = f"\n\n{c.FG_GREEN}Welcome to the minigame HUB! Pick one game by pressing \nthe according number on your keyboard{c.RESET}\n\n\n [1] The 2048 game\n\n [q] Quit\n\n "
        self.write(menu)
        # self.request.sendall(f"{c.BOLD}{c.UNDERLINED}{c.FG_RED}{c.BG_YELLOW} Yes it is awful {c.RESET}, {self.client_address}\n".encode())
        # self.request.sendall(("%s%s%s%s Yes it is awful %s, {0}\n".format(self.client_address) % (c.BOLD, c.UNDERLINED, c.FG_RED, c.BG_YELLOW, c.RESET)).encode())

        while True:
            # Listen for data from client
            try:
                data = self.request.recv(2**13)
            except TimeoutError:
                print("%s timed out" % (self.client_address, ))
                break
            except ConnectionResetError:
                print("%s reset connection" % (self.client_addrss))

            if not self.handleTelnetCommands(data):
                break


            # Turn the data into unicode, so it can be compared to regular
            # python strings, which in python3 are unicode by default
            # Note that at this point, if data is '', client disconnected,
            # but if client just hit enter (didn't enter anything), it's
            # \n or \n\r.
            byteData = False
            rawData = data
            try:
                data = data.decode("utf-8", "strict")
            except:
                byteData = True
                pass

            if not byteData:
                if self.status.get("menu") == True:
                    if data.rstrip() == "1":
                        self.status["2048"] = {
                            "state" : True,
                            "game": game2048.create_game(),
                            "points": 0,
                            "newpoints": 0,
                            "quit": False,
                            "firstFrame": True
                        }
                        self.status["menu"] = False
                    elif data.rstrip() == "q" :
                        self.write("Bye!\n")
                        print("%s disconnected from the menu" % (self.client_address, ))
                        break
                    else:
                        self.write(menu)
                if self.status.get("2048", {"state": False}).get("state") == True:
                    data = data.rstrip()
                    game = self.status["2048"]["game"]
                    point = 0
                    quitScreen = self.status["2048"]["quit"]
                    points = self.status["2048"]["points"]
                    over, win = game2048.is_over(game)
                    if not over and not win:
                        if data == 'w' or data == '\x1b[A':
                            game, _, point = game2048.move_up(game)
                        elif data == 's' or data == '\x1b[B':
                            game, _, point = game2048.move_down(game)
                        elif data == 'a' or data == '\x1b[D':
                            game, _, point = game2048.move_left(game)
                        elif data == 'd' or data == '\x1b[C':
                            game, _, point = game2048.move_right(game)
                        elif data == 'q' or data == '\x03':
                            quitScreen = True
                        else:
                            pass
                        points += point
                        self.status["2048"]["game"] = game
                        self.status["2048"]["newpoints"] = point
                        self.status["2048"]["points"] = points
                        self.status["2048"]["quit"] = quitScreen

                        self.write(game2048.render_screen(  game,
                                                            self.terminal["height"],
                                                            self.terminal["width"],
                                                            self.status["2048"]["points"],
                                                            self.status["2048"]["newpoints"],
                                                            "",
                                                            self.status["2048"]["quit"],
                                                            self.status["2048"]["firstFrame"]))
                        self.status["2048"]["firstFrame"] = False
                    elif over or win:
                        if data == "\r\x00" or data == "\r\n":
                            self.status["2048"] = {"state": False}
                            self.status["menu"] = True
                            self.write(menu)
                        else:
                            self.write(game2048.render_screen(  game,
                                                                self.terminal["height"],
                                                                self.terminal["width"],
                                                                self.status["2048"]["points"],
                                                                self.status["2048"]["newpoints"],
                                                                "",
                                                                self.status["2048"]["quit"],
                                                                False))


            # Check if we didn't get any data (client disconnected), or if
            # client typed "exit", requesting to disconnect
            if not byteData:
                if not data or data.rstrip() == "exit" or data.rstrip() == "quit" or data.rstrip() == "\x03":
                    print("%s disconnected gracefully" % (self.client_address, ))
                    break

                # Print the actual data the client sent us, without the
                # trailing newline and optional carriage return (Windows)
            print("%s: %s" % (self.client_address, rawData))

class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    # Exit the threads when main thread dies
    daemon_threads = True

    # When the program exits, sometimes threads were left behind that
    # would continue to listen to the port for a few more seconds. If
    # you tried to run this program again before those exit, you'd get an
    # error that the port was busy. This fixes that.
    TCPServer.allow_reuse_address = True

# Note: using a context manager on TCPServer wasn't supported until Python3.6
# Before that, use server_close()
# with ThreadingTCPServer((IP, PORT), MyRequestHandler) as server:
server = ThreadingTCPServer((IP, PORT), MyRequestHandler)
print("Listening on %s" % (server.server_address,))

# Set tcp keepalive values
set_keepalive_linux(server.socket)

# Run the server
server.serve_forever()
server.server_close()

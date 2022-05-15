import socket
import time
from threading import Thread


class ChatReader(Thread):
    server = "irc.chat.twitch.tv"
    port = 6667
    nick = "fettarmqp"
    secret = ""
    channel = "#fettarmqp"
    sock = socket.socket()
    running = True
    player = {}
    player_in = []

    def __init__(self, channel, nick, secret, player, player_in):
        # Call the Thread class's init function
        Thread.__init__(self)
        self.channel = "#" + channel
        self.nick = nick
        self.secret = secret
        self.running = True
        self.player = player
        self.player_in = player_in
        self.sock = socket.socket()
        self.connect()

    def connect(self):

        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.secret}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nick}\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))


    def run(self):

        self.sock.send(f"PRIVMSG {self.channel} :-----Poll Started-----\n".encode('utf-8'))
        for temp_player in self.player:
            if int(temp_player["vote_number"]) in self.player_in:
                self.sock.send(f"PRIVMSG {self.channel} :Type {temp_player['DisplayName']}, {temp_player['twitch_name']} to Kick\n".encode('utf-8'))

        while self.running:
            try:
                data = self.sock.recv(1024).decode('utf-8')
            except ConnectionAbortedError:
                continue
            if not data:
                break

            if data.startswith("PING"):
                self.sock.send(f"PONG :tmi.twitch.tv\n".encode('utf-8'))
            elif "PRIVMSG" in data:
                chatter = data[1:].split("!")[0]
                message = str(data[1:].split("PRIVMSG " + self.channel + " :")[1].replace("\n", "").replace("\r", ""))
                not_voted_til_jet = True
                prev_vote = None
                is_chatter_player = False
                index_of_player_and_chatter = None
                for i in range(len(self.player)):
                    if chatter in self.player[i]["votes"]:
                        not_voted_til_jet = False
                        prev_vote = i
                        break
                    if chatter == self.player[i]["twitch_name"]:
                        if int(self.player[i]["vote_number"]) in self.player_in:
                            is_chatter_player = True
                            index_of_player_and_chatter = i
                            break

                for temp_player in self.player:
                    if temp_player["DisplayName"] == message or temp_player["vote_number"] == message or temp_player["twitch_name"] == message:

                        if int(temp_player["vote_number"]) in self.player_in:
                            if not_voted_til_jet:
                                if is_chatter_player:
                                    self.player[index_of_player_and_chatter]["pick"] = temp_player["vote_number"]
                                else:
                                    temp_player["votes"].append(chatter)
                                    break
                            else:
                                if is_chatter_player:
                                    self.player[index_of_player_and_chatter]["pick"] = temp_player["vote_number"]
                                else:
                                    temp_player["votes"].append(chatter)
                                    self.player[prev_vote]["votes"].remove(chatter)

            else:
                print(data)

    def kill(self):
        self.running = False
        time.sleep(1)
        self.sock.send(f"PRIVMSG {self.channel} :----- POLL ENDET -----\n".encode('utf-8'))
        self.sock.close()


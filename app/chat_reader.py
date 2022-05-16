import socket
import time
from threading import Thread
from twitchio.ext import commands
import asyncio
from time import sleep
class ChatReader2(commands.Bot):

    server = "irc.chat.twitch.tv"
    port = 6667
    nick = "fettarmqp"
    secret = ""
    channel = "#fettarmqp"
    running = True
    player = {}
    player_in = []

    def __init__(self, channel, nick, secret, player, player_in):

        asyncio.set_event_loop(asyncio.new_event_loop())

        super().__init__(token=secret, prefix='?', initial_channels=[self.channel])
        # Call the Thread class's init function
        self.channel = "#" + channel
        self.nick = nick
        self.secret = secret
        self.running = False
        self.player = player
        self.player_in = player_in
        self.chat_votes = dict()

        self.mapping_number_to_player = {self.player[x]["vote_number"] : player[x]["twitch_name"] for x in range(len(self.player))}
        self.mapping_player_to_number = {self.player[x]["twitch_name"] : player[x]["vote_number"] for x in range(len(self.player))}


        


    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

        self.channel_hook = self.connected_channels[0]
        await self.run2()

    async def run2(self):
        await self.channel_hook.send(f"-----Poll Started-----\n")
        for temp_player in self.player:
            if int(temp_player["vote_number"]) in self.player_in:
                await self.channel_hook.send(f"Type {temp_player['DisplayName']}, {temp_player['twitch_name']} to Kick\n")

        self.running = True

       
    def kill(self):
        self.running = False
        
            

    async def event_message(self, ctx):
        if not self.running:
            return

        if ctx.content is None:
            return

        if ctx.author is None:
            return



        chatter = ctx.author.name
        message = ctx.content

        
        # check if message is a valid vote

        ## valid is username 
        valid = False
        if message.lower() in [self.player[x]["twitch_name"] for x in range(len(self.player))]:
            valid = True
            voted_player = message.lower()
            voted_number = self.mapping_player_to_number[voted_player]

        ## valid if int 
        if message in [self.player[x]["vote_number"] for x in range(len(self.player))]:
            valid = True
            voted_number = message
            voted_player = self.mapping_number_to_player[voted_number]

        if not valid:
            return



        self.chat_votes[chatter.lower()] = voted_player

        # valid vote found, update stats
        if chatter.lower() in [self.player[x]["twitch_name"] for x in range(len(self.player))]:
            # case: player voted against another player
            for i in range(len(self.player)):
                if(self.player[i]["twitch_name"] == chatter.lower()):
                    self.player[i]["pick"] = voted_number

        else:
            # it was a chat vote because chatter is not in players list
            # go over whole votes and assign to the player 

            temp_dict = {self.player[x]["twitch_name"] : 0 for x in range(len(self.player))}

            for val in self.chat_votes.values():
                try:
                    voted_person = self.mapping_number_to_player[val]
                except:
                    voted_person = val.lower()

                temp_dict[voted_person] += 1

            # reassign to original dict

            for i in range(len(self.player)):
                self.player[i]["votes"] = temp_dict[self.player[i]["twitch_name"]]

            
















   


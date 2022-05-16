import os

from flask import render_template, jsonify, request

import app
from app.chat_reader import ChatReader2

player = [
    {"DisplayName": "FettarmQP", "twitch_name": "fettarmqp", "vote_number": "0", "votes": 0, "cam_url": "https://vdo.ninja/?view=ymZU5Ac", "pick": ""},
    {"DisplayName": "Ede", "twitch_name": "sauerteigpizza", "vote_number": "1", "votes": 0, "cam_url": "https://vdo.ninja/?view=LDXUpTf", "pick": ""},
    {"DisplayName": "Tux", "twitch_name": "tuxmania", "vote_number": "2", "votes": 0, "cam_url": "https://vdo.ninja/?view=pSwLsG5", "pick": ""},
    {"DisplayName": "Ganzling", "twitch_name": "ganzling", "vote_number": "3", "votes": 0, "cam_url": "https://vdo.ninja/?view=7rAwuXK", "pick": ""},
    {"DisplayName": "Fall1ngTV", "twitch_name": "fall1ngtv", "vote_number": "4", "votes": 0, "cam_url": "https://vdo.ninja/?view=bQ9FKQd", "pick": ""}
]

# dead player not voteable

host = {"DisplayName": "Pydracor", "twitch_name": "Pydracor", "cam_url": "https://vdo.ninja/?view=WeVbH7G"}

started = False

player_lifes = 3


@app.app.route('/')
def index():
    return render_template('control.html', player_list=player, host=host, countdown_sec=0, countdown_min=3, player_lifes=player_lifes)


@app.app.route('/twitch_reader')
def read_chat():
    if started:
        print(started)
    votes = [0] * len(player)
    for temp_player in player:
        if temp_player["pick"] != "":
            votes[int(temp_player["pick"])] = votes[int(temp_player["pick"])] + 1

    max_chat_votes_value = 0
    max_chat_votes_index = []
    for i in range(len(player)):
        if (player[i]["votes"]) > max_chat_votes_value:
            max_chat_votes_value = (player[i]["votes"])
            max_chat_votes_index = [i]
        elif (player[i]["votes"]) == max_chat_votes_value:
            max_chat_votes_index.append(i)

    if max_chat_votes_value == 0:
        max_chat_votes_index = []

    in_danger_value = 0
    in_danger_index = []
    for i in range(len(player)):
        plus_value = 0
        if i in max_chat_votes_index:
            plus_value = 1
        if votes[i] + plus_value > in_danger_value:
            in_danger_value = votes[i] + plus_value
            in_danger_index = [i]
        elif votes[i] + plus_value == in_danger_value:
            in_danger_index.append(i)

    if in_danger_value == 0:
        in_danger_index = []

    return render_template('chat_ergs.html', player_list=player, votes=votes, index_of_max=max_chat_votes_index, in_danger=in_danger_index)


@app.app.route("/poll/start", methods=['POST'])
def start_read_chat():
    content = request.json
    #app.bot = ChatReader2(os.environ.get("CHANEL"), os.environ.get("NICKNAME"), os.environ.get("TOKEN"), player, content["player_list"])
    for temp_player in player:
        temp_player["pick"] = ""
        temp_player["votes"] = 0

    
    app.bot = ChatReader2("#tuxmania", "tuxmania", "oauth:9lf9s03zpclk0t550f6hhl858ibbhb", player, content["player_list"])
    app.bot.run()

    

    return "started Reading Chat"


@app.app.route("/poll/stop", methods=['POST'])
def stop_read_chat():
    app.bot.kill()



    return "stopped Reading Chat"


@app.app.route("/poll/reset", methods=['POST'])
def restart_read_chat():
    for temp_player in player:
        temp_player["pick"] = ""
        temp_player["votes"] = 0
    return "Resettet Poll"


@app.app.route("/get_chat_results")
def get_chat_results():
    erg_list = []
    for temp_player in player:
        erg_list.append(temp_player["votes"])
    return jsonify(erg_list)


@app.app.route("/get_player_results")
def get_player_results():
    erg_list = []
    for temp_player in player:
        if temp_player["pick"] == "":
            erg_list.append("")
        else:
            print(temp_player["pick"])
            erg_list.append(player[int(temp_player["pick"])]["DisplayName"])
    return jsonify(erg_list)


@app.app.route("/get_danger_player")
def get_danger_player():
    erg_list = [0] * len(player)
    for temp_player in player:
        print(temp_player["pick"])
        if temp_player["pick"] != "":
            print(player[int(temp_player["pick"])]["pick"])
            erg_list[int(temp_player["pick"])] = erg_list[int(temp_player["pick"])]+1
    erg_list2 = []
    for temp_player in player:
        erg_list2.append(len(temp_player["votes"]))
    max_entry = max(erg_list2)
    if max_entry != 0:
        for i in range(len(erg_list2)):
            if max_entry == erg_list2[i]:
                erg_list[i] = erg_list[i] + 1

    return jsonify(erg_list)

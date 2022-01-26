import os
import json
from flask import (
    Flask, render_template, request, session, redirect, url_for
    )
from flask_login import (
    LoginManager, login_user, logout_user, current_user
    )
# Set up the required variables needed
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"

fields = ["console", "series", "game_name", "classic", "quantity", "status"]
consoles = ["3DS", "DS", "NES-P", "NES-U", "SNES", "Nintendo 64", "Game Cube", "Game Boy", "Xbox", "Xbox 360", "Xbox One", "Nintendo Switch", "PSP", "PlayStation", "PlayStation 2", "PlayStation 3", "PlayStation 4", "Wii", "Wii U", "Sega MS", "Sega MD"]
field_cap = [20, 52, 0, 52, 6, 2, 2]


@app.route("/")
def index():
    list_data = list_game("name", "")
    return render_template("index.html", list_data=(list_data))


@app.route("/random")
def random():
    list_data = random_obj(10, 0)
    return render_template("random.html", list_data=(list_data))


@app.route("/random_item", methods=["POST"])
def random_game(x, status=0):
    x = request.form.get("Random")

    if x is None:
        x = 10
    
    list_data = random_obj(x, 0)
    return render_template("random.html", list_data=(list_data))


def random_obj():
    json_list = json.load(open("data/game_log.json", "r+"))
    temp_list = []
    for n in range(0, x):
        while x > 0:
            r = random.randint(0, len(json_list)-1)
            if status > 0 and json_list[str(r)]["status"] == status:
                temp_list.append([json_list[str(r)]["console"], json_list[str(r)]["game_name"]])
                x = x-1
            elif status == 0:
                temp_list.append([json_list[str(r)]["console"], json_list[str(r)]["game_name"]])
                x = x-1
    temp_list.insert(0, ["Game Name", "Console"])
    return temp_list


@app.route("/edit")
def edit():
    list_data = list_game("name", "")
    return render_template("edit_item.html", list_data=(list_data))


@app.route("/edit_item", methods=["POST"])
def edit_item():
    item = request.form.get("Item")
    list_data = list_game("name", item)


@app.route("/Q", methods=["POST"])
def search():
    contains = request.form.get("Search")
    field = request.form.get("Field")
    if contains is None:
        contains = ""
    list_data = list_game(field, contains)
    return render_template("index.html", list_data=(list_data), fields=(fields))


def list_game(field="", contains="", reverse=False, file="game_log.json"):
    json_list = json.load(open("data/"+file, "r+"))
    temp_list = []

    for i in range(0, len(fields)):
        if field in fields[i]:
            field = fields[i]
    altered = False
    for i in range(0, len(json_list)):
        item = []
        try:
            if field in json_list[str(i)] and contains.lower() in json_list[str(i)][field].lower():
                altered = True
            else:
                altered = False
        except:
            if field in json_list[str(i)] and str(contains) == str(json_list[str(i)][field]):
                altered = True
            else:
                altered = False
        if altered:
            item.append(str(json_list[str(i)][field]))
            for j in range(0, len(fields)):
                if field != fields[j] and fields[j] in json_list[str(i)]:
                    item.append(str(json_list[str(i)][fields[j]]))
            temp_list.append(item)

    temp_list.sort(reverse=bool(reverse))
    if len(temp_list) > 0:
        if field in "game_name":
            temp_list.insert(0, ["Game Name", "Console", "Series", "Classic", "Quantity", "Status"])
        elif field in "console":
            temp_list.insert(0, ["Console", "Series", "Game Name", "Classic", "Quantity", "Status"])
        elif field in "status":
            temp_list.insert(0, ["Status", "Console", "Series", "Game Name", "Classic", "Quantity"])
        elif field in "quantity":
            temp_list.insert(0, ["Quantity", "Console", "Series", "Game Name", "Classic", "Status"])
        elif field in "series":
            temp_list.insert(0, ["Series", "Console", "Game Name", "Classic", "Quantity", "Status"])
    else:
        temp_list.insert(len(temp_list), "The entry you have given cannot find any result.")
    return temp_list

if __name__ == "__main__":
    # Main function which sets up the app and .run variables/condit
    app.run(
        host=os.environ.get(
            "IP", "0.0.0.0"), port=int(
                os.environ.get(
                    "PORT", "5000")), debug=True)
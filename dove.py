import sys
import os
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich import box

USER = os.getlogin()
FILE = "/nfs/sgoinfre/goinfre/Perso/who.cache"

console = Console()

search = ""
if len(sys.argv) == 2:
    if sys.argv[1] == "h":
        print("0 - Wakanda")
        print("1 - Nidavellir")
        print("[search] - Search user")
    elif sys.argv[1] != "0" or sys.argv[1] != "1":
        search = sys.argv[1]


def positions():
    c1 = []
    for r in range(6, 0, -1):
        for p in range(1, 13):
            c1.append(f"c1r{r}p{p}")
    c2 = []
    for r in range(1, 7):
        for p in range(13, 0, -1):
            c2.append(f"c2r{r}p{p}")
    positions = {}
    positions[0] = c1
    positions[1] = c2
    return positions


def get_users():
    with open(FILE) as f:
        user = {}
        for i, line in enumerate(f.readlines()):
            user[i] = {}
            user[i]["login"] = line.split(" - ")[0].strip()
            user[i]["location"] = line.split(" - ")[1].strip()
        return user


def get_user(users, location):
    for i in users:
        if users[i]["location"] == location:
            return users[i]
    return None


users = get_users()

rooms = {
    0: {"name": "🐾 Wakanda 🐾", "width": 180, "online": 0},
    1: {"name": "⛰️  Nidavellir ⛰️", "width": 195, "online": 0},
}


def print_room(room):
    r = positions()[room]
    pos_room = []
    for location in r:
        border_color = "gray23"
        login = ""
        pos = location.split("p")[1]

        if (room == 0 and pos == "7") or (room == 1 and (pos == "3" or pos == "8")):
            pos_room.append(Panel("", width=5, box=box.MINIMAL))
        user = get_user(users, location)
        if user:
            login = user["login"]
            if login == USER:
                border_color = "dodger_blue1"
                login = "[dodger_blue1]SONO QUI[/dodger_blue1]"
            else:
                border_color = "white" if search != login else "bright_green"
                login = login.replace(search, f"[bright_green]{search}[/bright_green]")
            rooms[room]["online"] += 1
        pos_room.append(
            Panel(
                f"[white]{login}",
                title=f"{location}",
                border_style=border_color,
            )
        )
    if room == 0:
        for entrance in range(1, 14):
            arrow = "" if entrance != 7 else "⬆️"
            pos_room.append(Panel(arrow, width=5, box=box.MINIMAL))
    if room == 1:
        for entrance in range(1, 15):
            arrow = "" if entrance != 14 else "⬅️"
            pos_room.append(Panel(arrow, box=box.MINIMAL))
    console.print(
        Panel(
            Columns(pos_room),
            title=rooms[room]["name"],
            width=rooms[room]["width"],
            border_style="white",
            padding=(1, 0, 1, 0),
            subtitle=f"{rooms[room]['online']} 👤 / {len(r)} 🖥️ ",
            subtitle_align="right",
        )
    )


if len(sys.argv) == 2:
    if sys.argv[1] == "0" or sys.argv[1] == "1":
        print_room(int(sys.argv[1]))
    else:
        print_room(0)
        print_room(1)
else:
    print_room(0)
    print_room(1)

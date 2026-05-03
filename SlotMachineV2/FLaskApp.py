# Imports
import json
import os
from flask import Flask, render_template, session, request, redirect, url_for, flash
from SlotMachineV2 import SlotMachine
import time
app = Flask(__name__)
app.secret_key = "HysHys"
USER_FILE = "users.json"
game = SlotMachine()

# Getting users dict from file
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Saving users file with updated dict
def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

# Getting user info from users dict, balance default 100 if not found
def get_user(username):
    users = load_users()
    return users.get(username, {"balance": 100})

# Saving the users balance to dict
def save_user_balance(username, balance):
    users = load_users()
    users[username] = {"balance": balance}
    save_users(users)

# Getting current users game stats
# Grid default set to empty boxes
# payout default 0
# balance default 100
def get_game_state():
    bet_index = session.get("bet_index", 0)
    bet = game.get_bet(bet_index)

    return {
        "username": session.get("username"),
        "grid": session.get("grid", [["🔳", "🔳", "🔳"], ["🔳", "🔳", "🔳"], ["🔳", "🔳", "🔳"]]),
        "payout": session.get("payout", 0),
        "balance": session.get("balance", 100),
        "bet_index": bet_index,
        "bet": bet,
        "winning_lines": session.get("winning_lines", [])
    }

# Checks before every request is the user logged in, redirected to login page if not
@app.before_request
def require_login():
    if request.endpoint not in ("static", "login") and "username" not in session:
        return redirect(url_for("login"))

# Login page, if user already logged in, redirected to index
# Otherwise, getting users info from page and setting it in session
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "username" in session:
            return redirect(url_for("index"))
        return render_template("login.html")
    username = request.form["username"]
    user = get_user(username)
    flash(f" Welcome {username}!")
    session["username"] = username
    session["balance"] = user["balance"]
    return redirect(url_for("index"))

# Gets game state, sends all info to index.html
@app.route("/")
def index():
    game_state = get_game_state()
    symbol_odds = zip(game.symbols, game.odds)
    return render_template(
        "index.html",
        grid=game_state["grid"],
        payout=game_state["payout"],
        balance=game_state["balance"],
        bet=game_state["bet"],
        payouts=game.payouts,
        symbol_odds=symbol_odds,
        winning_lines=game_state["winning_lines"],
    )

# Checking for insufficient funds, spins the slotmachine, updates grid of emojis, payout and balance to session
@app.route("/spin")
def spin():
    game_state = get_game_state()

    balance = game_state["balance"]
    bet_index = game_state["bet_index"]
    bet = game_state["bet"]

    if bet > balance:
        flash("Insufficient funds", "warning")
        return redirect(url_for("index"))

    grid= game.spin()
    payout, winning_lines = game.check_wins(grid, bet)

    balance = balance - bet + payout

    session["balance"] = balance
    session["bet_index"] = bet_index
    session["grid"] = grid
    session["payout"] = payout
    session["winning_lines"] = winning_lines

    return redirect(url_for("index"))

# Lowers the bet, updates it to session. lower.bet funct checks if already at min bet
@app.route("/lower")
def lower_bet():
    game_state = get_game_state()
    new_bet_index = game.lower_bet(game_state["bet_index"])
    session["bet_index"] = new_bet_index
    return redirect(url_for("index"))

# Raises the bet, updates it to session. raise.bet funct checks if already at max bet
@app.route("/raise")
def raise_bet():
    game_state = get_game_state()
    new_bet_index = game.raise_bet(game_state["bet_index"])
    session["bet_index"] = new_bet_index
    return redirect(url_for("index"))

# Allows the user to deposit more funds into their account
@app.route("/deposit", methods=["POST"])
def deposit():
    game_state = get_game_state()
    balance = game_state["balance"]
    try:
        amount = int(request.form["deposit"])
    except ValueError:
        flash("Invalid amount", "warning")
        return redirect(url_for("index"))
    balance += amount
    session["balance"] = balance
    return redirect(url_for("index"))

# Logs out the user, saves balance, clears session
@app.route("/logout")
def logout():
    username = session.get("username")
    if username:
        save_user_balance(username, session.get("balance", 0))
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
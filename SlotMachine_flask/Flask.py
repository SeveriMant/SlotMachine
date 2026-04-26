from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, request, flash
from SlotMachine import SlotMachine


app = Flask(__name__)
app.secret_key = "HysHys"

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped_view

def get_game():
    game = SlotMachine()
    game.saldo = session["user"]["saldo"]
    game.bet_index = session["user"]["bet_index"]
    return game

def save_game(game):
    session["user"] = {
        "saldo": game.saldo,
        "bet_index": game.bet_index
    }

@app.route("/")
@login_required
def index():
    game = get_game()
    return render_template("index.html", saldo=game.saldo, bet=game.get_bet())

@app.route("/spin")
@login_required
def spin():
    game = get_game()
    result = game.spin()
    save_game(game)
    return render_template("index.html", **result, bet=game.get_bet())

@app.route("/raise")
@login_required
def raise_bet():
    game = get_game()
    game.raise_bet()
    save_game(game)
    return redirect(url_for("index"))

@app.route("/lower")
@login_required
def lower_bet():
    game = get_game()
    game.lower_bet()
    save_game(game)
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user" in session:
            flash("You are already logged in", "information")
            return redirect(url_for("index"))
        else:
            return render_template("login.html")
    else:
        flash("Successfully logged in", "information")
        session["user"] = {"un": request.form.get("un"),
                           "saldo": 100,
                           "bet_index": 0}

        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You are logged out", "information")
    return redirect(url_for("index"))

@app.route("/deposit", methods=["POST"])
@login_required
def deposit():
    amount = request.form.get("amount")
    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return redirect(url_for("index"))
    game = get_game()
    game.saldo += amount
    save_game(game)
    return redirect(url_for("index"))
    

if __name__ == "__main__":
    app.run(debug=True)


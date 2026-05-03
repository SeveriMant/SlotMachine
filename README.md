# Flask Slot Machine

A simple web-based slot machine game built with **Python** and **Flask**.  
Players can log in, spin a 3x3 slot machine, change their bet, and deposit more funds.

---

## Features

- User system
- Session-based game state
- 3x3 slot machine grid
- Emoji-based symbols
- Weighted symbol odss
- Bet raising and lowering
- Simple auto-spin function
- Deposit system
- Winning row and diagonal function
- Winning cells are highlighted
- Users balance is saved in "users.json" after logging out
- Simple HTML/CSS frontend

---

## Tech Stack

- Python
- Flask
- HTML
- CSS
- Jinja templates
- JSON file storage

---

## How the game works
The slotmachine generates a 3x3 grid of symbols
Each symbol has different odds and payout values

---

## Payouts
Winning combinations are:
- Three matching symbols in a row
- Three matching symbols diagonally

Rows are worth 1.5x and diagonals are worth 2.0x

Final payout is calculated using:
- symbol payout value x line multiplier x bet

---

## Betting
User can choose from these bet options:
1, 2, 5, 10, 15, 20


## Login and Balance saving
Users login using a username and password
Password is currently not checked
When user logs out, their balance is saved into users.json

When user logs back in, with same username, their balance is loaded from users.json file

New users start with a default balance of 100$


## Routes
- /login   | Shows login page, and logs user in
- /        | Shows the main page with slotmachine, balance, bet, and symbol payouts
- /spin    | Spins the slot machine
- /raise   | Raises current bet
- /lower   | Lowers current bet
- /deposit | Adds money to the current user's balance
- /logout  | Saves balance to users.json file and logs user out


## Possible future ideas
- Real password checking
- Sign-up page
- Add sound effects
- Add animations

import random, time

class SlotMachine:
    def __init__(self):
        self.saldo = 100
        self.bets = [5, 10, 20, 50]
        self.bet_index = 0
        self.emojis = ["🍇", "🍉", "🍋"]


    def get_bet(self):
        return self.bets[self.bet_index]

    def spin(self):
        bet = self.get_bet()

        if self.saldo < bet:
            return {"error": "Insufficient funds"}

        self.saldo -= bet
        results = [random.choice(self.emojis) for _ in range(3)]

        a, b, c = results

        if a == b == c:
            win = bet * 3
        elif a == b or b == c:
            win = bet * 1.5
        else:
            win = 0

        self.saldo += win

        return {
            "results": results,
            "win": win,
            "saldo": self.saldo
        }

    def lower_bet(self):
        if self.bet_index > 0:
            self.bet_index -= 1
        else:
            return "Already at minimum bet"

    def raise_bet(self):
        if self.bet_index < len(self.bets) - 1:
            self.bet_index += 1
        else:
            return "Already at maximum bet"




peli = SlotMachine()

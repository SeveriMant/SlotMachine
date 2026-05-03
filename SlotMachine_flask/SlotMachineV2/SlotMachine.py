import random

class SlotMachine:
# Payouts for each symbol
    payouts = {
        "🍒": 1,
        "🍋": 1.5,
        "🔔": 3,
        "⭐": 5,
        "💎": 20
    }

# Odds for each symbol, more valuable symbols have lower odds
    odds = [40, 30, 15, 10, 5]

 # Defining the available bet amounts and symbols
    def __init__(self):
        self.bets = [1, 2, 5, 10, 15, 20]
        self.symbols = ["🍒", "🍋", "🔔", "⭐", "💎"]

# Returns the current bet amount
    def get_bet(self,bet_index):
        bet = self.bets[bet_index]
        return bet

# Returns a 3x3 grid of randomly chosen symbols
    def spin(self):
        grid = [(random.choices(self.symbols, weights=self.odds, k=3)) for _ in range(3)]
        return grid

# Checks for winning combinations
# Returns the payout and winning lines
# A straight row is worth 1.5x the bet, a diagonal is worth 2x the bet
    def check_wins(self, grid, bet):
        wins = 0
        winning_lines = []

        # Matching rows
        for row_index, row in enumerate(grid):
            if row[0] == row[1] == row[2]:
                wins += self.payouts[row[0]] * 1.5
                winning_lines.extend([
                    [row_index, 0],
                    [row_index, 1],
                    [row_index, 2]
                ])

        # Diagonal
        if grid[0][0] == grid[1][1] == grid[2][2]:
            wins += self.payouts[grid[0][0]] * 2
            winning_lines.extend([
                [0, 0],
                [1, 1],
                [2, 2]
            ])

        # Descending diagonal
        if grid[0][2] == grid[1][1] == grid[2][0]:
            wins += self.payouts[grid[0][2]] * 2
            winning_lines.extend([
                [0, 2],
                [1, 1],
                [2, 0]
            ])
        wins *= bet

        return wins, winning_lines

# Lowers the bet if not at minimum
    def lower_bet(self, bet_index):
        if bet_index == 0:
            return bet_index
        bet_index -= 1
        return bet_index

# Raises the bet if not at maximum
    def raise_bet(self, bet_index):
        if bet_index == len(self.bets)-1:
            return bet_index
        bet_index += 1
        return bet_index

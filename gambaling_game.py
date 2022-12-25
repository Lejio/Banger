import random
import time


class roulette():

  def __init__(self):

    self.players = {}
    self.betting = {}
    self.num_players = 0
    self.color = ""
    self.roulette = {"GREEN": {}, "BLACK": {}, "RED": {}}
    self.default_cash = 10000

  def startgame(self, default_cash):  # Depricated method, you can still use this to change the default cash of all new players.

    self.default_cash = default_cash

  def addplayer(self, player):

    if player in self.players.keys():  # Checks the player's username is a key inside of the dictionary.

      return False

    self.players[player] = {"Money": self.default_cash, "Debt": 0}  # If player's name is not inside the dictionary, create a new key.

    return True

  def betcash(self, player, bet_money, color):

    self.players[player]["Money"] -= bet_money

    print(self.players)

    if ((self.players[player]["Money"]) <= 0):

      self.players[player]["Money"] += bet_money

      return False

    if player in self.roulette[color].keys():

      self.roulette[color][player] += bet_money

    else:
      
      self.roulette[color][player] = bet_money
      
    return True

  def getmoney(self, player, amount):  # Depricated method.

    self.players[player]["Money"] += amount
    self.players[player]["Debt"] += amount

  def start_round(self):

    number = random.randint(0, 37)

    if ((number == 0) or (number == 37)):  # Number 37 is turned into 00, while both numbers will represent GREEN

      if number == 37:

        number = 00

      self.color = "GREEN"

    elif (number % 2) == 0:  # If it is even, it has landed on BLACK

      self.color = "BLACK"

    else:

      self.color = "RED"

    return [self.color, number]

  def end_round(self, color):  # This method should be ran after the start_round() method. It completes the final back end processes, such as giving the players money, etc.

    self.pot = 0

    num_winners = len(self.roulette[self.color])

    if num_winners > 0:

      for col in self.roulette:

        if (col != self.color):

          for player in self.roulette[col]:

            self.pot += self.roulette[col][player]

        else:

          for player in self.roulette[col]:

            self.players[player]["Money"] += int(self.roulette[col][player])  # Returns the money to the player (suppositely, something is wrong with this atm)
            
      print(self.pot)
      self.pot = int(self.pot / num_winners)

      if self.pot == 0:
        
        for player in self.roulette[self.color]:
  
          self.players[player]["Money"] += int(self.roulette[self.color][player] * 1.5)  # The player increases their money by 50% if playing alone.

          return True

      else:

        for player in self.roulette[self.color]:

          self.players[player]["Money"] += self.pot

        return True

    return False

  def return_winners(self):

    winners = {}

    for player in self.roulette[self.color]:

      winners[player] = self.roulette[self.color][player]

      self.players[player]["Money"] += self.roulette[self.color][player]

    return winners

  def return_losers(self):

    losers = {}

    for col in self.roulette:

      if (col != self.color):

        for player in self.roulette[col]:

          if player in losers.keys():

            losers[player] =+ self.roulette[col][player]

          else:
            
            losers[player] = self.roulette[col][player]

    return losers

  def return_result(self):

    return [self.return_winners(), self.return_losers()]

  def get_info(self, player):

    return [
      player, self.players[player]["Money"], self.players[player]["Debt"]
    ]

  def get_bettable(self):

    return self.roulette

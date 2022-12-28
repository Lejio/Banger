def roulette_table(dict):

  prn_str = ""

  for color in dict:

    prn_str += color + ":\n"

    for player in dict[color]:

      prn_str += str(player) + " is betting " + str(dict[color][player]) + "\n"

    prn_str += "\n"

  return prn_str


def roulette_results(winners, losers):

  losers_list = "The losers are:\n"
  winners_list = "The winners are:\n"

  for winner in winners:

    winners_list += f"{str(winner)}: {winners[winner]}"

  winners_list += "\n"

  for loser in losers:

    losers_list += f"{str(loser)}: {losers[loser]}"

  return [winners_list, losers_list]

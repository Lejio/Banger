
def roulette_table(dict):

  prn_str = ""
  prn_list = []

  for color in dict:

    for player in dict[color]:

      prn_str += str(dict[color][player][0]) + " is betting " + str(dict[color][player][1]) + "$BNG\n"

    if (len(dict[color]) == 0):

        prn_str += "No active bets."

    prn_list.append(prn_str)
    prn_str = ""

  return prn_list


def roulette_results(winners, losers):

  losers_list = ""
  winners_list = ""

  for winner in winners:

    winners_list += f"{winners[winner][0]}: {winners[winner][1]}"

  winners_list += "\n"

  for loser in losers:

    losers_list += f"{losers[loser][0]}: -{losers[loser][1]}"

  return [winners_list, losers_list]

import random


class random_generator():

  def __init__(self, number_of_sides):

    self.number_of_sides = number_of_sides

  def roll_dice(self):

    return int(random.randint(1, self.number_of_sides))

  def coinflip(self):

    return int(random.randint(0, 1))

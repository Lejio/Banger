from replit import db

class users:

  def __init__(self):

    self.BANGERS = 'Bangers'
    self.LVL = 'Lvl'
    self.BADGE = 'Rank'

  def retrieve_info(self, user):

    return db[user]


  def add_user(self, user):

    db[user] = {self.BANGER:1000, self.LVL:0, self.BADGE:":video_game:"}
    
    return True


  def get_bangers(self, user):

    return db[user][self.BANGER]

  
  def get_level(self, user):

    return db[user][self.BADGE]
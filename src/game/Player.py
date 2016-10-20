from .Team import Team

class Player:
    """A class for keeping info about a player among the players on the court in an event, at a moment"""

    def __init__(self, player):
        self.team = Team(player[0])
        self.id = player[1]
        self.x = player[2]
        self.y = player[3]
        self.color = self.team.color

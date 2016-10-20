from .Ball import Ball
from .Player import Player

class Moment:
    """A class for keeping info about the moments in an event"""

    def __init__(self, index, moment):
        self.index = index
        self.quarter = moment[0]
        self.game_clock = moment[2]
        self.shot_clock = moment[3]
        ball = moment[5][0]
        self.ball = Ball(ball)
        players = moment[5][1:]
        self.players = [Player(player) for player in players]
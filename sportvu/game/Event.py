from .Moment import Moment

class Event:
    """A class for handling and showing events in a game"""

    def __init__(self, index, event):
        self.index = index
        moments = event['moments']
        self.moments = [Moment(index, moment) for index, moment in enumerate(moments)]
        home_players = event['home']['players']
        guest_players = event['visitor']['players']
        players = home_players + guest_players
        player_ids = [player['playerid'] for player in players]
        player_names = [" ".join([player['firstname'],
                                  player['lastname']]) for player in players]
        player_jerseys = [player['jersey'] for player in players]
        values = list(zip(player_names, player_jerseys))
        # Example: 101108: ['Chris Paul', '3']
        self.player_ids_dict = dict(zip(player_ids, values))
        self.eventId = event['eventId']


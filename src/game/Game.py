import pandas as pd
from .Event import Event
import src.util.visualize as visualize
from src.util.actions import get_actions

class Game:
    """A class for keeping info about the games"""

    def __init__(self, path_to_json):
        # self.events = None
        self.home_team = None
        self.guest_team = None
        self.events = None
        self.path_to_json = path_to_json
        self.actions = []

    def read_json(self):
        data_frame = pd.read_json(self.path_to_json)
        self.home_team = data_frame['events'][0]['home']['teamid']
        self.guest_team = data_frame['events'][0]['visitor']['teamid']
        self.events = [Event(index, event) for index, event in enumerate(data_frame['events'])]
        self.actions = get_actions(self.events)

    # For visualization
    def start(self):
        for index, event in enumerate(self.events):
            print("showing {}".format(index))
            # print("eventID {}".format(event.eventId))

            visualize.init(event)

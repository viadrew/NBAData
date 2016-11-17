import pandas as pd
from .Event import Event
import sportvu.util.visualize as visualize
from sportvu.util.actions import get_actions
import random
import csv

class Game:
    """A class for keeping info about the games"""

    def __init__(self, path_to_json):
        # self.events = None
        self.home_team = None
        self.guest_team = None
        self.events = None
        self.path_to_json = path_to_json
        self.actions = []

    def read_json(self, seed):
        data_frame = pd.read_json(self.path_to_json)
        self.home_team = data_frame['events'][0]['home']['teamid']
        self.guest_team = data_frame['events'][0]['visitor']['teamid']
        self.events = [Event(index, event) for index, event in enumerate(data_frame['events'])]

        #Randomly picking 2 quarters in a game (but only randomly once)
        quarters = [1, 2, 3, 4]
        random.seed(seed)
        random.shuffle(quarters)

        self.actions = get_actions(self.events, quarters[0], quarters[1])

    def actions_to_csv(self, path, filename):

        for action in self.actions:
            time = action.moments[0].game_clock
            m, s = divmod(time, 60)
            # print('{:d}:{:.2f} ... {:d}'.format(int(m), s, action.moments[0].quarter))

            with open(path, 'a') as f:
                writer = csv.writer(f)
                writer.writerow( (filename[:10], filename[11:21], action.event_index, action.moments[0].quarter,
                              '{:d}:{:.2f}'.format(int(m), s),
                              '{:.1f}'.format(action.frames / 25)) )

    # For visualization
    def start(self):
        for index, event in enumerate(self.events):
            print("showing {}".format(index))
            # print("eventID {}".format(event.eventId))

            visualize.init(event)

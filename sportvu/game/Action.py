class Action:
    """Class to store information on a determined action"""

    def __init__(self, event, event_index, start_moment, frames, ballhandler):
        self.event_index = event_index
        self.start_moment = start_moment
        self.frames = frames
        self.moments = event.moments[start_moment:(start_moment+frames)]
        self.ball_handler = ballhandler

    def def_players(self):
        return
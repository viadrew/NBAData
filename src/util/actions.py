import math
from shapely.geometry import Point, Polygon
from src.game.Action import Action

# Main utility function
def get_actions(events):
    '''Data extraction of 'actions' according to rule-based algorithm'''

    actions = []

    for i, event in enumerate(events):
        ball_handler = None
        is_action = False
        positive_condition_counter = 0
        start_moment = None

        for j, moment in enumerate(event.moments):
            # Retrieve data
            sorted_players = sorted(moment.players, key=lambda player: player.team.id)
            home_players = sorted_players[:5]
            away_players = sorted_players[5:]
            ball = moment.ball

            # Determine which team has offensive possession based on what side of the court the ball is in,
            # and what half it is (based on quarter)
            #
            # We ignore cases of ball handler bringing it up from their end as it is irrelevant in determining actions
            #
            # Ball on left side of court:
            #   1st half: Offensive team is the home team, otherwise the away team (right side of court)
            #   2nd half: Offensive team is the away team, otherwise the home team (right side of court)
            half = 1 if (moment.quarter in {1, 2}) else 2
            is_home = get_off_team(ball, half)

            if is_home:
                off_players = home_players
                def_players = away_players
            else:
                off_players = away_players
                def_players = home_players

            curr_ball_handler = get_ballhandler(ball, off_players)
            get_ballhandler(ball, def_players)

            # Time for the rule based algorithm ...
            if rule_algo(moment, off_players, def_players, ball, curr_ball_handler, half, is_home):
                # Increment counter of consecutive frames that passed the rule-based algo (base case counter=0)
                if (positive_condition_counter == 0):
                    positive_condition_counter += 1
                    ball_handler = curr_ball_handler
                    start_moment = j
                elif (curr_ball_handler.id == ball_handler.id):
                    positive_condition_counter +=1

                if positive_condition_counter >= 13:
                    # Action detected
                    if not is_action:
                        is_action = True
            else:
                if positive_condition_counter >= 13:
                    # Add action to actions list
                    action = Action(event, i, start_moment, positive_condition_counter)

                    if len(actions) is 0:
                        actions.append(action)
                    else:
                        duplicate = [a for a in actions if a.frames == action.frames and a.moments[0].game_clock ==
                                     action.moments[0].game_clock]
                        if not duplicate:
                            actions.append(action)

                    is_action = False
                positive_condition_counter = 0
    return actions

# Utility for get_actions
def get_ballhandler(ball, players):
    ''' Returns the likely ball handler among offensive players if any'''

    # Later needs to consider previous frame's ball handler
    player_distances = [(player, get_distance(ball, player)) for player in players]
    potential_bh = [candidate for candidate in player_distances if candidate[1] < 5]
    if not potential_bh:
        return None
    elif len(potential_bh) == 1:
        return potential_bh[0][0]
    return max(potential_bh, key=lambda x: x[1])[0]

def get_distance(object1, object2):
    ''' Return the distance between two trackable objects (player(s) or ball '''
    return math.sqrt(((object1.x - object2.x) ** 2) + ((object1.y - object2.y) ** 2))

def get_off_team(ball, half):
    ''' Used to determine the offensive team based on ball location and current half '''

    left_half = Polygon([(0, 0), (0, 50), (47, 50), (47, 0)])
    ball_xy = Point(ball.x, ball.y)

    return left_half.contains(ball_xy) and half == 1

def is_in_paint(player, ball, half, is_home):
    ''' Determine if offensive player or ball is in the paint '''

    player_xy = Point(player.x, player.y)
    ball_xy = Point(ball.x, ball.y)

    if (half == 1 and is_home) or (half == 2 and not is_home):
        paint = Polygon([(0, 15), (0, 35), (15, 35), (19, 33), (19, 17), (15, 15)])
    else:  # (half == 2 and is_home) or (half == 1 and not is_home)
        paint = Polygon([(94, 15), (94, 35), (79, 35), (75, 33), (75, 17), (79, 15)])

    return paint.contains(player_xy) or paint.contains(ball_xy)

def rule_algo(moment, off_players, def_players, ball, curr_ball_handler, half, is_home):
    ''' Rule algorithm as outlined in paper; '''

    # Check state after every rule and return at False, as future rules may depend on previous to be true:
    # 1: There is a player handling the ball
    condition1 = curr_ball_handler
    if not condition1:
        return False

    # 2: Another offensive player within 10 feet of ball-handler (i.e. the screener)
    non_bh_off_players = [player for player in off_players if player.id is not curr_ball_handler.id]
    potential_screeners = [screener for screener in non_bh_off_players if \
                           get_distance(curr_ball_handler, screener) <= 10]
    condition2 = not not potential_screeners
    if not condition2:
        return False

    likely_screener = min(potential_screeners, key=lambda x: get_distance(x, curr_ball_handler))
    # 3: Screener or ball is not inside the general paint area
    condition3 = is_in_paint(likely_screener, ball, half, is_home)
    if condition3:
        return False

    # 4: Screener is no more than 2ft. further from the basket than the ball handler is
    distance_to_basket = abs(get_distance(curr_ball_handler, ball) - get_distance(likely_screener, ball))
    condition4 = distance_to_basket <= 4 #3.2, 3.4, 3,5


    if not condition4:
        return False

    # 5: There is a defender <= 12 ft from ball handler (on-ball defender),
    defenders = [defender for defender in def_players if get_distance(defender, curr_ball_handler) <= 12]
    condition5 = not not defenders

    # determine likely defender for future
    #likely_defender = min(defenders, key=lambda x: get_distance(x, curr_ball_handler))
    if not condition5:
        return False

    return True


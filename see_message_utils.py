import math
import message_utils

def get_enemy_goal_from_team(side:str):
    if side in ['r', 'right']:
        return ['g', 'l']
    elif side in ['l', 'left']:
        return ['g', 'r']

def get_team_goal_from_team(side:str):
    if side in ['r', 'right']:
        return ['g', 'r']
    elif side in ['l', 'left']:
        return ['g', 'l'] 

def filter_goal(target_goal=['g', 'r']):
    return lambda item:item[0] == target_goal

def goal_is_visible(message, target_goal):
    goal_objects = list(filter(filter_goal(target_goal), message[0][2:-1]))
    if len(goal_objects) < 1:
        return False, None
    return True, goal_objects[0]

def team_goal_is_visible(message, player):
    target_goal = get_team_goal_from_team(player.status['player_side'])
    return goal_is_visible(message, target_goal)

def enemy_goal_is_visible(message, player):
    target_goal = get_enemy_goal_from_team(player.status['player_side'])
    return goal_is_visible(message, target_goal)

def filter_players():
    return lambda item:type(item[0]) == list and len(item[0]) == 3 and item[0][0] == 'p'

def filter_enemy_players(player) -> list:
    filter_players_func = filter_players()
    return lambda item:filter_players_func(item) and item[0][1] != player.status['team_name']

def filter_team_players(player) -> list:
    filter_players_func = filter_players()
    return lambda item:filter_players_func(item) and item[0][1] == player.status['team_name']

def filter_ball():
    return lambda item:item[0][0] in ['b', 'B']

def ball_is_visible(message):
    ball_objects = list(filter(filter_ball(), message[0][2:-1]))
    if len(ball_objects) < 1:
        return False, None
    return True, ball_objects[0]

def ball_is_kickable(message):
    ball_visible, ball = ball_is_visible(message)
    return (ball_visible and float(ball[1]) < 1.0), ball

def calc_objects_direction(A_distance, B_distance, A_direction, B_direction):
    rad = math.radians(A_direction - B_direction)
    return (A_distance ** 2 + B_distance ** 2) - (2 * A_distance * B_distance * math.cos(rad))

def judge_nearest_to_ball(message, ball_location, player_locations):
    ball_distance = float(ball_location[1])
    ball_direction = float(ball_location[2])
    for player_location in player_locations:
        # target is a other player
        target_distance = float(player_location[1])
        target_direction = float(player_location[2])
        result_distance = calc_objects_direction(
            target_distance,
            ball_distance,
            target_direction,
            ball_direction
        )
        if ball_distance > result_distance:
            return False
    return True

def filter_line():
    return lambda item:item[0][0] == 'l'

def normalize_angle(angle):
    if abs(angle) > 720.0:
        raise ValueError('invalid angle')
        sys.exit()
    while angle > 180.0:
        angle -= 360.0
    while angle < -180:
        angle += 360.0
    return angle

def get_neck_dir(message, player):
    lines = list(filter(filter_line(), message[0][2:-1]))
    if len(lines) > 0:
        print(lines)

def filter_flag():
    return lambda item:item[0][0] == 'f'


from see_message_utils import *
# commands

# turn
def turn_to_ball(message, player):
    ball_visible, ball_location = ball_is_visible(message)
    if not ball_visible or float(ball_location[2]) == 0.0:
        return None
    return '(turn {})'.format(ball_location[2])

def turn_to_enemy_goal(message, player):
    goal_visible, goal_location = enemy_goal_is_visible(message, player)
    if not goal_visible or float(goal_location[2]) == 0.0:
        return None
    return turn(message, player, goal_location[2])

def turn_to_team_goal(message, player):
    goal_visible, goal_location = team_goal_is_visible(message, player)
    if not goal_visible or float(goal_location[2]) == 0.0:
        return None
    return turn(message, player, goal_location[2])

def turn(message, player, direction=60):
    ball_kickable, ball_location = ball_is_kickable(message)
    if ball_kickable:
        return '(kick 10 {})(turn {})'.format(direction, direction)
    return '(turn {})'.format(direction)

def turn_60(message, player):
    return turn(message, player, 60)

def turn_minus_60(message, player):
    return turn(message, player, -60)

def turn_30(message, player):
    return turn(message, player, 30)

def turn_minus_30(message, player):
    return turn(message, player, -30)

def turn_180(message, player):
    return turn(message, player, 180)

# change view
def change_view_narrow(message, player):
    player.update_status('view_type', 'narrow')
    return '(change_view narrow)'

def change_view_normal(message, player):
    player.update_status('view_type', 'normal')
    return '(change_view normal)'

def change_view_wide(message, player):
    player.update_status('view_type', 'wide')
    return '(change_view wide)'

# dash
def dash_to_ball(message, player):
    ball_visible, ball_location = ball_is_visible(message)
    if not ball_visible:
        return None
    return '(dash 80 {})'.format(ball_location[2])

def dash_max(message, player):
    return '(dash 100)'

def dash_slow(message, player):
    return '(dash 50)'

def dash_180(message, player):
    return '(dash 80 180)'

def dash_90(message, player):
    return '(dash 80 90)'

def dash_minus_90(message, player):
    return '(dash 80 -90)'

# kick
def kick(message, player, direction=0, power=80):
    ball_kickable, ball_location = ball_is_kickable(message)
    if not ball_kickable:
        return None
    return '(kick {} {})(turn {})'.format(power, direction, direction)

def kick_to_goal(message, player):
    goal_visible, goal_location = enemy_goal_is_visible(message, player)
    if not goal_visible:
        return kick(message, player, goal_location[2], 100)
    else:
        return None

def kick_to_closest_member(message, player, skip_count=0):
    ball_kickable, ball_location = ball_is_kickable(message)
    visible_players = list(filter(filter_team_players(player), message[0][2:-1]))
    if len(visible_players) < skip_count + 1:
        return None
    visible_players = list(sorted(visible_players, key=lambda item:item[1]))
    kick_power = float(visible_players[skip_count][1]) * 3.0 + 10
    return kick(message, player, visible_players[skip_count][2], kick_power)
    
def kick_to_2nd_closest_member(message, player):
    return kick_to_closest_member(message, player, 1)

def kick_to_3rd_closest_number(message, player):
    return kick_to_closest_member(message, player, 2)

# say
code = 'Oe93oivgweIgMQXpreiIE'
def say_team(message, player):
    return '(say "team {}")'.format(code)

def say_pass(message, player):
    return '(say "pass {}")'.format(code)

# move
kickoff_positions = {
    1: {'x': -50.0, 'y': -0.0},
    2: {'x': -40.0, 'y': -15.0},
    3: {'x': -40.0, 'y': -5.0},
    4: {'x': -40.0, 'y': +5.0},
    5: {'x': -40.0, 'y': +15.0},
    6: {'x': -20.0, 'y': -15.0},
    7: {'x': -20.0, 'y': -5.0},
    8: {'x': -20.0, 'y': +5.0},
    9: {'x': -20.0, 'y': +15.0},
    10: {'x': -1.0, 'y': -5.0},
    11: {'x': -4.0, 'y': +10.0},
}

def move_kickoff(message, player):
    kickoff_position = kickoff_positions[player.status['player_number']]
    command = '(move {} {})'.format(kickoff_position['x'], kickoff_position['y'])
    return command

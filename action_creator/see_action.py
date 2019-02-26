import message_utils
import see_message_utils as see_utils
import status_utils
import commands
import math


# actions

def when_kickable_to_goal(message, goal):
    goal_distance = float(goal[1])
    goal_direction = float(goal[2])

    if goal_distance > 30.0:
        return '(kick 15 {})(dash 80 {})'.format(goal_direction, goal_direction)
    else:
        return '(kick 100 {})'.format(goal_direction)


def when_ball_visible(message, ball, player):
    command = commands.kick_to_closest_member(message, player)
    if command != None:
        return command
    command = commands.dash_to_ball(message, player)
    if command != None:
        return command
    return commands.turn_30(message, player)

def tmp_func(message, player):
    ball_visible , ball_location = see_utils.ball_is_visible(message)
    ball_kickable = ball_visible and float(ball_location[1]) < 1.0
    command = None

    if ball_kickable:
        command = commands.kick_to_closest_member(message, player)
        if command == None:
            return commands.turn_60(message, player) + commands.change_view_narrow(message, player)
        return command + commands.change_view_normal(message, player)
    elif ball_visible and player.status['player_number'] > 1:
        player_locations = list(filter(see_utils.filter_team_players, message[0][2:-1]))
        nearest_to_ball = see_utils.judge_nearest_to_ball(message, ball_location, player_locations)
        if float(ball_location[1]) < 10.0 and nearest_to_ball:
            return commands.dash_to_ball(message, player)
        return commands.turn_to_ball(message, player)
    elif ball_visible:
        return commands.dash_max(message, player)
    else:
        return commands.turn_30(message, player)

def action_after_kickoff(message, player):
    ball_visible, ball_location = see_utils.ball_is_visible(message)
    if ball_visible:
        return tmp_func(message, player)
    else:
        print('ball invisible')
        return '(turn 30)' + commands.change_view_normal(message, player)

def action_see(message, player):
    # if player.status['player_side'] == 'left' and player.status['player_number'] == 1:
    #     print(message)
    if message[0][0] != 'see':
        return None
    elif status_utils.is_initial_mode(player.status):
        return commands.move_kickoff(message, player)
    else:
        return action_after_kickoff(message, player)

import see_message_utils as see_utils

def write_see_info(message, player):
    if message[0][0] != 'see':
        return None
    write_ball_info(message, player)        
    write_team_goal_info(message, player)
    write_enemy_goal_info(message, player)
    write_player_info(message, player)

def write_ball_info(message, player):
    ball_visible, ball_location = see_utils.ball_is_visible(message)
    ball_kickable = ball_visible and float(ball_location[1]) < 1.0
    nearest_to_goal = ball_visible and see_utils.judge_nearest_to_goal(message, ball_location, player_locations)

    player.update_status('ball', {
        'visible': ball_visible,
        'kickable': ball_kickable,
        'player_is_nearest': nearest_to_goal
    })

def write_team_goal_info(message, player):
    team_goal_visible, team_goal_location = see_utils.team_goal_is_visible(message, player)
    player.update_status('team_goal', {
        'visible': team_goal_visible,
        'location': team_goal_location
    })

def write_enemy_goal_info(message, player):
    enemy_goal_visible, enemy_goal_location = see_utils.enemy_goal_is_visible(message, player)
    player.update_status('enemy_goal', {
        'visible': enemy_goal_visible,
        'location': enemy_goal_location
    })

def write_player_info(message, player):
    player.update_status('team_players', list(filter(see_utils.filter_team_players(player), message[0][2:-1])))
    player.update_status('enemy_players', list(filter(see_utils.filter_enemy_players(player), message[0][2:-1])))

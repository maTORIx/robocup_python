
def is_initial_mode(status):
    if 'play_mode' not in status.keys():
        return False
    play_mode = status['play_mode']
    if play_mode.startswith('goal_r') or play_mode.startswith('goal_l') or play_mode == 'before_kick_off':
        return True
    else:
        return False

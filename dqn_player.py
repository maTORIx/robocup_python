from socket import *
import threading
import sys
import json
import random

import message_utils
import status_utils
import status_writer
import see_message_utils
from commands import move_kickoff
import dqn

# logger 定義
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

LERNING_LATE = 0.5
GAMMA = 0.995

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
handler_format = logging.Formatter('%(levelname)s: %(message)s at %(name)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

class Player(threading.Thread):
    def __init__(self, host_name='localhost', port=6000, version='15.40'):
        threading.Thread.__init__(self)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = host_name
        self.PORT = port
        self.ADDRESS = gethostbyname(self.HOSTNAME)
        self.ServerVersion = version
        self.status_writer_list = status_writer.status_writer_list

        self.command_history = [""]
        self.status = {}
        self.dqn = dqn.Estimater(1, 'left')
        self.episode_finished = True
        self.next_reward = 0
        self.last_command = ''


    def send(self, command):
        if len(command) == 0:
            return
        command = command + "\0"
        try:
            to_byte_command = command.encode(encoding='utf_8')
            self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))
            logger.debug("sending {} is done".format(command))
        except OSError:
            logger.error('送信失敗')
            sys.exit()

    def receive(self):
        try:
            message, arr = self.socket.recvfrom(4096)
            message = message.decode("UTF-8")
            self.PORT = arr[1]
            return message
        except OSError:
            logger.error('受信失敗')
            sys.exit()
            return ""


    def initialize(self, number, team_name):
        self.update_status('player_number', int(number))
        self.update_status('team_name', team_name)
        if self.status['player_number'] == 1:
            command = '(init {}(goalie)(version {}))'.format(self.status['team_name'], self.ServerVersion)
        else:
            command = '(init {}(version {}))'.format(self.status['team_name'], self.ServerVersion)
        self.send(command)
    
    def update_status(self, parameter_name, status):
        self.status[parameter_name] = status

    # thread を動かしている最中に行われる関数
    def run(self):
        while True:
            message = self.receive()
            parsed_message = message_utils.parse_message(message)
            self.analyzeMessage(parsed_message)
    
    def get_reward(self, message):
        reward = 0
        ball_visible, ball_location = see_message_utils.ball_is_visible(message)
        if ball_visible: reward += 1 + 50 - float(ball_location[2])
        if self.last_command == None: reward -= 1
        return reward
    
    def write_status(self, message):
        for func in self.status_writer_list:
            func(message, self)

    def analyzeMessage(self, message):
        commands = []
        message_head = message[0][0]
        if isinstance(message, type(None)) or len(message) < 1:
            return None
        self.write_status(message)
        # print('end: ', status_utils.is_initial_mode(self.status))
        
        if message_head == 'see' and status_utils.is_initial_mode(self.status):
            if self.episode_finished == False:
                self.dqn.end(self.status['play_mode'].startswith('goal_l'))
                self.episode_finished = True
            command = move_kickoff(message, self)
            self.send(command)
        elif message_head == 'see':
            if self.episode_finished:
                self.episode_finished = False
            # reward = message_utils.calc_reward_from_see_message(message, self) + self.next_reward
            reward = self.get_reward(message)
            suggest_command = self.calc_suggest_command(message)
            suggest_command = None
            command = self.dqn(message_utils.parse_see_message_to_data(message, self), reward, suggest_command=suggest_command)

            # self.next_reward = message_utils.calc_next_reward(command, message, self.last_command)
            self.last_command = command
            
            self.send(command)
    
    def calc_suggest_command(self, message):
        ball_visible, ball_location = see_message_utils.ball_is_visible(message)
        ball_kickable = ball_visible and float(ball_location[1]) < 1.0
        goal_visible, goal_location = see_message_utils.enemy_goal_is_visible(message, self)
        if ball_kickable and goal_visible:
            return '(kick 80 {})'.format(goal_location[2])
        elif ball_visible and (float(ball_location[2]) > 20 or float(ball_location[2]) < -20):
            return '(turn {})'.format(ball_location[2])
        elif ball_kickable:
            return '(kick 15 60)'
        elif ball_visible:
            return '(dash 80 {})'.format(ball_location[2])
        else:
            return '(turn 60)'

def start_team(team_name, host_name='localhost', port=6000, version='15.50'):
    players = []
    for i in range(11):
        p = Player(host_name, port, version)
        players.append(p)
        players[i].initialize(i+1, team_name)
        players[i].start()  


if __name__ == "__main__":
    # team_1 = start_team('left')
    # team_2 = start_team('right')
    player_dqn = Player()
    player_dqn.initialize(11, 'right')
    player_dqn.start()
    print("試合登録完了")

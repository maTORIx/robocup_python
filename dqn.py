import os
import copy
import time
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from message_utils import parse_message
import datetime

# util and commands 

def calc_paramater(act_min, act_max, max_val):
    if act_max == 0.0 and act_min == 0.0:
        return 0, (0.5,0.5)
    reward_sum = act_max + act_min
    reward_rate = (act_min / reward_sum, act_max / reward_sum)
    value = max_val * reward_rate[1]
    return value, reward_rate

def command_turn(inference_result):
    direction, reward_rate = calc_paramater(inference_result[0], inference_result[1],180)
    command = '(turn {})'.format(direction - 90)
    # print(inference_result, reward_rate)
    return command, reward_rate

def command_dash(inference_result):
    power, reward_rate_a = calc_paramater(inference_result[0], inference_result[1], 100)
    direction, reward_rate_b = calc_paramater(inference_result[2], inference_result[3], 180)
    command = '(dash {} {})'.format(power, direction - 90)
    return command, (reward_rate_a[0] / 2.0, reward_rate_a[1] / 2.0, reward_rate_b[0] / 2.0, reward_rate_b[1] / 2.0)

def command_kick(inference_result):
    power, reward_rate_a = calc_paramater(inference_result[0], inference_result[1], 100)
    direction, reward_rate_b = calc_paramater(inference_result[2], inference_result[3], 180)
    command = '(kick {} {})'.format(power, direction - 90)
    return command, (reward_rate_a[0] / 2.0, reward_rate_a[1] / 2.0, reward_rate_b[0] / 2.0, reward_rate_b[1] / 2.0)

def command_change_view_wide(inference_result):
    return '(change_view wide)', (1,)

def command_change_view_normal(inference_result):
    return '(change_view normal)', (1,)

def command_change_view_narrow(inference_result):
    return '(change_view narrow)', (1,)

def random_commands():
    vals = [
        (0, [0.2, 0.8]),
        (0, [0.3, 0.7]),
        (0, [0.4, 0.6]),
        (1, [0.2, 0.8, 0.8, 0.2]),
    ]
    return vals[random.randrange(len(vals))]

def find_command_and_rate(command:str) -> int:
    print(command)
    parsed_command = parse_message(command)[0]
    command_index =  ['turn', 'dash', 'kick', 'change_view'].index(parsed_command[0])
    if parsed_command[0] == 'turn':
        command_index = 0
        dir_a = float(parsed_command[1]) + 180.0
        dir_b = 360.0 - dir_a
        return command_index, [dir_b, dir_a]
    elif parsed_command[0] == 'dash' or parsed_command[0] == 'kick':
        command_index = 1 if parsed_command[0] == 'dash' else 2
        power_a = float(parsed_command[1])
        power_b = 100.0 - power_a
        dir_a = float(parsed_command[2]) + 180.0
        dir_b = 360.0 - dir_a
        return command_index, [power_b, power_a, dir_b, dir_a]
    elif parsed_command[0] == 'change_view':
        return 2 + ['wide', 'normal', 'narrow'].index(parsed_command[1])



command_arg_counts = np.array([2,4,4,1,1,1])
commands = [
    command_turn,
    command_dash,
    command_kick,
    command_change_view_wide,
    command_change_view_normal,
    command_change_view_narrow
]

# turn(dir) dash(power, direction), kick(power, direction) change_view_wide() change_view_normal() change_view_narrow()
# 入力値がある場合、入力値＊２のActが存在していることになる

# 環境
MONITOR = False
HIDDEN_SIZE = 300
MEMORY_SIZE = 3000
BATCH_SIZE = 20
TRAIN_INTERVAL = 10
GAMMA = 0.97
acts_num = 13
obs_num = 294 * 2 + acts_num * 3

class NN(nn.Module):
    def __init__(self):
        super(NN, self).__init__()
        self.fc1 = nn.Linear(obs_num, HIDDEN_SIZE)
        self.fc2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.fc3 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.fc4 = nn.Linear(HIDDEN_SIZE+obs_num, acts_num)
        self.dropout1 = nn.Dropout(0.3)
        self.dropout2 = nn.Dropout(0.5)
 
    def __call__(self, x):
        h = F.relu(self.fc1(x))
        h = F.relu(self.fc2(h))
        h = self.dropout1(h)
        h = F.relu(self.fc3(h))
        h = self.dropout2(h)
        y = F.relu(self.fc4(torch.cat([h, x], -1)))
        return y

class Estimater():
    def __init__(self, player_number, player_side, save_path='robo.pt', batch_size=BATCH_SIZE):
        self.player_number = player_number
        self.player_side = player_side
        self.save_path = save_path
        
        self.batch_size = batch_size
        self.commands = commands
        self.command_arg_counts = command_arg_counts

        self.q_func = NN()
        self.q_func_old = copy.deepcopy(self.q_func)
        if os.path.exists(self.save_path):
            self.load()
        self.optimizer = optim.RMSprop(self.q_func.parameters(), lr=0.00015, alpha=0.95, eps=0.01)

        self.saved = False
        self.episode = [] # [[state, act, reward_rate, reward, next_state]]
        self.total_reward = 0
        self.call_count = 0
    
    def __call__(self, state, state_reward=0, suggest_command=None):
        input_state = np.array(state, dtype='float32')
        command, act_command ,reward_rate, inference_result = self.predict(input_state, suggest_command)

        # input datas to self.episode for training
        self.total_reward += state_reward
        self.call_count += 1
        self.episode.append([input_state, act_command, reward_rate, None, None])
        if len(self.episode) > 0:
            self.episode[-1][3:] = [state_reward, input_state]

        if len(self.episode) > MEMORY_SIZE:
            self.episode.pop()
        if  self.call_count % TRAIN_INTERVAL == 0:
            self.train()

        if self.call_count % 500 == 0 and not self.saved:
            self.save()
        return command, inference_result
    
    def set_episode(self, episode):
        self.episode = episode
    
    def predict(self, state, suggest_command=None):
        result = self.q_func(Variable(torch.from_numpy(state))).data.numpy()
        command, best_act, reward_rate = self.parse_result_to_command(result, suggest_command)
        return command, best_act, reward_rate, result
    
    def parse_result_to_command(self, result, suggest_command=None):
        best_act, splited_result = self.inference_split(result, suggest_command)
        command, reward_rate = self.commands[best_act](splited_result[best_act])
        
        return command, best_act, reward_rate

    def inference_split(self, result, suggest_command=None):
        acts_results = []
        act_rewards = []
        start_index = 0
        for i in self.command_arg_counts:
            acts_results.append(result[start_index:start_index+i])
            act_rewards.append(np.sum(result[start_index:start_index+i]))
            start_index += i
        
        if suggest_command != None:
            best_act, act_reward = find_command_and_rate(suggest_command)
            acts_results[best_act] = np.array(act_reward)
        elif random.randint(0, 5) == 0:
            best_act, tmp = random_commands()
            acts_results[best_act] = tmp
        else:
            best_act = np.argmax(act_rewards)

        return best_act, acts_results

    def train(self):
        episode = np.array(self.episode)
        if len(episode) < self.batch_size:
            return None
        
        np.random.shuffle(episode)
        for i in range(len(episode))[::self.batch_size]:
            batch = episode[i:i+self.batch_size]
            if len(batch) < self.batch_size:
                continue
            states = np.array(batch[:,0].tolist(), dtype='float32')
            best_acts = batch[:,1]
            reward_rates = batch[:,2]
            rewards = batch[:,3]
            next_states = np.array(batch[:,4].tolist(), dtype='float32')
            inferences_a = self.q_func(Variable(torch.from_numpy(states)))
            inferences_b = self.q_func_old(Variable(torch.from_numpy(next_states))).data.numpy()
            target = copy.deepcopy(inferences_a.data.numpy())
            for l in range(self.batch_size):
                update_start = np.sum(self.command_arg_counts[:best_acts[l]])
                update_end = update_start + self.command_arg_counts[best_acts[l]]
                best_act, splited_inference = self.inference_split(inferences_b[l])
                tmp = np.sum(splited_inference[best_act])
                updates = np.array(reward_rates[l]) * (rewards[l] + (GAMMA * tmp))
                target[l,update_start:update_end] = updates
                # if l == 0:
                #     print(['turn', 'dash', 'kick', 'wide', 'normal', 'narrow'][best_acts[l]], rewards[l], updates)
            self.optimizer.zero_grad()
            loss = nn.MSELoss()(inferences_a, Variable(torch.from_numpy(target)))
            loss.backward()
            self.optimizer.step()
        
        self.q_func_old = copy.deepcopy(self.q_func)
        
    def end(self, win=True):
        reward = 2000 if win else -500
        self.episode[-1][3] = reward
        self.episode[-1][4] = np.zeros(obs_num)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        np.save('dataset_{}.npy'.format(timestamp), np.array(self.episode))
        self.train()

        self.episode = []
        self.total_reward = 0
        self.call_count = 0
    
    def save(self):
        torch.save(self.q_func.state_dict(), self.save_path)
    
    def load(self):
        self.q_func.load_state_dict(torch.load(self.save_path))
        self.q_func_old = copy.deepcopy(self.q_func)

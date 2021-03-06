import os
import numpy as np
from scipy.io import loadmat

def standardize(data):
    # zero-mean + normalize
    return (data - data.mean()) / data.std()

def init_data(config):
    path = os.path.join(config.data_path, config.subject + config.task +
            ('C' if config.cooling else ''), 'ConcatTaskData.mat')
    if not os.path.exists(path):
        pass
        # TO-DO : create appropriate ConcatTaskData.mat file

    # set up weight dictionary
    weights = dict()
    for weight in config.weights:
        weights[weight] = 1 # default
    
    # load task data
    task = loadmat(path, matlab_compatible=True)

    # initialize data dictionary
    data = dict({'name': config.subject + config.task + ('C' if config.cooling else '') + '_' + str(config.seed)})
    
    behavior = task['task'][0,0]['pillow'][0,0]
    
    y = {'y': behavior['choice'][0]}
    answer = {'answer': behavior['answer'][0]}
    correct = {'correct': behavior['correct'][0]}
    dayLength = {'dayLength': behavior['dayLength'][0]}

    # load all supported covariates
    stimulus_strength = behavior['stimulus_strength'][:]
    reward_history = behavior['rewardhistory'][:]
    stim_1 = behavior['stim_1'][:]
    stim_2 = behavior['stim_2'][:]
    stim_reward = stimulus_strength * reward_history
    temperature = behavior['temp'][:]

    if config.standardize:
        stimulus_strength = standardize(stimulus_strength)
        stim_1 = standardize(stim_1)
        stim_2 = standardize(stim_2)
        temp_standard = standardize(temperature)
   
    # convert to dict formate
    stimulus_strength = {'stimulus_strength': stimulus_strength} 

    # create inputs data type
    inputs = dict({'inputs': stimulus_strength})
    inputs['inputs']['reward_history'] = reward_history
    inputs['inputs']['StimulusStrength*RewardHistory'] = stim_reward
    inputs['inputs']['stim_1'] = stim_1
    inputs['inputs']['stim_2'] = stim_2
    inputs['inputs']['temperature'] = temperature
    inputs['inputs']['temperature_standard'] = temp_standard

    # finalize return type
    data.update(y)
    data.update(answer)
    data.update(correct)
    data.update(dayLength)
    data.update(inputs)

    # TODO : update the parameter list ... add parameter list to config file
    # TODO : include some logic for handling the interleaved case, which can be a little tricky
    
    return weights, data

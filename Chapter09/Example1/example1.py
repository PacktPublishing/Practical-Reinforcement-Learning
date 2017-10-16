#First thing to import all the required libraries here

import sys, time
from scipy import *

from pybrain.rl.environments import Task
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.environments.mazes import Maze, MDPMazeTask
from pybrain.rl.experiments import Experiment
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q, SARSA


var_structure_arr_ = array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 0, 0, 1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 1, 0, 0, 1, 0, 1],
                   [1, 0, 0, 1, 0, 0, 1, 0, 1],
                   [1, 0, 0, 1, 0, 1, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 1, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1]])
				   
				   

var_controller_ = ActionValueTable(81, 4)
var_controller_.initialize(1.0)				   



var_learner_ = Q()
var_Agent_ = LearningAgent(var_controller_, var_learner_)

var_task_ = MDPMazeTask(Task)

experiment = Experiment(var_task_, var_Agent_)




#We will import all the scientific libraries using numpy package

import numpy as _numP_

#We will import Grid World package

from gridworld import GridWorld

#Now we define our environment 3 by 4 Grid World

environment = GridWorld(3, 4)

# Now we will Define state matrix
# And adding the obstacle at the position (1,1)
# Finally adding the termina states

var_matrix_state_ = _numP_.zeros((3,4))
var_matrix_state_[0, 3] = 1
var_matrix_state_[1, 3] = 1
var_matrix_state_[1, 1] = -1

# Now we will define our matrix for reward
# And set the reqard as -0.04 for all states

var_matrix_reward_ = _numP_.full((3,4), -0.04)
var_matrix_reward_[0, 3] = 1
var_matrix_reward_[1, 3] = -1

# Here we will define our matrix for transition
# and also define the actions probabilities

var_matrix_transition = _numP_.array([[0.8, 0.1, 0.0, 0.1],
                              [0.1, 0.8, 0.1, 0.0],
                              [0.0, 0.1, 0.8, 0.1],
                              [0.1, 0.0, 0.1, 0.8]])

# It's time to define the matrix for policy
# 1=RIGHT, 0=UP, 3=LEFT, 2=DOWN, -1=NoAction NaN=Obstacle



var_matrix_policy = _numP_.array([[1, 1, 1, -1],
                          [0, _numP_.NaN, 0, -1],
                          [0, 3, 3, 3]])

# Set the matrices 

environment.setStateMatrix(var_matrix_state_)
environment.setRewardMatrix(var_matrix_reward_)
environment.setTransitionMatrix(var_matrix_transition)

#We reset the Grid World environment
var_obser_ = environment.reset()

#Render method will display our Grid World
environment.render()

for _ in range(1000):

    var_actions_ = var_matrix_policy[var_obser_[0], var_obser_[1]]

    var_obser_, var_rewards_, var_done_ = environment.step(var_actions_)

    print("")

    print("Total actions_: " + str(var_actions_))

    print("Total Rewards: " + str(var_rewards_))

    print("Complete: " + str(var_done_))

    environment.render()

    if var_done_: 

	    break


	  
	  
	  
	  
	  
def fuc_return_get(par_list_state_, par_gamma_df):
		var_count_ = 0
		var_value_return = 0
		for var_visit in par_list_state_:
			var_rewards_ = var_visit[1]
			var_value_return += var_rewards_ * _numP_.power(par_gamma_df, var_count_)
			var_count_ += 1
		return var_value_return

		
# Define the empty matrix utility
var_matrix_utility_ = _numP_.zeros((3,4))

# Now we initialize it
var_matrix_mean_running = _numP_.full((3,4), 1.0e-10) 
par_gamma_df = 0.999 #discount factor
var_epoch_tot = 50000
var_epoch_print = 1000

for var_epoch_ in range(var_epoch_tot):
    
  #now new episode start from here
    var_list_episode = list()
	


    #First Observation will be Reset and return
    observation = environment.reset(exploring_starts=True) 	

    for _ in range(1000):
        
    # Now we will take the action from the matrix action
        var_actions_ = var_matrix_policy[var_obser_[0], var_obser_[1]]

        # Now the agent will move one step and notice the observation and reward from the environment
        var_obser_, var_rewards_, var_done_ =  environment.step(var_actions_)

        # Include that visit into the list of episode
        var_list_episode.append((var_obser_, var_rewards_))
        if var_done_: break

    # Here the episode is completed, now we will estimate the utilities
    var_count_ = 0

    # We will check here that is this the first visit in the state
    var_matrix_checkup = _numP_.zeros((3,4))

    # Now we are going to implement the First visit Monte Carlo method
    # And for all the states it is store it in the list of episodes and check if it is first visit and estimate the returns.

    for var_visit_ in var_list_episode:
        var_obser_ = var_visit_[0]
        var_row_ = var_obser_[0]
        var_col_ = var_obser_[1]
        var_rewards_ = var_visit_[1]

        if(var_matrix_checkup[var_row_, var_col_] == 0):
            return_value = fuc_return_get(var_list_episode[var_count_:], par_gamma_df)
            var_matrix_mean_running[var_row_, var_col_] += 1
            var_matrix_utility_[var_row_, var_col_] += return_value
            var_matrix_checkup[var_row_, var_col_] = 1
        var_count_ += 1

    if(var_epoch_ % var_epoch_print == 0):
        print("Matrix utility later " + str(var_epoch_+1) + " no of iterations:") 
        print(var_matrix_utility_ / var_matrix_mean_running)

#Finally we will check the mstrix utility received
print("Matrix utility later " + str(var_epoch_tot) + " no of iterations:")
print(var_matrix_utility_ / var_matrix_mean_running)


#Import python scientific libraries
import numpy as np

#First we create list of all the states

def meth_State_Space_Init():

    var_States_ = []
  
    for var_Card_ in range(1,11):
    
     for var_Value_ in range(11,22):
        
      var_States_.append((var_Value_, False, var_Card_))
      var_States_.append((var_Value_, True, var_Card_))

    return var_States_


  

#Now we are going to create a key value pair dictionary 
#for all the possible action-state and the values

#Below method will create a Q look up table


def meth_State_Actions_Init(var_States_):

    var_av_ = {}
  
    for var_State_ in var_States_:
  
        var_av_[(var_State_, 0)] = 0.0
        var_av_[(var_State_, 1)] = 0.0
    
    return var_av_

  
#Now we will set-up a dictionary that contains 
#all the actions-state to capture the record


def math_S_Account_Init(stateActions):
    var_Counts_ = {}
    for var_sa_ in stateActions:
        var_Counts_[var_sa_] = 0
    return var_Counts_

  
#Now we will write a code that calculate our reward, 
#it is +1 for winning a game
#-1 for losing a game
#0 for tie a game


#We will substract it with 3 to get the value

def math_Reward_Calc(parm_Outcome_):

    return 3-parm_Outcome_

  
#Now this function will recalculate the reward average in the Q lookup table

def meth_QTable_Update(var_Table_Average, var_Count_Average_, returns):

    for var_Key_ in returns:

     var_Table_Average[var_Key_] = var_Table_Average[var_Key_] + (1.0 / var_Count_Average_[var_Key_]) * (returns[var_Key_]- var_Table_Average[var_Key_])

    return var_Table_Average
    

    
#This value returning a Q value or average rewards for all the states

def meth_QValue_Reward_Average(var_State_, var_Table_Average):

    var_Stay_ = var_Table_Average[(var_State_,0)]
    var_Hit_ = var_Table_Average[(var_State_,1)]

    return numP.array([var_Stay_, var_Hit_])

  
  
#Now we convert the state of the game to ((ace total , player) 
#and (ace total, dealer), status)

def getRLstate(var_State_):

    var_Hand_Player_, var_Hand_Dealer, status = var_State_

    player_val, var_Ace_Player_ = var_Hand_Player_

    return (player_val, var_Ace_Player_, var_Hand_Dealer[0])
	
	
	
	
	
	
	
	
#Now we set the value for number of run
#It just take 1-2 minutes to run 

var_epochs_ = 5000000 
var_Eepsilon_ = 0.1

var_Space_State_ = meth_State_Space_Init()

var_Table_Average = meth_State_Actions_Init(var_Space_State_)

var_Count_Average_ = math_S_Account_Init(var_Table_Average)

for var_i_ in range(var_epochs_):

    #Now we will initialize a new game
    var_State_ = meth_Game_Init()
  
    var_Hand_Player_, var_Hand_Dealer, var_Status_ = var_State_
    
  #Now check if player total card value is less then 11, so will add another card
    #because the total is less then 11 thats why we give another card
       
   
    while var_Hand_Player_[0] < 11:
        
        var_Hand_Player_ = add_card(var_Hand_Player_, meth_var_Card__Random_())
    
        var_State_ = (var_Hand_Player_, var_Hand_Dealer, var_Status_)
    
        var_State_RL = getRLstate(var_State_) 
    
  
    #Now set-up to temp hold action-state for current episode
    
  #return, action, state
  
    var_Returns_ = {} 
  
    while(var_State_[2] == 1): 
        
        var_Probabilities_Actions = meth_QValue_Reward_Average(var_State_RL, var_Table_Average)
        if (random.random() < var_Eepsilon_):
        
         var_Actions_ = random.randint(0,1)
        
    else:
            var_Actions_ = np.argmax(var_Probabilities_Actions)
        
            var_sa_ = ((var_State_RL, var_Actions_))
    
            var_Returns_[var_sa_] = 0 
    
    #For average calculation we increment the counter
    
            var_Count_Average_[var_sa_] += 1 
        
    #Start the game now 
    
    var_State_ = meth_Play_(var_State_, var_Actions_) 
        
    var_State_RL = getRLstate(var_State_)
    
  
  #Now once an episode complete then reward will be assign to all the actions-state
  
    for var_key_ in var_Returns_: 
  
        var_Returns_[var_key_] = math_Reward_Calc(var_State_[2])
    
        var_Table_Average = updateQtable(var_Table_Average, var_Count_Average_, var_Returns_)
  
print("Complete...") 
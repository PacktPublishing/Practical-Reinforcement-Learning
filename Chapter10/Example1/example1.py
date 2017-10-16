#import all the required libraries
import scipy
import logging
import numpy as numP


#Reinforcement learning test agent dependency
import playing as _Library_play_
#from playing import _Library_play_ 

#now we will construct the neural network
from nn import neural_net 

from cvxopt import _matrix_nn 

#optimization convex library
from cvxopt import _solvers_CVX_ 

# environment dependencies will be added here
from flat_game import _munk_Car_ 

# Now we define the reinforcement learner
from learning import _helper_IRL_ 

_var_States_Num_ = 8 

# brown/yellow/bumping/red
var_behavior_ = 'red' 

# For each iterations we will define the number of training frames
var_Frame_ = 100000


class IRLAgent:
 
 
 def __init__(_self, _parm_FE_random_, _expertFE, _parm_Epsilon_, _parm_States_num_, _parm_Frames_, _parm_behavior_):
  _self.var_Policy_Random = _parm_FE_random_
  _self._var_Policy_Expert = _expertFE
  _self._var_States_Num_ = _parm_States_num_
  _self.var_Frame_ = _parm_Frames_
  _self.var_behavior_ = _parm_behavior_

# when t<0.1 then terminate
 _self._var_Epsilon_ = _parm_Epsilon_


 _self._var_T_Random_ = numP.linalg.norm(numP.asarray(_self._var_Policy_Expert)-numP.asarray(_self.var_Policy_Random)) 

# Here we will store the t value and policy
 _self.policiesFE = {_self._var_T_Random_:_self.var_Policy_Random} 
 print ("Expert Policy - Random Start (t) :: " , _self._var_T_Random_) 
 _self._var_T_Current_ = _self._var_T_Random_
 _self.minimumT = _self._var_T_Random_
 
 
 
 #Using Reinforcement learning agent we will get the expectations and new policy
def _func_Get_AgentFE_(self, W, i): 

# Now we will train the agent and save the model in a file
 _helper_IRL_(W, self.var_behavior_, self.var_Frame_, i) 

# We will get the feature expectations (FE) from the saved model
 var_Model_Save = 'saved-models_'+self.var_behavior_+'/evaluatedPolicies/'+str(i)+'_2000_iterations-'+str(self.var_Frame_)+'.h5' 
 
 var_Model_ = _neural_network_(self._var_States_Num_, [164, 150], var_Model_Save)


 #It return the FE by executing the policy learned
 return _Library_play_(var_Model_, W)

 
 #now add the feature expectation policy list and its differences
 def _func_List_Updater_Policy_(self, W, i): 

# Here get the FE of a new policy corresponding to the input weights
  _var_FE_Temp = self._func_Get_AgentFE_(W, i) 

# t = _var_Hyper_Distance
  _var_Hyper_Distance = numP.abs(numP.dot(W, numP.asarray(self._var_Policy_Expert)-numP.asarray(_var_FE_Temp))) 

  self.policiesFE[_var_Hyper_Distance] = _var_FE_Temp
 return _var_Hyper_Distance 

 
 
def func_Weight_Finder_Optimal(self):
 
 f = open('weights-'+var_behavior_+'.txt', 'w')
 i = 1
 
 while True:

# In the list of episode find a new weight for optimization
  W = self.func_Optimize() 

 print ("weights ::", W )
 f.write( str(W) )
 f.write('\n')
 print ("Now the total distances :", self.policiesFE.keys())
 self._var_T_Current_ = self._func_List_Updater_Policy_(W, i)
 print ("The Current distance is: ", self._var_T_Current_ )

# If the point reached to close enough then terminate
 
 i += 1
 
 f.close()
 
 return W
 
 
 
  # As an SVM problem implement the convex optimization
 
def func_Optimize(self): 
 
 var_m_ = len(self._var_Policy_Expert)
 var_P_ = _matrix_nn(2.0*numP.eye(var_m_), var_tc_='d') 
 var_Q_ = _matrix_nn(numP.zeros(var_m_), var_tc_='d')
 var_List_Policy = [self._var_Policy_Expert]
 var_List_H = [1]
 
 for i in self.policiesFE.keys():
 
  var_List_Policy.append(self.policiesFE[i])
 
  var_List_H.append(1)
 
  var_Mat_Policy_ = numP._matrix_nn(var_List_Policy)
 
  var_Mat_Policy_[0] = -1*var_Mat_Policy_[0]
 
  var_G_ = _matrix_nn(var_Mat_Policy_, var_tc_='d')
 
  var_H_ = _matrix_nn(-numP.array(var_List_H), var_tc_='d')
 
  sol = _solvers_CVX_.qp(var_P_,var_Q_,var_G_,var_H_)

  weights = numP.squeeze(numP.asarray(sol['x']))
  norm = numP.linalg.norm(weights)
  weights = weights/norm
 return weights 
 
 
 
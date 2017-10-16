
#First import all the required libraries

from __future__ import imp_Function_Print

import argparse as imp_parse_
import skimage as imp_skimage_
from skimage import transform, color, exposure
from skimage.transform import rotate
from skimage.viewer import ImageViewer

# We include the sys libraries here
import sys
sys.path.append("game/")

# The game flappy bird libraries included here
import wrapped_flappy_bird as imp_Game_

# We include the random function libraries here
import random

# All the scientific libraries include here
import numpy as numP

# Now include the collection libraries
from collections import deque as imp_DQ

#Also include the JSON libraries here
import json

#Here we will use the keras libraries
from keras import initializations
from keras.initializations import normal, identity
from keras.models import model_from_json
from keras.models import Sequential

from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD as imp_SGD_ , Adam as imp_Adam_


#Now we will use the import the tensor flow libraries
import tensorflow as imp_ten_Flow

var_Game_ = 'bird' # It is the game name that we store it in log file

_var_Config_ = 'nothreshold'
_var_Actions_ = 2 # no. of valid actions
_var_Gama_ = 0.99 
_var_Observation_ = 3200. 

_var_Explore_ = 3000000. 
_var_Epsilon_Final_ = 0.0001 
_var_Epsilon_initital_ = 0.1 
_var_Replay_Memory_ = 50000 
_var_Batch_ = 32 
_var_Action_Per_Frame_ = 1
_var_Learning_Rate_ = 1e-4

_var_Image_Rows_ , _var_Image_Columns_ = 80, 80

#Black and white image convertion 

_var_Image_Channels_ = 4 #We stack 4 frames

def func_Build_Model_():

 print("Now we build the model")
 var_Build_Models_ = Sequential()
 var_Build_Models_.add(Convolution2D(32, 8, 8, subsample=(4, 4), border_mode='same',input_shape=(_var_Image_Rows_,_var_Image_Columns_,_var_Image_Channels_))) #80*80*4

 var_Build_Models_.add(Activation('relu'))
 var_Build_Models_.add(Convolution2D(64, 4, 4, subsample=(2, 2), border_mode='same'))
 var_Build_Models_.add(Activation('relu'))
 var_Build_Models_.add(Convolution2D(64, 3, 3, subsample=(1, 1), border_mode='same'))

 var_Build_Models_.add(Activation('relu'))
 var_Build_Models_.add(Flatten())
 var_Build_Models_.add(Dense(512))
 var_Build_Models_.add(Activation('relu'))
 var_Build_Models_.add(Dense(2))
 
 var_Adam_ = imp_Adam_(lr=_var_Learning_Rate_)
 var_Build_Models_.compile(_var_Loss_='mse',optimizer=var_Adam_)
 
 print("We completed building the model")
 return var_Build_Models_



 def func_Train_Network(var_Build_Models_,parm_Args_):
 
 # We will open the game now on the emulator
  var_State_Game_ = imp_Game_.GameState()

# We will store the old observations into the replay memory
  var_D_ = imp_DQ()


 # Now we will get the first image and then pre-process the image to 80 x 80 x 4
 var_Do_Nothing_ = numP.zeros(_var_Actions_)
 var_Do_Nothing_[0] = 1
 var_X_T_, var_R_0_, var_Terminal_ = var_State_Game_.frame_step(var_Do_Nothing_)

 var_X_T_ = imp_skimage_.color.rgb2gray(var_X_T_)
 var_X_T_ = imp_skimage_.transform.resize(var_X_T_,(80,80))
 var_X_T_ = imp_skimage_.exposure.rescale_intensity(var_X_T_,out_range=(0,255))


 var_S_T_ = numP.stack((var_X_T_, var_X_T_, var_X_T_, var_X_T_), axis=2)
 
#Now we will use Keras library to reshape it.
 var_S_T_ = var_S_T_.reshape(1, var_S_T_.shape[0], var_S_T_.shape[1], var_S_T_.shape[2]) #1*80*80*4

if parm_Args_['mode'] == 'Run':
 
 _var_Observe_ = 999999999 #We keep _var_Observe_, never train
 _var_Epsilon_ = _var_Epsilon_Final_
 print ("Now we are going to load the weight")
 var_Build_Models_.load_weights("model.h5")
 var_Adam_ = imp_Adam_(lr=_var_Learning_Rate_)
 var_Build_Models_.compile(_var_Loss_='mse',optimizer=var_Adam_)
 print ("Here the load weight successful.") 
 
else: #Now we are going to training mode
 _var_Observe_ = _var_Observation_
 _var_Epsilon_ = _var_Epsilon_initital_

_vat_T_ = 0

while (True):
 _var_Loss_ = 0
 _var_Q_sa__ = 0
 _var_Index_Action_ = 0
 _var_R_T_ = 0
 _var_A_T_ = numP.zeros([_var_Actions_])
 
 #Now we will choose an action
if _vat_T_ % _var_Action_Per_Frame_ == 0:
 
 if random.random() <= _var_Epsilon_:
 
  print("----------Take Random Action----------")
 
  _var_Index_Action_ = random.randrange(_var_Actions_)
 
  _var_A_T_[_var_Index_Action_] = 1
 
 else:
 
 #Now from the input stack of 4 images, we will do the prediction here
  q = var_Build_Models_.predict(var_S_T_) 
  _var_Max_Q_ = numP.argmax(q)
  _var_Index_Action_ = _var_Max_Q_
  _var_A_T_[_var_Max_Q_] = 1

#Now we will be reducing the epsilon gradually
 if _var_Epsilon_ > _var_Epsilon_Final_ and _vat_T_ > _var_Observe_:
  _var_Epsilon_ -= (_var_Epsilon_initital_ - _var_Epsilon_Final_) / _var_Explore_

#Now we will run the chosen action and observed next reward and state
 _var_X_T1_Color, _var_R_T_, var_Terminal_ = var_State_Game_.frame_step(_var_A_T_)

 _var_X_T1_ = imp_skimage_.color.rgb2gray(_var_X_T1_Color)
 _var_X_T1_ = imp_skimage_.transform.resize(_var_X_T1_,(80,80))
 _var_X_T1_ = imp_skimage_.exposure.rescale_intensity(_var_X_T1_, out_range=(0, 255))

 #1x80x80x1
_var_X_T1_ = _var_X_T1_.reshape(1, _var_X_T1_.shape[0], _var_X_T1_.shape[1], 1) 
_var_S_T1_ = numP.append(_var_X_T1_, var_S_T_[:, :, :, :3], axis=3)

# store the transition in var_D_
var_D_.append((var_S_T_, _var_Index_Action_, _var_R_T_, _var_S_T1_, var_Terminal_))
 
if len(var_D_) > _var_Replay_Memory_:
 var_D_.popleft()

#If done ovserving then only do a training
 if _vat_T_ > _var_Observe_:
  _var_Mini_Batch_ = random.sample(var_D_, _var_Batch_)

 #32, 80, 80, 4
_var_Inputs_ = numP.zeros((_var_Batch_, var_S_T_.shape[1], var_S_T_.shape[2], var_S_T_.shape[3])) 
 
print (_var_Inputs_.shape)
 
_var_Targets_ = numP.zeros((_var_Inputs_.shape[0], _var_Actions_)) 

#Now we will do the experience replay
 
for i in range(0, len(_var_Mini_Batch_)):
 
 _var_State_T_ = _var_Mini_Batch_[i][0]


 #index action
 _var_Action_T_ = _var_Mini_Batch_[i][1] 
 _var_Reward_T_ = _var_Mini_Batch_[i][2]
 _var_State_T1_ = _var_Mini_Batch_[i][3]
 var_Terminal_ = _var_Mini_Batch_[i][4]


#saved down var_S_T_
_var_Inputs_[i:i + 1] = _var_State_T_ 

# Now we will hit the probability of each 
_var_Targets_[i] = var_Build_Models_.predict(_var_State_T_) 
_var_Q_sa__ = var_Build_Models_.predict(_var_State_T1_)

if var_Terminal_:
 _var_Targets_[i, _var_Action_T_] = _var_Reward_T_
else:
 _var_Targets_[i, _var_Action_T_] = _var_Reward_T_ + _var_Gama_ * numP.max(_var_Q_sa__)


 _var_Loss_ += var_Build_Models_.train_on_batch(_var_Inputs_, _var_Targets_)

var_S_T_ = _var_S_T1_
_vat_T_ = _vat_T_ + 1

# save the progress for every 10000 iterations
if _vat_T_ % 1000 == 0:
 
 print("Now we will save the model")
 var_Build_Models_.save_weights("var_Build_Models_.h5", overwrite=True)
 with open("var_Build_Models_.json", "w") as outfile:
  json.dump(var_Build_Models_.to_json(), outfile)

# Here we will print all the information
 _var_State_ = ""
 if _vat_T_ <= _var_Observe_:
  _var_State_ = "observe"
 elif _vat_T_ > _var_Observe_ and _vat_T_ <= _var_Observe_ + _var_Explore_:
  _var_State_ = "explore"
 else:
  _var_State_ = "train"

print("TIMESTEP", _vat_T_, "/ STATE", _var_State_, \
 "/ EPSILON", _var_Epsilon_, "/ ACTION", _var_Index_Action_, "/ REWARD", _var_R_T_, \
 "/ Q_MAX " , numP.max(_var_Q_sa__), "/ Loss ", _var_Loss_)

print("Finally here our episode finished")
print("-------------------------------")


def func_Game_Play_(parm_Args_):
 var_Build_Models_ = func_Build_Model_()
 func_Train_Network(var_Build_Models_,parm_Args_)

def func_Main_():
 parser = imp_parse_.ArgumentParser(description='Description of your program')
 parser.add_argument('-m','--mode', help='Train / Run', required=True)
 parm_Args_ = vars(parser.parse_args())
 func_Game_Play_(parm_Args_)

if __name__ == "__main__":
 _var_Config_ = imp_ten_Flow.ConfigProto()
 _var_Config_.gpu_options.allow_growth = True
 _var_Sess_ = imp_ten_Flow.Session(config=_var_Config_)
 from keras import backend as imp_Ks_
 imp_Ks_.set_session(_var_Sess_)
 func_Main_()

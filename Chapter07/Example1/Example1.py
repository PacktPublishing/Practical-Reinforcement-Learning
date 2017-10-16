# provides access to reinforcement algorithms and other environments
import gym

# provides mathematical fucntions
import math

# provides access to random module and its fucntions
import random

# provides support for multidimension arrays, metrices, high level mathematical fucntions
import numpy as numP

# provides matlab style functions
import matplotlib

# provides matlab style functions
import matplotlib.pyplot as imp_Plt_

# provides access to dictionaries
from collections import namedtuple 

# provide access to efficient looping
from itertools import count 

# provides access to copying list
from copy import deepcopy 

#defined the image module
from PIL import Image 


# provides access to Tensor computation and Deep Neural Networks
import torch

#provides easier way to build and train models for Neural Networks
import torch.nn as imp_nn_

#Numerical Package for torch Deep Neural Networks
import torch.optim as imp_Optim_

#Functional interface for Neural Networks
import torch.nn.functional as imp_F_

#provide automatic differentiation
from torch.autograd import imp_Variable_

#provides access to models,image,video datasets for torch Deep Neural Networks
import torchvision.transforms as imp_T_


var_Environment_ = gym.make('CartPole-v0').unwrapped

# set up matplotlib

var_is_ipython_ = 'inline' in matplotlib.get_backend()


if var_is_ipython_:
    from IPython import var_Display_

  
imp_Plt_.ion()


# if we are using gpu

var_Cuda_Use_ = torch.cuda.is_available()

var_Tensor_Floar_ = torch.cuda.var_Tensor_Floar_ if var_Cuda_Use_ else torch.var_Tensor_Floar_

var_Tensor_Long_ = torch.cuda.var_Tensor_Long_ if var_Cuda_Use_ else torch.var_Tensor_Long_

var_Tensor_Byte_ = torch.cuda.var_Tensor_Byte_ if var_Cuda_Use_ else torch.var_Tensor_Byte_

var_Tensor_ = var_Tensor_Floar_




var_Transition_ = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class cls_Memory_Replay(object):

    def __init__(self, parm_Capacity):
        self.var_Capacity_ = parm_Capacity
        self.var_Memory_ = []
        self.var_Position_ = 0

    def func_Push(self, *args):
        
    
        
     if len(self.var_Memory_) < self.var_Capacity_:
          self.var_Memory_.append(None)
          self.var_Memory_[self.var_Position_] = Transition(*args)
          self.var_Position_ = (self.var_Position_ + 1) % self.var_Capacity_
	 
    

    def func_Sample(self, var_Size_Batch_):
        return random.func_Sample(self.var_Memory_, var_Size_Batch_)
    

    def __len__(self):
        return len(self.var_Memory_)  
		
		
		
class cls_DQN_(imp_nn_.Module):


    def __init__(self):
        super(cls_DQN_, self).__init__()
        self.var_conv1_ = imp_nn_.Conv2d(3, 16, kernel_size=5, stride=2)
        self.var_bn1_ = imp_nn_.BatchNorm2d(16)
        self.var_Conv2_ = imp_nn_.Conv2d(16, 32, kernel_size=5, stride=2)
        self.var_Bn2_ = imp_nn_.BatchNorm2d(32)
        self.var_Conv3_ = imp_nn_.Conv2d(32, 32, kernel_size=5, stride=2)
        self.var_Bn3_ = imp_nn_.BatchNorm2d(32)
        self.var_Head_ = imp_nn_.Linear(448, 2)
    
    

    def forward(self, parm_x_):
        var_x_ = imp_F_.relu(self.var_bn1_(self.var_conv1_(parm_x_)))
        var_x_ = imp_F_.relu(self.var_Bn2_(self.var_Conv2_(parm_x_)))
        var_x_ = imp_F_.relu(self.var_Bn3_(self.var_Conv3_(parm_x_)))
    
        return self.var_Head_(var_x_.view(var_x_.size(0), -1))
		
		
		

var_Resize_ = imp_T_.Compose([imp_T_.ToPILImage(),
                    imp_T_.Scale(40, interpolation=imp_Image_.CUBIC),
                    imp_T_.ToTensor()])


var_Width_Screen = 600


def func_Get_Location_Cart_():
    var_Width_World_ = var_Environment_.x_threshold * 2
    var_Scale_ = var_Width_Screen / var_Width_World_
    return int(var_Environment_.var_State_[0] * var_Scale_ + var_Width_Screen / 2.0) 


def func_Get_Screen_():

    var_Screen_ = var_Environment_.render(mode='rgb_array').transpose(
        (2, 0, 1)) 


    var_Screen_ = var_Screen_[:, 160:320]
    var_Width_View_ = 320
    var_Location_Cart = func_Get_Location_Cart_()

    if var_Location_Cart < var_Width_View_ // 2:
        var_Range_Slice_ = slice(var_Width_View_)

    elif var_Location_Cart > (var_Width_Screen - var_Width_View_ // 2):
        var_Range_Slice_ = slice(-var_Width_View_, None)

    else:
        var_Range_Slice_ = slice(var_Location_Cart - var_Width_View_ // 2,
                            var_Location_Cart + var_Width_View_ // 2)


    var_Screen_ = var_Screen_[:, :, var_Range_Slice_]
   
    var_Screen_ = numP.ascontiguousarray(var_Screen_, dtype=numP.float32) / 255
 
    var_Screen_ = torch.from_numpy(var_Screen_)
   
   
    return resize(var_Screen_).unsqueeze(0).type(var_Tensor_)

var_Environment_.reset()

imp_Plt_.figure()

imp_Plt_.imshow(func_Get_Screen_().cpu().squeeze(0).permute(1, 2, 0).numpy(),
           interpolation='none')

imp_Plt_.title('Example extracted screen')

imp_Plt_.show()













var_Size_Batch_ = 128
var_Gamma_ = 0.999
var_Start_EPS_ = 0.9
var_End_EPS_ = 0.05
var_Decay_EPS_ = 200

var_Model_ = cls_DQN_()

if var_Cuda_Use_:
    var_Model_.cuda()

var_Optimizer_ = imp_Optim_.RMSprop(var_Model_.parameters())
var_Memory_ = cls_Memory_Replay(10000)


var_Done_Steps = 0


def func_Action_Select_(var_State_):
    global var_Done_Steps
    var_Sample_ = random.random()
    var_Threshold_EPS_ = var_End_EPS_ + (var_Start_EPS_ - var_End_EPS_) * \
        math.exp(-1. * var_Done_Steps / var_Decay_EPS_)
    var_Done_Steps += 1
  
    if var_Sample_ > var_Threshold_EPS_:
    
        return model(
            Variable(var_State_, volatile=True).type(var_Tensor_Floar_)).data.max(1)[1].view(1, 1)
    
    else:
    
        return var_Tensor_Long_([[random.randrange(2)]])


_var_Durations_Episode_ = []


def func_Durations_Plot_():

    imp_Plt_.figure(2)
    imp_Plt_.clf()
    vat_T_Durations = torch.FloatTensor(_var_Durations_Episode_)
    imp_Plt_.title('Training...')
    imp_Plt_.xlabel('Episode')
    imp_Plt_.ylabel('Duration')
    imp_Plt_.plot(vat_T_Durations.numpy())
    
  
    if len(vat_T_Durations) >= 100:
        var_Means_ = vat_T_Durations.unfold(0, 100, 1).mean(1).view(-1)
        var_Means_ = torch.cat((torch.zeros(99), var_Means_))
        imp_Plt_.plot(var_Means_.numpy())

    imp_Plt_.pause(0.001) 
  
    if var_is_ipython_:
        var_Display_.clear_output(wait=True)
        var_Display_.display(imp_Plt_.gcf())
		
		
		
		
		
		
var_Sync_Last = 0


def func_Model_Optimize_():

    global var_Sync_Last
    if len(var_Memory_) < var_Size_Batch_:
        return
    _var_Transitions_ = var_Memory_.func_Sample(var_Size_Batch_)
    
    _var_Batch_ = Transition(*zip(*_var_Transitions_))

    
    _var_Mask_Non_Final_ = var_Tensor_Byte_(tuple(map(lambda s: s is not None,
                                          _var_Batch_.var_State_Next_)))

    
  
    var_Next_States_Final_ = Variable(torch.cat([s for s in _var_Batch_.var_State_Next_
                                                if s is not None]),
                                     volatile=True)
                   
    var_Batch_State_ = Variable(torch.cat(_var_Batch_.state))
    var_Batch_State_ = Variable(torch.cat(_var_Batch_.action))
    var_Batch_Reward_ = Variable(torch.cat(_var_Batch_.reward))

    
    var_Values_Action_ = model(var_Batch_State_).gather(1, var_Batch_State_)

    
    _var_Values_Next_State_ = Variable(torch.zeros(var_Size_Batch_).type(var_Tensor_))
    _var_Values_Next_State_[_var_Mask_Non_Final_] = model(var_Next_States_Final_).max(1)[0]
    
    _var_Values_Next_State_.volatile = False
    
  
    var_State_Expected_Values_Actions_ = (_var_Values_Next_State_ * var_Gamma_) + var_Batch_Reward_

    
    _var_loss_ = imp_F_.smooth_l1_loss(var_Values_Action_, var_State_Expected_Values_Actions_)

    
    var_Optimizer_.zero_grad()
  
    _var_loss_.backward()
    
    for var_Param_ in model.parameters():
        var_Param_.grad.data.clamp_(-1, 1)
    
        var_Optimizer_.step()  
		

		
		
		
		
		
		
		
		
var_Episode_Num_ = 10
for var_Episode_i_ in range(var_Episode_Num_):
    
    var_Environment_.reset()
    var_Screen_Last_ = func_Get_Screen_()
    var_Screen_Current_ = func_Get_Screen_()
    var_State_ = var_Screen_Current_ - var_Screen_Last_
    
    for var_T_ in count():
        
        var_Action_ = func_Action_Select_(var_State_)
        _, var_Reward_, var_Done_, _ = var_Environment_.step(var_Action_[0, 0])
        var_Reward_ = Tensor([var_Reward_])

        
        var_Screen_Last_ = var_Screen_Current_
        var_Screen_Current_ = func_Get_Screen_()
        if not var_Done_:
            var_State_Next_ = var_Screen_Current_ - var_Screen_Last_
        else:
            var_State_Next_ = None

        
        var_Memory_.func_Push(var_State_, var_Action_, var_State_Next_, var_Reward_)

        
        var_State_ = var_State_Next_

        
        func_Model_Optimize_()
        if var_Done_:
            _var_Durations_Episode_.append(var_T_ + 1)
            func_Durations_Plot_()
            break

print('Complete')
var_Environment_.render(close=True)
var_Environment_.close()
imp_Plt_.ioff()
imp_Plt_.show()
    
    
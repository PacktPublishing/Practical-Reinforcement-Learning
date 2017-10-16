import sys
import gym

#In this program we will do the test
#for learning agent,
#and environment name through command line

environment = gym.make('LunarLander-v2'
if len(sys.argv) < 2
else sys.argv[1])

if not hasattr(environment.action_space, 'n') : raise Exception('The agent only supporting the discrete action space')

PERFORM_ACTION = environment.action_space.n

_ROLLINGOUT_TIME = 1000

CONTROL_SKIP = 0

#we can test is the skip is still usable ?

_action_agent_human_ = 0
_restart_want_human_ = False
_pause_set_human_ = False

def _key_pressed_(_key_pressed, mod) : 
 global _action_agent_human_,_restart_want_human_,_pause_set_human_
if _key_pressed == 0xff0d: 
 _restart_want_human_ = True
if _key_pressed == 32 : 
 _pause_set_human_ = not _pause_set_human_ 
 aaa = int(_key_pressed - ord('0')) 


def _key_released_(_key_pressed, mod) : global _action_agent_human_
aaa = int(_key_pressed - ord('0'))
if _action_agent_human_ == aaa: _action_agent_human_ = 0

environment.render()
environment.unwrapped.viewer.window.on__key_press_ = _key_pressed_
environment.unwrapped.viewer.window.on__key_release_ = _key_released_

def _rollingout_(environment) : 
 global _action_agent_human_, _restart_want_human_, _pause_set_human_
 _restart_want_human_ = False

 observation = environment.reset()
 skip = 0
 for t in range(_ROLLINGOUT_TIME) : 
  if not skip: 
   aaa = _action_agent_human_ 
   skip = CONTROL_SKIP
  else: skip -= 1

 observation, r, _done_, 
 info = environment.step(aaa)
 environment.render()


if _restart_want_human_: break
while _pause_set_human_: environment.render()

#Now importing the time libraries
import time

time.sleep(0.1)

print("PERFORM_ACTION={}".format(PERFORM_ACTION))
print("Please press one of the following keys 1, 2 or 3 and it take PERFORM_ACTION 1 or 2 or 3 ...")
print("if you did not press any keys then it takes an action 0")

while 1 : _rollingout_(environment)
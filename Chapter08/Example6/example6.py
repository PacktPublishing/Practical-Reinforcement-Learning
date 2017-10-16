import argparse
import logging
import sys
import gym
from gym import wrappers

class RandomAgent(object) :

#It is the world simplest agent

 def __init__(self_Agent, action_state_space) : self_Agent.action_space = action_state_space

 def act(self_Agent, observations, rewards, complete) : return self_Agent.action_space.sample()

 if __name__ == '__main__': parser = argparse.ArgumentParser(description = None) 
 parser.add_argument('env_id', nargs = '?', default = 'CartPole-v0', help = 'Select which environment you want to run')

 argument = parser.parse_args() 

  # We need to call the method undo_logger_setup , it will undo the
  # Gym's logger setup and we need to configure it manually
  # If we dont call it then most of of the time default should be fine 

 gym.undo_logger_setup()

 logger_Details = logging.getLogger()
 formating = logging.Formatter('[%(asctime)s] %(message)s')

 handling = logging.StreamHandler(sys.stderr)

 handling.setFormatter(formating)

 logger_Details.addHandler(handling)

  #We can setup the level to logging.WARN or logging.DEBUG
  #if we want it to change the amount of output.

 logging.setLevel(logging.INFO)
 environment = gym.make(argument.env_id)

  #We need to provide the output directory to write(It can be an#existing directory, we are including one with existing data.#Kindly notr that all files must be with namespaced).We can also put it to to temporary#directory

 outdir = '/tmp/results_agent'
 environment = wrappers.Monitor(env, directory = outdir, force = True)
 environment.seed(0)
 agent = RandomAgent(environment.action_space)
 episode_count = 100
 rewards = 0
 complete = False

 for i in range(episode_count) : ob = environment.reset()
 while True: action = agent.act(ob, rewards, complete)
 ob,
 rewards,
 complete,
 _ = environment.step(action)
 
  #Note there 's no environment.render() here. 
            # But the environment still can open window and
            # render if asked by environment.monitor: it calls environment.render('rgb_array ') 
            # to record video.
            # Video is not recorded every episode, see capped_cubic_video_schedule for details.
            # Close the environment and write monitor result info to disk
 environment.close()

    # Upload to the scoreboard. We could also do this from another
    # process if we wanted.

 logger.info("Successfully ran RandomAgent. Now trying to upload results to the scoreboard. If it breaks, you can always just try re-uploading the same results.")
    
 gym.upload(outdir)
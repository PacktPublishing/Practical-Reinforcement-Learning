package project;

//Required java libraries
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.List;

//Now we will import all the BURLAP libraries, 
//there are lot of them to implement and it ease all our development
import burlap.behavior.policy.EpsilonGreedy;

//This library is related to implement policies
import burlap.behavior.policy.Policy;

//This library is related to implement Utitlities policies
import burlap.behavior.policy.PolicyUtils;

//This library is related to implement Single agent and episodic
import burlap.behavior.singleagent.Episode;

//This library is related to implement MDP
import burlap.behavior.singleagent.MDPSolver;

//This library is related to implement Episode Visualizer
import burlap.behavior.singleagent.auxiliary.EpisodeSequenceVisualizer;

//This library is related to Learning Agent
import burlap.behavior.singleagent.learning.LearningAgent;


//This library is related to implement States in MDP
import burlap.behavior.singleagent.auxiliary.StateReachability;

//This library is related to implement Single agent planner
import burlap.behavior.singleagent.planning.Planner;

//This library is related to implement Value fuctions constants
import burlap.behavior.valuefunction.ConstantValueFunction;

//This library is related to implement Q Provider
import burlap.behavior.valuefunction.QProvider;

//This library is related to implement Q Value
import burlap.behavior.valuefunction.QValue;

//This library is related to implement Value function
import burlap.behavior.valuefunction.ValueFunction;

//This library is related to implement Grid world
import burlap.domain.singleagent.gridworld.GridWorldDomain;

//This library is related to implement Grid world terminal function
import burlap.domain.singleagent.gridworld.GridWorldTerminalFunction;

//This library is related to implement Grid World visualization
import burlap.domain.singleagent.gridworld.GridWorldVisualizer;

//This library is related to implement Grid Agent
import burlap.domain.singleagent.gridworld.state.GridAgent;

//This library is related to implement states in Grid World
import burlap.domain.singleagent.gridworld.state.GridWorldState;

//This library is related to implement actions
import burlap.mdp.core.action.Action;

//This library is related to implement states
import burlap.mdp.core.state.State;

//This library is related to implement SA Domain
import burlap.mdp.singleagent.SADomain;

//This library is related to implement full model
import burlap.mdp.singleagent.model.FullModel;

//This library is related to implement transition probabilities
import burlap.mdp.singleagent.model.TransitionProb;

//This library is related to implement hashable states
import burlap.statehashing.HashableState;

//This library is related to implement hashable state factory
import burlap.statehashing.HashableStateFactory;

//This library is related to implement simple hashable state factory
import burlap.statehashing.simple.SimpleHashableStateFactory;

//This library is related to implement visualization
import burlap.visualizer.Visualizer;

//These libraries are related to Environment
import burlap.mdp.singleagent.environment.Environment;
import burlap.mdp.singleagent.environment.EnvironmentOutcome;
import burlap.mdp.singleagent.environment.SimulatedEnvironment;


//This library is related to QFunction
import burlap.behavior.valuefunction.QFunction;




public class QLearningTutorial extends MDPSolver implements QProvider, LearningAgent {

            

       
		
		
		Map<HashableState, List<QValue>> _q_Values_;

		QFunction _initQ_;

		double _learn_Rate_;

		Policy _learn_Policy_;


		public QLearningTutorial(SADomain domain_sa, double
		  _gamma_discount_factor, HashableStateFactory factoryHash, QFunction
		  _initQ_, double _learn_Rate_, double _eps_)
			  {

				this.solverInit(domain_sa, _gamma_discount_factor,
				  factoryHash);

				this._initQ_ = _initQ_;

				this._learn_Rate_ = _learn_Rate_;

				this._q_Values_ = new HashMap<HashableState, List<QValue>>();

				this._learn_Policy_ = new EpsilonGreedy(this, _eps_);

				}
				
				
				
				
 @Override
    public List<QValue> qValues(State st) 
    {
        //get the hashed state first
        HashableState hashSt = this.hashingFactory.hashState(st);

        //We will check if it is stored the values already
        List<QValue> qValueSt = this._q_Values_.get(hashSt);

        //If we dont have Q-values stored then add and create Q-values 
        if(qValueSt == null){
            List<Action> act = this.applicableActions(st);
            qValueSt = new ArrayList<QValue>(act.size());
            //Now we will create the Q-value for all the actions
            for(Action a : act){
                //Now we will add the q value 
                qValueSt.add(new QValue(st, a, this._initQ_.qValue(st, a)));
            }
            //we will store this for later use
            this._q_Values_.put(hashSt, qValueSt);
        }

        return qValueSt;
    }

    @Override
    public double qValue(State st, Action act) 
    {
        return Qstored(st, act).q;
    
    }


    protected QValue Qstored(State st, Action act)
    {
    
       //we will get all Q-values first
        List<QValue> qValueSt = this.qValues(st);

        //then we iterate through all the stored Q-values
        for(QValue qVal : qValueSt){
            if(qVal.a.equals(act)){ 
                return qVal;
            }
        }

        throw new RuntimeException("Matching Q-value not found");
   
    }

    @Override
    public double value(State st) {
        return QProvider.Helper.maxQ(this, st);
    }
        				

		
		
		
		
		
@Override
public Episode runLearningEpisode(Environment environment) 
{

        return this.runLearningEpisode(environment, -1);

}

@Override
public Episode runLearningEpisode(Environment environment, int
  maximumsteping) 
{
  
        //We will initialize the episode object with the environment initial state
        Episode episode = new
          Episode(environment.currentObservation());

        //behave until a terminal state or max steping is reached
        State state_Current = environment.currentObservation();
        int steping = 0;
        while(!environment.isInTerminalState() && (steping <
          maximumsteping || maximumsteping == -1)){

                //now we will select the action
                Action act = this._learn_Policy_.action(state_Current);

                //take the action and observe outcome
                EnvironmentOutcome envn_Out_Come =
                  environment.executeAction(act);

                //Now we will record the results
                episode.transition(envn_Out_Come);

                //get the max Q value of the resulting state if it's not terminal, 0 otherwise
                double maximumQ = envn_Out_Come.terminated ? 0. :
                  this.value(envn_Out_Come.op);

                //Now we will update the old Q value
                QValue oldQValue = this.Qstored(state_Current, act);

                oldQValue.q = oldQValue.q + this._learn_Rate_ *
                 (envn_Out_Come.r + this.gamma * maximumQ - oldQValue.q);


                //Now point to the next enviornment and update the state
                state_Current = envn_Out_Come.op;
                steping++;

        }

        return episode;

		
}		




		@Override
		public void resetSolver()
		{
				this._q_Values_.clear();
		}		
		
		
		
		public static void main(String[] args) {

        GridWorldDomain gridDomain = new GridWorldDomain(11, 11);
        gridDomain.setMapToFourRooms();
        gridDomain.setProbSucceedTransitionDynamics(0.8);
        gridDomain.setTf(new GridWorldTerminalFunction(10, 10));

        SADomain _domain_sa = gridDomain.generateDomain();

        //now we get the agent as 0,0 state
        State st = new GridWorldState(new GridAgent(0, 0));

        //now we will create an environment for our agent
        SimulatedEnvironment environment = new
          SimulatedEnvironment(_domain_sa, st);

        //now we will create Q-learning element
        QLearningTutorial _QL_agent_ = new
          QLearningTutorial(_domain_sa, 0.99, new
          SimpleHashableStateFactory(), 
          new ConstantValueFunction(), 0.1, 0.1);

        //Now we will run the Q learning algorithm and results will be store in a list
        List<Episode> _episodes_ = new ArrayList<Episode>(1000);
       
        for(int i = 0; i < 1000; i++)
        {
          _episodes_.add(_QL_agent_.runLearningEpisode(environment));
                environment.resetEnvironment();
        }

        Visualizer visualizer =
          GridWorldVisualizer.getVisualizer(gridDomain.getMap());
          new EpisodeSequenceVisualizer(visualizer, _domain_sa,
           _episodes_);

}







		

}
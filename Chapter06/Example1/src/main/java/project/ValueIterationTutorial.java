
package project;


//We will import all the required libraries
import java.util.*;

//Now we will import all the BURLAP libraries, 
//there are lot of them to implement and it ease all our development
//We already introduce the implementation of BURLAP in earlier chapters
import burlap.behavior.policy.GreedyQPolicy;

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

//This library is related to implement States in MDP
import burlap.behavior.singleagent.auxiliary.StateReachability;

//This library is related to implement Single agent planner
import burlap.behavior.singleagent.planning.Planner;

//This library is related to implement Value functions constants
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


public class ValueIterationTutorial extends MDPSolver implements QProvider, Planner{

 @Override   
  public double value(State st) 
   { 
    
      return 0.0; 
   
   }
 

  
  

	
	
	
	protected Map<HashableState, Double> functionValue;
	protected ValueFunction vfinit;
	protected int _iterations_Num;

	  
	public ValueIterationTutorial(SADomain domain_SA, double
	  gamma_discount_factor, HashableStateFactory _hashFactory_,
	  ValueFunction vfinit, int _iterations_Num)
	  {
		this.solverInit(domain_SA, gamma_discount_factor, _hashFactory_); 
		this.vfinit = vfinit; this._iterations_Num = _iterations_Num; 
		this.functionValue = new HashMap<HashableState, Double>();
	  }
	
	
	
	public void ReachableFrom(State stateSeed) 
    {
     Set<HashableState> Hashedstates = StateReachability.getReachableHashedStates(stateSeed, this.domain, this.hashingFactory); 

     //initialize the value function for all states 

     for(HashableState stateHash : Hashedstates)
     {
         if(!this.functionValue.containsKey(stateHash))
         { 
           this.functionValue.put(stateHash, this.vfinit.value(stateHash.s()));
         }
     }
}





@Override
    public List<QValue> qValues(State st) {
        List<Action> actionsApplicable = this.applicableActions(st);
        List<QValue> qvalueSt = new ArrayList<QValue>
       (actionsApplicable.size());
        for(Action act : actionsApplicable){
            qvalueSt.add(new QValue(st, act, 
              this.qValue(st, act)));
        }
        return qvalueSt;
    }

    @Override
    public double qValue(State st, Action act) {

      if(this.model.terminal(st)){
      return 0.;
      }

      //We will check the all the possible outcomes
      List<TransitionProb> tansProb = 
        ((FullModel)this.model).transitions(st, act);

      //aggregating all possible outcomes
      double q_Value = 0.; 
      for(TransitionProb transp : tansProb){
      
      //we will check the reward for this transition
      double _rr = transp.eo.r;

      //We will find the value for the next state
      double valuep = this.functionValue.get
        (this.hashingFactory.hashState(transp.eo.op));

      //Now we will add the contribution weighted by the transition probability and
      //it discounting the next state
      q_Value += transp.p * (_rr + this.gamma * valuep);
      
    }

      return q_Value;
    }

	
	
	
	@Override
  public GreedyQPolicy planFromState(State _initial_State_) {
        
        HashableState InitialStatehashed = 
          this.hashingFactory.hashState(_initial_State_);
    
        if(this.functionValue.containsKey(InitialStatehashed))
        {
           //planning perform here!
                return new GreedyQPolicy(this); 
        
        }

        //We find all the possible reachable states 
        this.ReachableFrom(_initial_State_);

        //Over the complete state space we perform multiple iterations
        for(int i = 0; i < this._iterations_Num; i++){
                
                //iterate over each state
                for(HashableState shKey : this.functionValue.keySet())
                {
                  //Now update the value from the bellman  equation
                  this.functionValue.put(shKey,
                    QProvider.Helper.maxQ(this, shKey.s()));
                }
        }

        return new GreedyQPolicy(this);

}



@Override
public void resetSolver() {
	this.functionValue.clear();
}
	

 public static void main(String [] args){
                
        GridWorldDomain gridDomain = new GridWorldDomain(11, 11);
        gridDomain.setTf(new GridWorldTerminalFunction(10, 10));
        gridDomain.setMapToFourRooms();

        //we implement it as 0.8 means 80% will go to intended direction
        gridDomain.setProbSucceedTransitionDynamics(0.8);

        SADomain domain_sa = gridDomain.generateDomain();

        //Initialize the agent to initial state 0, 0
        State st = new GridWorldState(new GridAgent(0, 0));

        //setup value iteration with discount factor as 0.99, 
        //a value function initialization that initializes all states to value 0, and which will
        //run for 30 iterations over the state space
        ValueIterationTutorial valueIteration = new
          ValueIterationTutorial(domain_sa, 0.99, new SimpleHashableStateFactory(), new ConstantValueFunction(0.0), 30);

        //we will now run the planning from our initial state
        Policy pol = valueIteration.planFromState(st);

        //we will evaluate the policy 
        Episode episode = PolicyUtils.rollout(pol, st,
        domain_sa.getModel());

        Visualizer visualize =
          GridWorldVisualizer.getVisualizer(gridDomain.getMap());
          new EpisodeSequenceVisualizer(visualize, domain_sa,
            Arrays.asList(episode));
                
}


	
	
  
}
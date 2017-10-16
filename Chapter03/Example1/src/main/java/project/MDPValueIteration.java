package project;

import burlap.behavior.policy.GreedyQPolicy;
import burlap.behavior.policy.Policy;
import burlap.behavior.policy.PolicyUtils;
import burlap.behavior.singleagent.Episode;
import burlap.behavior.singleagent.MDPSolver;
import burlap.behavior.singleagent.auxiliary.EpisodeSequenceVisualizer;
import burlap.behavior.singleagent.auxiliary.StateReachability;
import burlap.domain.singleagent.gridworld.GridWorldDomain;
import burlap.domain.singleagent.gridworld.GridWorldTerminalFunction;
import burlap.domain.singleagent.gridworld.GridWorldVisualizer;
import burlap.domain.singleagent.gridworld.state.GridAgent;
import burlap.domain.singleagent.gridworld.state.GridWorldState;
import burlap.mdp.core.action.Action;
import burlap.mdp.core.state.State;
import burlap.mdp.singleagent.SADomain;
import burlap.mdp.singleagent.model.FullModel;
import burlap.mdp.singleagent.model.TransitionProb;
import burlap.behavior.singleagent.planning.Planner;
import burlap.behavior.valuefunction.ConstantValueFunction;
import burlap.behavior.valuefunction.QProvider;
import burlap.behavior.valuefunction.QValue;
import burlap.behavior.valuefunction.ValueFunction;
import burlap.statehashing.HashableState; 
import burlap.statehashing.HashableStateFactory; 
import burlap.statehashing.simple.SimpleHashableStateFactory; 
import burlap.visualizer.Visualizer; 
import java.util.*; 

public class MDPValueIteration extends MDPSolver implements QProvider, Planner 
{
	
	protected Map<HashableState, Double> mdpValueFunction;
	protected ValueFunction vinit;
	protected int numIterations;

	public MDPValueIteration(SADomain saDomain, double alpha,
	  HashableStateFactory hsf, ValueFunction initializeVF, int numIterations)
	{
	 this.solverInit(saDomain, alpha, hsf);
	 this.vinit = initializeVF;
	 this.numIterations = numIterations;
	 this.mdpValueFunction = new HashMap <HashableState, Double> ();
	}
	
	
	
	
 @Override 
public double value(State st) 
{
 return 0.0;
}

 
public void performReachabilityFrom(State sState)
{
  Set<HashableState> hashStates = StateReachability.getReachableHashedStates(sState, this.domain, this.hashingFactory);
 
//initialize the value function for all states
 for(HashableState hash: hashStates)
 {
  if(!this.mdpValueFunction.containsKey(hash))
  {
    this.mdpValueFunction.put(hash, this.vinit.value(hash.s()));
  }
 }
}


@Override
public List<QValue> qValues(State st) {
 List<Action> app_Actions = this.applicableActions(st);
 List<QValue> qValue_state = new ArrayList<QValue>(app_Actions.size());
 for(Action act : app_Actions){
   qValue_state.add(new QValue(st, act, this.qValue(st, act)));
 }
 return qValue_state;
}

@Override
public double qValue(State st, Action act) {
if(this.model.terminal(st)){
 return 0.;
 }

//We need to check the possible outcomes
 List<TransitionProb> tran_prob = ((FullModel)this.model).transitions(st, act);

//We need to aggregate all the possible outcome
 double aggregate_q = 0.;
 for(TransitionProb tran_probability : tran_prob){
 
//Now we need to check the reward for the transition
 double reward = tran_probability.eo.r;

//We also need to determine the value of the next state
 double valueP=this.mdpValueFunction.get
   (this.hashingFactory.hashState(tran_probability.eo.op));
//now add the contribution weighted using discounting and 
 //transition probability for the next state
 aggregate_q += tran_probability.p * (reward + this.gamma * valueP);
 }
return aggregate_q;
}



@Override
public GreedyQPolicy planFromState(State initState) {
 
 HashableState hashedInitState = this.hashingFactory.hashState(initState);
 if(this.mdpValueFunction.containsKey(hashedInitState)){

//doing planning here
 return new GreedyQPolicy(this); 
 }

//In case this state is new then we need to find all the reachable state from this state
 this.performReachabilityFrom(initState);

//We need to do the iterations over the complete state space
 for(int i = 0; i < this.numIterations; i++){
 
//Each state to iterate
 for(HashableState sh : this.mdpValueFunction.keySet()){

 //value update as per bellman equation
 this.mdpValueFunction.put(sh, QProvider.Helper.maxQ(this, sh.s()));
 }
 }
return new GreedyQPolicy(this);
}



@Override
public void resetSolver() {
  this.mdpValueFunction.clear();
}




public static void main(String [] args){
 
 GridWorldDomain grid_world_domain = new GridWorldDomain(11, 11);
 grid_world_domain.setTf(new GridWorldTerminalFunction(10, 10));
 grid_world_domain.setMapToFourRooms();

//set the value to 80% to go to intended direction
 grid_world_domain.setProbSucceedTransitionDynamics(0.8);
 SADomain sa_Domain = grid_world_domain.generateDomain();

//get initial state with agent in 0,0
 State st = new GridWorldState(new GridAgent(0, 0));

//set a discount factor to 0.99 discount factor, a value function that initializes
 //the states to 0, and will run for about 30 iterations
 //over the state space
 MDPValueIteration value_Iteration = new MDPValueIteration(sa_Domain, 0.99, new 
   SimpleHashableStateFactory(), new ConstantValueFunction(0.0), 30);

//run planning from our initial state
 Policy policy = value_Iteration.planFromState(st);

//evaluate the policy with one roll out visualize the trajectory
Episode episode = PolicyUtils.rollout(policy, st, sa_Domain.getModel());
Visualizer v = GridWorldVisualizer.getVisualizer(grid_world_domain.getMap());
  new EpisodeSequenceVisualizer(v, sa_Domain, Arrays.asList(episode));
 
}





}
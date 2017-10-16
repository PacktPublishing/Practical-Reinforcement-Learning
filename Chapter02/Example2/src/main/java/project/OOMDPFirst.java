package project;

//We will import all the required libraries

//This library is for implementing run time exceptions
import javax.management.RuntimeErrorException;

//Now we will import all the BURLAP libraries, there are lot of them to implement and it ease all our development


import burlap.mdp.auxiliary.DomainGenerator;
import burlap.mdp.auxiliary.common.SinglePFTF;
import burlap.mdp.core.StateTransitionProb;
import burlap.mdp.core.TerminalFunction;
import burlap.mdp.core.action.Action;
import burlap.mdp.core.action.UniversalActionType;
import burlap.mdp.core.oo.OODomain;
import burlap.mdp.core.oo.propositional.PropositionalFunction;
import burlap.mdp.core.oo.state.OOState;
import burlap.mdp.core.oo.state.ObjectInstance;
import burlap.mdp.core.oo.state.generic.GenericOOState;
import burlap.mdp.core.state.State;
import burlap.mdp.singleagent.common.SingleGoalPFRF;
import burlap.mdp.singleagent.environment.SimulatedEnvironment;
import burlap.mdp.singleagent.model.FactoredModel;
import burlap.mdp.singleagent.model.RewardFunction;
import burlap.mdp.singleagent.model.statemodel.FullStateModel;
import burlap.mdp.singleagent.oo.OOSADomain;
import burlap.shell.visual.VisualExplorer;
import burlap.visualizer.*;


//This library is related to implement Domain
import burlap.domain.singleagent.graphdefined.GraphDefinedDomain;

import burlap.mdp.singleagent.oo.OOSADomain;


//This library is related to implement Value Iterations
import burlap.behavior.singleagent.planning.stochastic.valueiteration.ValueIteration;


public class OOMDPFirst 
{

    DomainGenerator domain_generator;
    OOSADomain var_domain_;
	int var_StatesNum_;
    
    public OOMDPFirst()
    {
        this.var_StatesNum_ = 6; 
        //this.domain_generator = new OOSADomain(var_StatesNum_);
       // this.var_domain_ = this.domain_generator.generateDomain();
    }
	
	
	State var_initial_state;
       
    //this.var_initial_state = OOSADomain.getState(this.var_domain_, 0);
	
	
	public OOMDPFirst(double var_parameter1_, double var_parameter2_, double var_parameter3_, double var_parameter4_)
    {
        this.var_StatesNum_ = 6;
        this.domain_generator = new GraphDefinedDomain(var_StatesNum_); 
        
        // actions from initial state 0
        ((GraphDefinedDomain) this.domain_generator).setTransition(0,
          0, 1, 1.);
        ((GraphDefinedDomain) this.domain_generator).setTransition(0,
          1, 2, 1.);
        ((GraphDefinedDomain) this.domain_generator).setTransition(0,
          2, 3, 1.);
    
        // actions from initial state 1
        ((GraphDefinedDomain) this.domain_generator).setTransition(1,
          0, 1, 1.);
    
        // actions from initial state 2
        ((GraphDefinedDomain) this.domain_generator).setTransition(2,
          0, 4, 1.);
    
        // actions from initial state 4
        ((GraphDefinedDomain) this.domain_generator).setTransition(4,
          0, 2, 1.);
    
        // actions from initial state 3
        ((GraphDefinedDomain) this.domain_generator).setTransition(3,
          0, 5, 1.);
    
        // actions from initial state 5
        ((GraphDefinedDomain) this.domain_generator).setTransition(5,
          0, 5, 1.);
    
        RewardFunction _varReward_func;
        _varReward_func = new RewardFourParam(var_parameter1_, var_parameter2_, var_parameter3_, var_parameter4_);
  
     
        
     } 
  
  
	 public static class RewardFourParam implements RewardFunction
    {
        
        double var_parameter1_;
        double var_parameter2_;
        double var_parameter3_;
        double var_parameter4_;
        
    public RewardFourParam(double var_parameter1_, double 
      var_parameter2_, double var_parameter3_, double var_parameter4_)
    {
            this.var_parameter1_ = var_parameter1_;
            this.var_parameter2_ = var_parameter2_;
            this.var_parameter3_ = var_parameter3_;
            this.var_parameter4_ = var_parameter4_;
    }
        
        @Override
     public double reward(State st, Action a, State sprime)
        {
            int _var__var_SID=6;
            double r;
            
            if(_var__var_SID == 0 || _var__var_SID ==3)
            {
                r=0; 
            }
            else if(_var__var_SID == 1)
            {
                r=this.var_parameter1_; 
            }
            else if(_var__var_SID == 2)
            {
                r=this.var_parameter2_; 
            }
            else if(_var__var_SID == 4)
            {
                r=this.var_parameter3_; 
            }
            else if(_var__var_SID == 5)
            {
                r=this.var_parameter4_; 
            }
            else
            {
        throw new RuntimeErrorException(null, "Unknown State "+_var__var_SID);
            }
            return r;
        }
    }
	

	public static void main(String args[])
	{
		
		System.out.println("Main executed...");
	}
	
	
	
 }
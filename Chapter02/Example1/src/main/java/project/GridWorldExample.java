package project;

//We will import all the required java libraries
import java.util.List;
import java.awt.*;
import java.awt.geom.Ellipse2D;
import java.util.ArrayList;
import java.awt.geom.Rectangle2D;

//Now we will import all the BURLAP libraries, there are lot of them to implement and it ease all our development


//This library is related to implement SA Domain
import burlap.mdp.singleagent.SADomain;

//This library is related to implement single agent simulated environment
import burlap.mdp.singleagent.environment.SimulatedEnvironment;

//This library is related to implement single agent model
import burlap.mdp.singleagent.model.FactoredModel;

//This library is related to implement state painter
import burlap.visualizer.StatePainter;

//This library is related to implement domain generator
import burlap.mdp.auxiliary.DomainGenerator;

//This library is related to implement transition probabilities
import burlap.mdp.core.StateTransitionProb;

//This library is related to implement state render layer
import burlap.visualizer.StateRenderLayer;

//This library is related to implement visualization
import burlap.visualizer.Visualizer;

//This library is related to implement terminal function
import burlap.mdp.core.TerminalFunction;

//This library is related to implement actions
import burlap.mdp.core.action.Action;

//This library is related to implement universal action type
import burlap.mdp.core.action.UniversalActionType;

//This library is related to implement states
import burlap.mdp.core.state.State;

//This library is related to implement reward function
import burlap.mdp.singleagent.model.RewardFunction;

//This library is related to implement full state model on single agent
import burlap.mdp.singleagent.model.statemodel.FullStateModel;

//This library is related to implement visual explorer
import burlap.shell.visual.VisualExplorer;

//This library is related to implement state painter
import burlap.visualizer.StatePainter;


public class GridWorldExample implements DomainGenerator {


	public static final String VARIABLE_A = "a";
	public static final String VARIABLE_B = "b";

	public static final String AGENT_ACTIONS_EAST = "east";
	public static final String AGENT_ACTIONS_NORTH = "north";
	public static final String AGENT_ACTIONS_SOUTH = "south";
	public static final String AGENT_ACTIONS_WEST = "west";




 
 protected int [][] map_GridWorld = new int[][]{
        {0,0,0,0,0,1,0,0,0,0,0},
        {0,0,0,0,0,0,0,0,0,0,0},
        {0,0,0,0,0,1,0,0,0,0,0},
        {0,0,0,0,0,1,0,0,0,0,0},
        {0,0,0,0,0,1,0,0,0,0,0},
        {1,0,1,1,1,1,1,1,0,1,1},
        {0,0,0,0,1,0,0,0,0,0,0},
        {0,0,0,0,1,0,0,0,0,0,0},
        {0,0,0,0,0,0,0,0,0,0,0},
        {0,0,0,0,1,0,0,0,0,0,0},
        {0,0,0,0,1,0,0,0,0,0,0},
};



protected class GridWorldExampleStateModel implements FullStateModel{

   

    
	protected double [][] transitionExampleProbs;

public GridWorldExampleStateModel() {
    this.transitionExampleProbs = new double[4][4];
    for(int i = 0; i < 4; i++){
        for(int j = 0; j < 4; j++){
            double p = i != j ? 0.2/3 : 0.8;
            transitionExampleProbs[i][j] = p;
        }
    }
}


@Override
public State sample(State s, Action act) {

    s = s.copy();
    GridStateEX gsExample = (GridStateEX)s;
    int curA = gsExample.a;
    int curB = gsExample.b;

    int adirExample = actionDir(act);

    //sample direction with random roll
    double random = Math.random();
    double _sumProb = 0.;
    int _dir = 0;
    for(int i = 0; i < 4; i++){
        _sumProb += this.transitionExampleProbs[adirExample][i];
        if(random < _sumProb){
            _dir = i;
            break; //found direction
        }
    }

    //get resulting position
    int [] _newPos = this.moveExampleResult(curA, curB, _dir);

    //set the new position
    gsExample.a = _newPos[0];
    gsExample.b = _newPos[1];

    //return the modified state
    return gsExample;
}


protected int actionDir(Action a){
    int adir = -1;
    if(a.actionName().equals(AGENT_ACTIONS_NORTH)){
        adir = 0;
    }
    else if(a.actionName().equals(AGENT_ACTIONS_SOUTH)){
        adir = 1;
    }
    else if(a.actionName().equals(AGENT_ACTIONS_EAST)){
        adir = 2;
    }
    else if(a.actionName().equals(AGENT_ACTIONS_WEST)){
        adir = 3;
    }
    return adir;
}



protected int [] moveExampleResult(int curA, int curB, int exampleDirection){

    //first thing we will change in a and b from direction 
    //using 3: west; 2:east; 1: south; 0: north;
    int adelta = 0;
    int bdelta = 0;
    if(exampleDirection == 0){
        adelta = 1;
    }
    else if(exampleDirection == 1){
        bdelta = -1;
    }
    else if(exampleDirection == 2){
        adelta = 1;
    }
    else{
        adelta = -1;
    }

    int na = curA + adelta;
    int nb = curB + bdelta;

    int _width = GridWorldExample.this.map_GridWorld.length;
    int _height = GridWorldExample.this.map_GridWorld[0].length;

    //Now we need to verify that it is a valid new position
    if(na < 0 || na >= _width || nb < 0 || nb >= _height ||
            GridWorldExample.this.map_GridWorld[na][nb] == 1){
        na = curA;
        nb = curB;
    }


    return new int[]{na,nb};

}

@Override
public List<StateTransitionProb> stateTransitions(State st, Action act) {

    //get agent current position
    GridStateEX gsExample = (GridStateEX) st;

    int curA = gsExample.a;
    int curB = gsExample.b;

    int _adir = actionDir(act);

    List<StateTransitionProb> tpsExample = new ArrayList<StateTransitionProb>(4);
    StateTransitionProb _noChange = null;
    for(int i = 0; i < 4; i++){

        int [] newPosExample = this.moveExampleResult(curA, curB, i);
        if(newPosExample[0] != curA || newPosExample[1] != curB){
            
			//We will write the possible new outcome
            
			GridStateEX _ns = gsExample.copy();
            _ns.a = newPosExample[0];
            _ns.b = newPosExample[1];

            //Now create the object of transition probability and add this to our possible outcomes
            tpsExample.add(new StateTransitionProb(_ns, 
              this.transitionExampleProbs[_adir][i]));
        }
        else{
            
			//Check if it is a block state, it means the possible direction is not changed.
            if(_noChange != null){
                _noChange.p += this.transitionExampleProbs[_adir][i];
            }
            else{
                //In case no block state then move the transition
                _noChange = new StateTransitionProb(st.copy(),
                  this.transitionExampleProbs[_adir][i]);
                tpsExample.add(_noChange);
            }
        }

    }


    return tpsExample;
}


}
 
 











///////////////////////////////






/////////////////////////////////

public static class TFExample implements TerminalFunction {

    int goalA;
    int goalB;

    public TFExample(int goalA, int goalB){
        this.goalA = goalA;
        this.goalB = goalB;
    }

    @Override
    public boolean isTerminal(State st) {

        //get location of agent in next state
        int _ax = (Integer)st.get(VARIABLE_A);
        int _ay = (Integer)st.get(VARIABLE_B);

        //check if this is the goal state
        if(_ax == this.goalA && _ay == this.goalB){
            return true;
        }

        return false;
    }

}





//////////////////////////////////

public static class RFExample implements RewardFunction {

    int goalA;
    int goalB;

    public RFExample(int goalA, int goalB){
        this.goalA = goalA;
        this.goalB = goalB;
    }

    @Override
    public double reward(State st, Action act, State sprimeExample) {

        int _ax = (Integer)st.get(VARIABLE_A);
        int _ay = (Integer)st.get(VARIABLE_B);

        //check if it is a goal state
        if(_ax == this.goalA && _ay == this.goalB){
            return 100.;
        }

        return -1;
    }


}



////////////////

protected int _goala = 10;
protected int _goalb = 10;

/////////

public void setGoalLocation(int _goala, int _goalb){
    this._goala = _goala;
    this._goalb = _goalb;
}

///////////////

@Override
public SADomain generateDomain() {

    SADomain domainExample = new SADomain();


    domainExample.addActionTypes(
            new UniversalActionType(AGENT_ACTIONS_NORTH),
            new UniversalActionType(AGENT_ACTIONS_SOUTH),
            new UniversalActionType(AGENT_ACTIONS_EAST),
            new UniversalActionType(AGENT_ACTIONS_WEST));

    GridWorldExampleStateModel _smodelExample = new GridWorldExampleStateModel();
    RewardFunction _rf = new RFExample(this._goala, this._goalb);
    TerminalFunction _tf = new TFExample(this._goala, this._goalb);

    domainExample.setModel(new FactoredModel(_smodelExample, _rf, _tf));

    return domainExample;
}



/////////////////////











//////////////////

public class WallPainterExample implements StatePainter {

    public void paint(Graphics2D _g2, State st, float _cWidth, float
      _cHeight) {

        //we display the wall in black 
        _g2.setColor(Color.BLACK);

        //seting floats for the height and weight of our domain
        float _fWidth = GridWorldExample.this.map_GridWorld.length;
        float _fHeight = GridWorldExample.this.map_GridWorld[0].length;

        //check the single cell width
        //the complete map will be painted on the whole canvas.

        float _width = _cWidth / _fWidth;
        float _height = _cHeight / _fHeight;

        
        for(int i = 0; i < GridWorldExample.this.map_GridWorld.length; 
          i++){
            for(int j = 0; j < 
              GridWorldExample.this.map_GridWorld[0].length; j++){

                //Check if it is a wall
                if(GridWorldExample.this.map_GridWorld[i][j] == 1){

                    //left coordinate of cell on our canvas
                    float _rx = i*_width;

                    float _ry = _cHeight - _height - j*_height;

                    //Now paint into the ractangle
                    _g2.fill(new Rectangle2D.Float(_rx, _ry, _width, 
                      _height));

                }
            }
        }
    }
}

public class AgentPainterExample implements StatePainter {

    @Override
    public void paint(Graphics2D _g2, State st,
                            float _cWidth, float _cHeight) {

        //agent will be filled in gray
        _g2.setColor(Color.GRAY);

        //set up floats for the width and height of our domain
        float _fWidth = GridWorldExample.this.map_GridWorld.length;
        float _fHeight = GridWorldExample.this.map_GridWorld[0].length;

        //determine the width of a single cell on our canvas
        //such that the whole map can be painted
        float _width = _cWidth / _fWidth;
        float _height = _cHeight / _fHeight;

        int _ax = (Integer)st.get(VARIABLE_A);
        int _ay = (Integer)st.get(VARIABLE_B);

        //left coordinate of cell on our canvas
        float _rx = _ax*_width;

        //top coordinate of cell on our canvas
        //coordinate system adjustment because the java canvas
        //origin is in the top left instead of the bottom right
        float _ry = _cHeight - _height - _ay*_height;

        //paint the rectangle
        _g2.fill(new Ellipse2D.Float(_rx, _ry, _width, _height));

    }
	
}

public StateRenderLayer getStateRenderLayer(){
	StateRenderLayer rl = new StateRenderLayer();
	rl.addStatePainter(new GridWorldExample.WallPainterExample());
	rl.addStatePainter(new GridWorldExample.AgentPainterExample());

	return rl;
}

public Visualizer getVisualizer(){
	return new Visualizer(this.getStateRenderLayer());
}


public static void main(String [] args){

    GridWorldExample _gen = new GridWorldExample();
    _gen.setGoalLocation(10, 10);
    SADomain _domain = _gen.generateDomain();
    State _initialState = new GridStateEX(0, 0);
    SimulatedEnvironment _env = new SimulatedEnvironment(_domain,
      _initialState);

    Visualizer _v = _gen.getVisualizer();
    VisualExplorer _exp = new VisualExplorer(_domain, _env, _v);

    _exp.addKeyAction("w", AGENT_ACTIONS_NORTH, "");
    _exp.addKeyAction("s", AGENT_ACTIONS_SOUTH, "");
    _exp.addKeyAction("d", AGENT_ACTIONS_EAST, "");
    _exp.addKeyAction("a", AGENT_ACTIONS_WEST, "");

    _exp.initGUI();

}
}
        
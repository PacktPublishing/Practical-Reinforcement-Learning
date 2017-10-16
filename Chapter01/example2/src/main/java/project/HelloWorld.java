package project; 
import burlap.shell.visual.VisualExplorer; 
import burlap.mdp.singleagent.SADomain; 
import burlap.domain.singleagent.gridworld.GridWorldDomain; 
import burlap.domain.singleagent.gridworld.GridWorldVisualizer; 
import burlap.domain.singleagent.gridworld.state.GridWorldState; 
import burlap.domain.singleagent.gridworld.state.GridLocation; 
import burlap.domain.singleagent.gridworld.state.GridAgent; 
import burlap.mdp.core.state.State; 
import burlap.visualizer.Visualizer; 

public class HelloWorld 
{ 
 public static void main(String[] args) 
 {
 //11x11 grid world 
 GridWorldDomain gridworld = new GridWorldDomain(11,11); 
 
 //layout four rooms
 gridworld.setMapToFourRooms(); 

 //transitions with 0.9 success rate 
 gridworld.setProbSucceedTransitionDynamics(0.9); 

 //now we will create the grid world domain 
 SADomain sad= gridworld.generateDomain(); 

 //initial state setup 
 State st = new GridWorldState(new GridAgent(0, 0), new GridLocation(10, 10, "loc0")); 
 
 //now we will setup visualizer and visual explorer 
 Visualizer vis = GridWorldVisualizer.getVisualizer(gridworld.getMap()); 
 VisualExplorer ve= new VisualExplorer(sad, vis, st); 

 //now setup the control keys move the agent to "a w d s"
 ve.addKeyAction("a", GridWorldDomain.ACTION_WEST, ""); 
 ve.addKeyAction("w", GridWorldDomain.ACTION_NORTH, ""); 
 ve.addKeyAction("d", GridWorldDomain.ACTION_EAST, ""); 
 ve.addKeyAction("s", GridWorldDomain.ACTION_SOUTH, ""); 
 
 ve.initGUI(); } }
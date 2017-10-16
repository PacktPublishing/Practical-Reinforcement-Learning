package project;

//We will import all the required java libraries
import java.util.Arrays;
import java.util.List;

//Now we will import all the BURLAP libraries, there are lot of them to implement and it ease all our development

//This library is related to implement Deep copy state
import burlap.mdp.core.state.annotations.DeepCopyState;

//This library is related to implement mutable states
import burlap.mdp.core.state.MutableState;

//This library is related to implement state utilities
import burlap.mdp.core.state.StateUtilities;

//This library is related to implement exception handling
import burlap.mdp.core.state.UnknownKeyException;

import static project.GridWorldExample.VARIABLE_A;
import static project.GridWorldExample.VARIABLE_B;

public class GridStateEX implements MutableState{


    
    
	
	 public int a;
	 public int b;

  public GridStateEX() {
  }

  public GridStateEX(int a, int b) {
    this.a = a;
    this.b = b;
  }
  
  private final static List<Object> keys = Arrays.<Object>asList(VARIABLE_A, VARIABLE_B);

  
  @Override
public MutableState set(Object variableKey, Object value) {
    if(variableKey.equals(VARIABLE_A)){
        this.a = StateUtilities.stringOrNumber(value).intValue();
    }
    else if(variableKey.equals(VARIABLE_B)){
        this.b = StateUtilities.stringOrNumber(value).intValue();
    }
    else{
        throw new UnknownKeyException(variableKey);
    }
    return this;
}

@Override
public List<Object> variableKeys() {
    return keys;
}

@Override
public Object get(Object variableKey) {
    if(variableKey.equals(VARIABLE_A)){
        return a;
    }
    else if(variableKey.equals(VARIABLE_B)){
        return b;
    }
    throw new UnknownKeyException(variableKey);
}


@Override
public GridStateEX copy() {
    return new GridStateEX(a, b);
}

@Override
public String toString() {
    return StateUtilities.stateToString(this);
}


}
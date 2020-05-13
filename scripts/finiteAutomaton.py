class finiteAutomaton:
    """
    a state machine with a grand title. Handlers are functions
    
    Here I am trying to make a switching signal similar to those described in 
    Path-complete positivity of switching systems by Forni, Jungers, and Sepulchre in 2016.
    
    The Automaton is path complete if it is constructed so that its paths capture the complete
    allowed behaviour of the switching signal
    """
    
    def __init__(self,dontLoop=None):
        self.handlers = {}
        self.startState = None
        self.currentState = None
        self.endStates = []
        if dontLoop == None:
            self.dontLoop = False
        else:
            self.dontLoop = True
    
    def Q(self):
        #returns the list of states, Q, of the finite automaton
        return list(self.handlers.keys())
    
    def F(self):
        #returns the list of end states, F, of the the finite automaton
        return self.endStates 
    
    def delta(self):
        #returns a dict of state transitions, delta, of the finite automaton
        return self.handlers
    
    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)
    
    def set_start(self, name):
        self.startState = name.upper()
        self.currentState = name.upper()
    
    def run(self, cargo):

        if self.dontLoop:
            try:
                handler = self.handlers[self.currentState]
            except:
                raise InitializationError("must call .set_start() before .run()")      
            (newState, cargo) = handler(cargo)
            
            if newState.upper() in self.endStates:
                print("reached ", newState)
            else:
                self.currentState = newState.upper()
            return cargo

        else:

            try:
                handler = self.handlers[self.startState]
            except:
                raise InitializationError("must call .set_start() before .run()")      
            if not self.endStates:
                raise  InitializationError("at least one state must be an end_state if run with dontLoop = False")

            while True:
                (newState, cargo) = handler(cargo)
                if newState.upper() in self.endStates:
                    print("reached ", newState)
                    break 
                else:
                    handler = self.handlers[newState.upper()] 

import sys
import dndTools
import finiteAutomaton

hethState = finiteAutomaton.finiteAutomaton()

def locationHub(x):
    newState = 'locationHub'
    
    options_string = '0: heth wilderness\t1: exit\n'
    try:
        choice = int(input(options_string))
    except:
        choice = -1
        
    if (choice == 0):
        newState = 'hethWilderness'
    elif (choice ==1):
        newState = 'endState'
    else:
        print('input was not recognised')
    return(newState,0) 
    

def hethWilderness(x):
    newState = 'hethWilderness'
    
    options_string = 'heth wilderness\n0: weather\t1: random encounter\t2: camp encounter\t3: change location\n'
    try:
        choice = int(input(options_string))
    except:
        choice = -1
        
    if (choice == 0): #weather
        dndTools.hethWeather('oghma')
    elif (choice == 1): #random encounter
        print(dndTools.hethRandomEncounters())
    elif (choice == 2): #random camp encounter
        print(dndTools.campRandomEncounters())
    elif (choice == 3): #change location
        newState = 'locationHub'
    else:
        print('iniput was not recognised')
        
    return(newState,1) 

def endState(x):
    #state machine exits when passed an end state
    pass
    


hethState.add_state('locationHub',locationHub)   
hethState.add_state('hethWilderness',hethWilderness)
hethState.add_state('endState',endState,end_state=1)
hethState.set_start('locationHub')

def heth():
    hethState.run(0)

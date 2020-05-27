import sys
import dndTools
from dndTools import randomTable,randomTableFromCSV
import finiteAutomaton


def hethWeather(season):
    """
    12 months:
    Lathander - 42 days of spring
    Dusk Lunarpass - 7 days 
    Eldath - 42 days of spring
    Lliira - 42 days of summer
    Chauntea - 42 days of summer
    Oghma - 42 days of autumn
    Dawn Lunarpass - 7 days 
    Myrkul - 42 days of autumn 
    Savras - 42 days of winter
    Ilmater - 42 days of winter
    """

    springWeather = randomTable(['good weather 5-10C','good weather 10C-15C','good weather 15-20C','rain 5-15C'])
    summerWeather = randomTable(['good weather 15-20C','good weather 20-25C'])
    autumnWeather = randomTable(['good weather, 5-10C','overcast 5-10C','overcast 5-8C','overcast 3-6C','rain 3-5C','hail 3C','snow -3 - 0C'])
    winterWeather = randomTable(['good weather, 0-5C','overcast 0-3C','overcast -3-0C','overcast -6-0C','snow -3-0C','snow -10 -> -3C','hail 0-3C'])

    if(season == 'lathander'):
        pass
    elif(season == 'dusk'):
        pass
    elif(season == 'eldath'):
        pass
    elif(season == 'lliira'):
        pass
    elif(season == 'chauntea'):
        pass
    elif(season =='oghma'):
        print('the weather in Oghma\'s month is {0}'.format(autumnWeather()))
    elif(season == 'dawn'):
        print('the weather in the Dawn lunarpass is {0}'.format(autumnWeather()))
    elif(season == 'myrkul'):
        myrkulWeather = randomTable([autumnWeather,winterWeather])
        print('the weather in Myrkul\'s month is {0}'.format(myrkulWeather()))
    elif(season == 'savras'):
        print('the weather in Savras\' month is {0}'.format(winterWeather()))
    elif(season == 'ilmater'):
        ilmaterWeather = randomTable([winterWeather,'cold clear -10C, blizzard -10C, strong winds, -5c feels like -20C'])
        print('the weather in ilmater\'s month is {0}'.format(ilmaterWeather()))
    else:
        weather = randomTable([springWeather,summerWeather,autumnWeather,winterWeather])
        print('the weather is {0}'.format(weather()))


#heth encounters
passerbyEncounters = randomTableFromCSV('../config/passerbyEncounters.csv')
faunaEncounters = randomTableFromCSV('../config/faunaEncounters.csv')
floraEncounters = randomTableFromCSV('../config/floraEncounters.csv')
intrigueEncounters = randomTableFromCSV('../config/intrigueEncounters.csv')
humanoidThreatEncounters = randomTableFromCSV('../config/humanoidThreatEncounters.csv')
threatEncounters = randomTableFromCSV('../config/threatEncounters.csv')
campRandomEncounters = randomTableFromCSV('../config/campEncounters.csv')
hethWildernessEncounters = randomTable([passerbyEncounters,faunaEncounters,floraEncounters,intrigueEncounters,
                                    humanoidThreatEncounters,threatEncounters])
hethEncounters = randomTable([campRandomEncounters,hethWildernessEncounters])

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
    cargo = 1

    options_string = 'heth wilderness\n0: weather\t1: random encounter\t2: camp encounter\t3: change location\t4:travel wilderness\n'
    try:
        choice = int(input(options_string))
    except:
        choice = -1
        
    if (choice == 0): #weather
        hethWeather('oghma')
    elif (choice == 1): #random encounter
        print(hethWildernessEncounters())
    elif (choice == 2): #random camp encounter
        print(campRandomEncounters())
    elif (choice == 3): #change location
        newState = 'locationHub'
    elif (choice == 4): #enter the travelwilderness state
        newState = 'travelWilderness'
        cargo = [int(input('how many days?\n')),input('what month?\n'),0]
    else:
        print('iniput was not recognised')
        
    return(newState,cargo) 

def travelWilderness(cargo):
    """
    for travelWilderness cargo should be a list format, [days,season,daysTravelled,numFails]
    where days is the expected number of days for the journey
    month is the current month
    daysTravelled is the number of days travelled so far.
    """
    days,month,daysTravelled = cargo

    failFlag = 0
    
    print('day {0} of travel'.format(daysTravelled))
    hethWeather(month)
    
    if(input('get a survival check for the day DC based on weather and terrain if success press y') != 'y'):
        failFlag = 1
    if(input('run an encounter today? y or other') == 'y'):
        print(hethEncounters())
        input('press any key to continue')
    else:
        print('describe the view')
    print('make camp and -1 ration!\n\n\n\n\n')

    daysTravelled += 1

    if(daysTravelled < days):
        newState = 'travelWilderness'
    else:
        newState = 'locationHub'

    if(failFlag > 0):
        if (input('have they got lost? if y add half a day to travel\n'=='y')):
            days += 0.5

    cargo = [days,month,daysTravelled]

    return(newState,cargo)

def endState(x):
    #state machine exits when passed an end state
    pass
    


hethState.add_state('locationHub',locationHub)   
hethState.add_state('hethWilderness',hethWilderness)
hethState.add_state('travelWilderness',travelWilderness)
hethState.add_state('endState',endState,end_state=1)
hethState.set_start('locationHub')

def heth():
    """
    launches the heth state machine
    """
    hethState.run(0)

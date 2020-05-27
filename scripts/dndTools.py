import numpy as np
import math
import random
from numpy import random as rd
import csv

def roll(n=1, d=20, highest_n=None, lowest_n=None, modifier=None):
    """
    d is the number of sides, 
    n is the number of dice, 
    highest_n should be an int, if given the highest_n highest value rolls are returned
    lowest_n should be an int, if given the lowest_n lowest value rolls are returned
    modifier is a number to be added to the roll. This should include the proficiency bonus
    
    for example: 
    roll(n=3, d=4) will return the result of rolling 3D4 
    roll(n=2, d=20, highest_n = 1) is equivalent to rolling 1D20 with advantage
    roll(n=2, d=20, lowest_n = 1) is equivalent to rolling 1D20 with disadvantage
    
    """
    
    rolls = np.random.randint(1,d + 1,size = n)
    
    if (highest_n != None):
        while (rolls.shape[0] > highest_n):
            rolls = np.delete(rolls,rolls.argmin())
    elif (lowest_n != None):
        while (rolls.shape[0] > lowest_n):
            rolls = np.delete(rolls,rolls.argmax())
    
    result = sum(rolls)
    
    if (modifier != None):
        result += modifier
    
    return result

def simulateRoll(dc,modifier,n=1000):
    """
    prints the number of successes out of n rolls 
    """
    successes = 0
    for i in range (0,n):
        if(roll(modifier=modifier) >= dc):
            successes += 1
    return(successes/n)

def rollCharacterStats():
    stats = []
    for i in range(0,6):
        stat = roll(6,4,highest_n=3)
        stats.append(stat)
        
    return stats


class nameGen:
    def __init__(self, maleNameFragments,femaleNameFragments):
        self.maleNameFragments = maleNameFragments
        self.femaleNameFragments = femaleNameFragments
    
    def __call__(self,gender):
        """
        generates a name of the given gender from the provided name fragments  
        """
        if(gender == "male" or gender == "m" ):
            nameFragments = self.maleNameFragments
        else:
            nameFragments = self.femaleNameFragments

        name = ""
        for nameFragment in nameFragments:
                name += nameFragment[random.randint(0,len(nameFragment)-1)]

        return name

#Orc names    
mOrcNameFragments = [["Cro", "Thra","Vor","Da","Bor","gar"], #first syllable
                     ["b","m","d","v","k","g"], #middle consonant
                     ["ur","ak","ar","um","","oth"]] #ending syllable
fOrcNameFragments = [["No", "San","Tum","Ur"], #first syllable
                     ["","i","a"], #middle vowel
                    ["mi","ka","da","me"]] #last syllable
orcName = nameGen(mOrcNameFragments,fOrcNameFragments)

#Halfling names
mHalflingNameFragments = [["Dav", "Cos","Jo","Las","Knu"], #first syllable
                          ["ry","mo","seph","ire"]] #last syllable
fHalflingNameFragments = [["Chen", "Mae","Leu","Wil","Wal"], #first syllable
                          ["wyn","la","da"]] #last syllable
halflingName = nameGen(mHalflingNameFragments,fHalflingNameFragments)


class randomTable:
    def __init__(self, tableEntries):
        """
        tableEntries should be a list of strings and/or randomTable objects.  
        """               
        self.tableEntries = tableEntries
            
    def __call__(self):
        chosenEntry = self.tableEntries[rd.randint(0,len(self.tableEntries))]
        
        if (isinstance(chosenEntry,randomTable)):
            return(chosenEntry())
        else:
            return(chosenEntry)
        
def randomTableFromCSV(filename):
    """
    import a csv file as a randomTable, csv should be two columns 
    """
    tableEntries = []
    with open(filename, newline='',encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        subtableFlag = False
        for row in reader:
            if(row[0] == 'subtable' and not subtableFlag):
                subtableEntries = [row[1]]
                subtableFlag = True
            elif(row[0] == 'subtable' and subtableFlag):
                subtableEntries.append(row[1])
            elif(row[0] != 'subtable' and subtableFlag):
                tableEntries.append(randomTable(subtableEntries))
                tableEntries.append(row[1])
                subtableFlag = False
            else:
                tableEntries.append(row[1])
    return randomTable(tableEntries)

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



passerbyEncounters = randomTableFromCSV('../config/passerbyEncounters.csv')
faunaEncounters = randomTableFromCSV('../config/faunaEncounters.csv')
floraEncounters = randomTableFromCSV('../config/floraEncounters.csv')
intrigueEncounters = randomTableFromCSV('../config/intrigueEncounters.csv')
humanoidThreatEncounters = randomTableFromCSV('../config/humanoidThreatEncounters.csv')
threatEncounters = randomTableFromCSV('../config/threatEncounters.csv')

campRandomEncounters = randomTableFromCSV('../config/campEncounters.csv')

hethRandomEncounters = randomTable([passerbyEncounters,faunaEncounters,floraEncounters,intrigueEncounters,
                                    humanoidThreatEncounters,threatEncounters])
hethEncounters = randomTable([campRandomEncounters,hethRandomEncounters])

def travelWilderness(days=1,season='oghma',daysTravelled=0):
    numFails = 0
    for day in range(0,days):
        print('day {0} of travel'.format(daysTravelled))
        if (season=='oghma'):
            hethWeather('oghma')
        else:
            hethWeather('NA')

        if(input('get a survival check for the day DC based on weather and terrain if success press y') != 'y'):
            numFails += 1
        if(input('run an encounter today? y or other') == 'y'):
            print(hethEncounters())
            input('press any key to continue')
        else:
            print('describe the view')
        print('make camp and -1 ration!\n\n\n\n\n')

        daysTravelled += 1

    #print('get a con save for each member in the group DC = 8 + {0} (num days max 7) + {1} (numfailed survivalchecks) \non fail they gain 1 level of exhaustion'.format(min(days,7),numFails))

    if(numFails >2):
        if (input('have they got lost? if y continuing travelling for at least {0} days'.format(int(numFails/2)))=='y'):
            travelWilderness(days=int(numFails/2),season=season, daysTravelled=daysTravelled)


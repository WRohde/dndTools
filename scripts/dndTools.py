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

def randomTableToCSV(randomTable,filename): 
    """
    export the randomTable to csv
    """
    with open(filename,"w+", newline='',encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)

        for entry in randomTable.tableEntries:
            if type(entry) is type(randomTable):
                for subentry in entry.tableEntries:
                    writer.writerow(["subtable", subentry])
            else:
                writer.writerow(["", entry])
            
                


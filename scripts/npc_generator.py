import numpy as np
import random
import csv
import dndTools

class ancestry: #TODO add surnames
    def __init__(self, ancestry, ancestry_weight, m_names, f_names, x_names, descriptions, gender_ratio = [49,49,2]):
        """
        ancestry should be a string and is the name of the ancestry.
        ancestry_weight should be a positive integer between 1 and 100. The chance of an ancestry
        being selected from the ancestry_table will be ancestry_weight/sum(ancestry_weights). A race
        with a value of 1 will be rare, with a value of 100 it will be common.
        m_names, f_names, x_names and descriptions should all be lists of strings
        gender_ratio is the ratio of male:female:nonbinary in a list of floats [m,f,x]
        """
        self.ancestry = ancestry
        self.ancestry_weight = ancestry_weight
        self.m_names = m_names
        self.f_names = f_names
        self.x_names = x_names
        self.descriptions = descriptions
        self.gender_ratio = gender_ratio

class ancestry_table:
    def __init__(self, ancestries = None):
        """
        ancestries should be a dict of ancestry class objects with ancestry.ancestry as their
        respective keys.
        """
        self.ancestry_table = ancestries
        self.ancestries = list(ancestries.keys())
        self.ancestry_weights = []
        for ancestry in self.ancestries:
            self.ancestry_weights.append(self.ancestry_table[ancestry].ancestry_weight)

    def load_ancestry_table(self,filepath): #TODO load from json
        pass

    def save_ancestry_table(self,filepath): #TODO save to json
        pass

    def random_ancestry(self,n=1):
        chosen_ancestry = random.choices(self.ancestries, weights=self.ancestry_weights, k=n)
        return chosen_ancestry

    def random_gender(self,ancestries):
        genders = []
        for ancestry in ancestries:
            genders.append(random.choices(['male','female','non-binary'],weights=self.ancestry_table[ancestry].gender_ratio)[0])
        return genders

    def get_name(self,ancestries,genders):
        names = []
        for i,ancestry in enumerate(ancestries):
            current_ancestry = self.ancestry_table[ancestry]
            if genders[i] == 'male':
                names.append(random.choice(current_ancestry.m_names))
            elif genders[i] == 'female':
                names.append(random.choice(current_ancestry.f_names))
            else:
                names.append(random.choice(current_ancestry.x_names))
        return names


class quirk_table:
    def __init__(self,filepath=None,appearance=None,abilities=None,talents=None,mannerisms=None,interactions=None,ideals=None,bonds=None,flaws=None):
        """
        all of the quirks should be dndTools.randomTable objects, or should be left as None and
        imported from csv with load_csv_quirk_tables
        """
        if filepath:
            self.load_csv_quirk_tables(filepath)
        else:
            self.appearance = appearance
            self.abilities = abilities
            self.talents = talents
            self.mannerisms = mannerisms
            self.interactions = interactions
            self.ideals = ideals
            self.bonds = bonds
            self.flaws = flaws

    def load_csv_quirk_tables(self,filepath):
        """
        each quirk should be in the folder given as filepath in a csv sharing it's name.
        e.g. the appearance quirk table should be located at filepath/appearance.csv

        They are loaded as dndTools.randomTable objects
        """

        self.appearance = dndTools.randomTableFromCSV(filepath + "appearance.csv")
        self.abilities = dndTools.randomTableFromCSV(filepath + "abilities.csv")
        self.talents = dndTools.randomTableFromCSV(filepath + "talents.csv")
        self.mannerisms = dndTools.randomTableFromCSV(filepath + "mannerisms.csv")
        self.interactions = dndTools.randomTableFromCSV(filepath + "interactions.csv")
        self.ideals = dndTools.randomTableFromCSV(filepath + "ideals.csv")
        self.bonds = dndTools.randomTableFromCSV(filepath + "bonds.csv")
        self.flaws = dndTools.randomTableFromCSV(filepath + "flaws.csv")

    def save_csv_quirk_tables(self,filepath):
        """
        saves all the quirks as csv files in filepath
        """

        dndTools.randomTableToCSV(self.appearance, filepath + "appearance.csv")
        dndTools.randomTableToCSV(self.abilities, filepath + "abilities.csv")
        dndTools.randomTableFromCSV(self.talents, filepath + "talents.csv")
        dndTools.randomTableFromCSV(self.mannerisms, filepath + "mannerisms.csv")
        dndTools.randomTableFromCSV(self.interactions, filepath + "interactions.csv")
        dndTools.randomTableFromCSV(self.ideals, filepath + "ideals.csv")
        dndTools.randomTableFromCSV(self.bonds, filepath + "bonds.csv")
        dndTools.randomTableFromCSV(self.flaws, filepath + "flaws.csv")

    def generate_quirks(self,n):
        quirk_strings = []
        for i in range(n):
            quirk_string = ""
            if self.appearance:
                quirk_string += " They have {0}, ".format(self.appearance())
            if self.abilities:
                quirk_string += " {0}. ".format(self.abilities())
            if self.talents:
                quirk_string += "their talent is: {0}. ".format(self.talents())
            if self.interactions:
                quirk_string += "They are {0} and ".format(self.interactions())
            if self.mannerisms != None:
                quirk_string += "they {0}.".format(self.mannerisms())
            if self.ideals:
                quirk_string += "Their ideals are {0}, ".format(self.ideals())
            if self.bonds:
                quirk_string += "Their bonds are {0}, ".format(self.bonds())
            if self.flaws:
                quirk_string += "Their flaws are {0}.".format(self.flaws())
            quirk_strings.append(quirk_string)
        return quirk_strings

#from temp_ancestries import * # TEMP until I add saving/loading from JSON

def generate_npc(n,ancestry_table,quirk_table):
    npc_strings = []
    # ancestry components
    ancestries = ancestry_table.random_ancestry(n)
    genders = ancestry_table.random_gender(ancestries)
    names = ancestry_table.get_name(ancestries,genders)

    #quirks
    quirks = quirk_table.generate_quirks(n)

    for i in range(n):
        npc_string = "{2} is a {1} {0}. {3}".format(ancestries[i],genders[i],names[i],quirks[i])
        npc_strings.append(npc_string)
    return npc_strings

def npc(n=1,csv_export=False):
    """
    function to run from commandline for debugging
    """
    npcs = generate_npc(n,ancestry_table,quirk_table)
    for npc in npcs:
        print(npc)

    if csv_export:
        with open('npcs.csv', 'w', newline='') as csvfile:
            npcwriter = csv.writer(csvfile,delimiter=',')
            for npc in npcs:
                npcwriter.writerow([npc])

    

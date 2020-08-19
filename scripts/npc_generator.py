import numpy as np
import random

class ancestry:
    def __init__(self, ancestry, ancestry_weight, m_names, f_names, x_names, descriptions):
        """
        ancestry should be a string and is the name of the ancestry.
        ancestry_weight should be a positive integer between 1 and 100. The chance of an ancestry
        being selected from the ancestry_table will be ancestry_weight/sum(ancestry_weights). A race
        with a value of 1 will be rare, with a value of 100 it will be common.
        m_names, f_names, x_names and descriptions should all be lists of strings
        """
        self.ancestry = ancestry
        self.ancestry_weight = ancestry_weight
        self.m_names = m_names
        self.f_names = f_names
        self.x_names = x_names
        self.descriptions = descriptions

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

    def save_ancestry_table(self,filepaht): #TODO save to json
        pass

    def random(self,n):
        chosen_ancestry = random.choices(self.ancestries, weights=self.ancestry_weights, k=n)
        return chosen_ancestry

    def get_name(self,ancestry,gender):
        current_ancestry = self.ancestry_table[ancestry]
        if gender == 'm':
            names = current_ancestry.m_names
        elif gender == 'f':
            names = current_ancestry.f_names
        else:
            names = current_ancestry.x_names

        return random.choice(names)

from temp_ancestries import * # TEMP until I add saving/loading from JSON

def generate_npc(n,ancestry_table):
    npc_strings = []
    ancestry = ancestry_table.random(n)
    for npc in range(n):
        gender = random.choices(['m','f','x'],weights=[49.3,49.3,0.4])[0]
        print(gender)
        npc_string = ancestry_table.get_name(ancestry[npc],gender)
        npc_string += ", "
        npc_string += ancestry[npc]
        npc_strings.append(npc_string)
    return npc_strings

def npc(n=1):
    """
    function to run from commandline for debugging
    """
    for npc in generate_npc(n,ancestry_table):
        print(npc)

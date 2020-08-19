from npc_generator import *

dragonborn = ancestry('dragonborn',1,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])
dwarf = ancestry('dwarf',5,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])
elf = ancestry('elf',2,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])
gnome = ancestry('gnome',3,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])
halfelf = ancestry('half-elf',2,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])
halfling = ancestry('halfling',3,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])
halforc = ancestry('half-orc',2,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])
human = ancestry('human',5,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])
tiefling = ancestry('tiefling',1,['m1','m2','m3'],['f1','f2','f3'],['x1','x2','x3'],['d1','d2','d3'])

ancestries = {dragonborn.ancestry:dragonborn,
              dwarf.ancestry:dwarf,
              elf.ancestry:elf,
              gnome.ancestry:gnome,
              halfelf.ancestry:halfelf,
              halfling.ancestry:halfling,
              halforc.ancestry:halforc,
              human.ancestry:human,
              tiefling.ancestry:tiefling}

ancestry_table = ancestry_table(ancestries)

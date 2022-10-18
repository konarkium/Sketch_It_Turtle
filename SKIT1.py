"""Sketch it turtle: backbone, branch, double bond and elements"""

import numpy as np
import matplotlib.pyplot as plt

def rot(angle):
    return np.array([[np.cos(angle),-np.sin(angle)],
                     [np.sin(angle), np.cos(angle)]])
    
def Turtle(cmd, loc, stp=np.array([0.1,0])):
    loc_list = [loc]
    for c in cmd:
        if c[0] == 'F':    
            loc=loc+int(c[1:])*stp
            loc_list.append(loc)            
        else:
            if c[0] == 'L':
                T = rot(np.deg2rad(int(c[1:])))
                stp = T@stp
            else:
                T = rot(-np.deg2rad(int(c[1:])))
                stp = T@stp
    return loc_list

fig = plt.figure('stick_figures', figsize =(5 , 5), dpi = 300) 
ax = fig. add_subplot(aspect='equal')

#%% backbone chain

cmd1 = 'L30-F10-R60-F10-L60-F10-R60-F10'
cmd1 = cmd1.split(sep='-')

loc1 = np.array([1,2]) #starting position
        
loc_list1 = Turtle(cmd1, loc1)
x1,y1 = zip(*loc_list1)

"""plotting cmd1"""
ax.plot(x1,y1, color='k')

#%% line two

cmd2 = 'L90-F10-R60-F10-R60-F10-R60-F10'
cmd2 = cmd2.split(sep='-')

loc2 = np.array(loc_list1[1]) #using a point from loc_list1 as starting point
        
loc_list2 = Turtle(cmd2, loc2)
x2,y2 = zip(*loc_list2)

"""plotting cmd2"""
ax.plot(x2,y2, color='k')

#%% double bond

cmd3 = 'L30-F1-R90-F1-L90-F8'
cmd3 = cmd3.split(sep='-')

loc3 = np.array(loc_list2[1])
loc_list3 = Turtle(cmd3, loc3)
x3,y3 = zip(*loc_list3)
ax.plot(x3[2:],y3[2:],color='k')

#%% shapes n texts

from matplotlib.patches import Circle
circle = Circle((loc_list1[1][0],loc_list1[1][1]+0.04) , 0.2, 
                color='white', alpha=1,zorder=3)
ax.add_patch(circle)

ax.annotate('N', xy=(loc_list1[1]), ha='center', va='center')

ax.annotate('OH', xy=(loc_list1[-1]), ha='left', va='top')

plt.xlim(0,6)
plt.ylim(0,6)

plt.savefig('C:/Users/konar/Desktop/SKIT1.png', dpi=300,bbox_inches="tight")
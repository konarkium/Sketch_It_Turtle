"""Sketch it turtle: bonds above and below the plane"""

import numpy as np
import matplotlib.pyplot as plt

def rot(angle):
    return np.array([[np.cos(angle),-np.sin(angle)],
                     [np.sin(angle), np.cos(angle)]])
    
def Turtle(cmd, loc, stp=np.array([0.1,0])):
    loc_list = [loc]
    for c in cmd:
        if c[0] == 'F':
            loc=loc+float(c[1:])*stp
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

#%% solid structure: towards the plane

cmd4 = 'R70-F10'
cmd4 = cmd4.split(sep='-')

loc4 = np.array(loc_list1[2])

loc_list4 = Turtle(cmd4,loc4)

bond = np.linspace(loc_list4[0],loc_list4[1],100)
x4,y4 = zip(*bond)

for i,(x,y) in enumerate(zip(x4,y4),1):
    cmdb = f'L20-F{i/150}'
    cmdb = cmdb.split(sep='-')
    locb = np.array((x,y))
    loc_listb = Turtle(cmdb,locb)
    xb,yb = zip(*loc_listb)
    ax.plot(xb,yb,c='k')
    
    cmdb = f'R160-F{i/150}'
    cmdb = cmdb.split(sep='-')
    locb = np.array((x,y))
    loc_listb = Turtle(cmdb,locb)
    xb,yb = zip(*loc_listb)
    ax.plot(xb,yb,c='k')

#%% dashed structure: away from the plane

cmd5 = 'R110-F10'
cmd5 = cmd5.split(sep='-')

loc5 = np.array(loc_list1[2])

loc_list5 = Turtle(cmd5,loc5)

bond = np.linspace(loc_list5[0],loc_list5[1],100)
x5,y5 = zip(*bond)

for i,(x,y) in enumerate(zip(x5,y5),1):
    if i%10==0:
        cmdb = f'R20-F{i/150}'
        cmdb = cmdb.split(sep='-')
        locb = np.array((x,y))
        loc_listb = Turtle(cmdb,locb)
        xb,yb = zip(*loc_listb)
        ax.plot(xb,yb,c='k')
        
        cmdb = f'L160-F{i/150}'
        cmdb = cmdb.split(sep='-')
        locb = np.array((x,y))
        loc_listb = Turtle(cmdb,locb)
        xb,yb = zip(*loc_listb)
        ax.plot(xb,yb,c='k')

plt.xlim(0,5)
plt.ylim(0,5)

plt.savefig('C:/Users/konar/Desktop/SKIT2.png', dpi=300,bbox_inches="tight")

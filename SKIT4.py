"""Sketch it turtle: a common bond function"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib .patches import Arc
    
def turtle(cmd, loc, stp=np.array([0.1,0])):
    def rot(angle):
        return np.array([[np.cos(angle),-np.sin(angle)],
                         [np.sin(angle), np.cos(angle)]])
    cmd = cmd.split(sep='-')
    loc_list = [loc]
    for c in cmd:
        # moves 'F'orward 
        if c[0] == 'F':
            loc=loc+float(c[1:])*stp
            loc_list.append(loc) 
        # moves 'B'ackward
        elif c[0] == 'B':
            loc=loc-float(c[1:])*stp
            loc_list.append(loc)   
        # applying the rotational matrix
        else:
            # Turns 'L'eft
            if c[0] == 'L':
                T = rot(np.deg2rad(float(c[1:])))
                stp = T@stp
            # Turns 'R'ight
            elif c[0] == 'R':
                T = rot(-np.deg2rad(float(c[1:])))
                stp = T@stp
    return loc_list

def plot(loc_list,s=0,c='k'):
    x,y = zip(*loc_list)
    ax.plot(x[s:],y[s:],c=c)

def bond(cmd, loc, kind='n', m=1):
    #first extract and define value of theta
    x=0
    for i,n in enumerate(cmd[1:]):
        if n.isdigit():
            continue
        else:
            x = i
            break  
    theta = int(cmd[1:x+1]) 
    if cmd[0]=='L':
        theta = theta
    elif cmd[0]=='R':
        if theta <=90:
            theta = -theta    
        elif theta > 90:
            theta = 180-theta
    #convert commands into co-ordinates
    loc_list = turtle(cmd,loc)    
    bond = np.linspace(loc_list[0],loc_list[1],100)
    x,y = zip(*bond[10:])
    # 'w' for wave
    if kind=='w': 
        for i,(x,y) in enumerate(zip(x,y)):
            if i%20==0: 
                arc = Arc(xy=(x,y), width=0.1, height=0.15,
                          angle=theta, theta1=180, theta2=360)
            elif i%10==0:
                arc = Arc(xy=(x,y), width=0.1, height=0.15,
                          angle=theta, theta1=0, theta2=180)
            ax.add_patch(arc)
    # 'e'xtra bonds aka double n triple bonds
    elif kind[0] =='e':
        if kind[1] == 'l':
            cmd = f'L{abs(theta)}-F1-L90-F1-R90-F8' 
        elif kind[1] == 'r':
            cmd = f'L{abs(theta)}-F1-R90-F1-L90-F8'
        loc_list = turtle(cmd,loc)
        plot(loc_list,s=2,c='k') 
    # bonds above n below the plane and co-ord bonds
    else:
        for i,(x,y) in enumerate(zip(x,y)):
            # if m = 1: solid bond; if m = 10: dashed bond
            if i%m==0:
                # v for 'v'type
                if kind == 'v': 
                    cmd = f'L{abs(90+theta)}-F{i/100}-B{i/100}-B{i/100}'
                # n for normal
                elif kind =='n': 
                    cmd = f'L{abs(90+theta)}-F0.5-B0.5-B0.5'
                loc = np.array((x,y))
                loc_list = turtle(cmd,loc)
                plot(loc_list,c='k')   

fig = plt.figure('stick_figures', figsize =(5 , 5), dpi = 300) 
ax = fig. add_subplot(aspect='equal')

bb = 'L30-F10-R60-F10-R60-F10-R60-F10-R60-F10-R60-F10-B10-L120-F10-R60-F10-R60-F10-R60-F10-R60-F10'
lb = np.array([3,3])
loc_lb = turtle(bb, lb)
plot(loc_lb)

b = 'L90-F10'
l = np.array(loc_lb[1])
bond(b, l, 'w')

b = 'R30-F10'
l = np.array(loc_lb[1])
bond(b, l, 'v')

b = 'R90-F10'
l = np.array(loc_lb[2])
bond(b, l, 'n')

b = 'L30-F10'
l = np.array(loc_lb[4])
bond(b, l, 'v')

b = 'R90-F10'
l = np.array(loc_lb[4])
bond(b, l, 'w')

b = 'L90-F10'
l = np.array(loc_lb[5])
bond(b, l, 'el')

b = 'R90-F10'
l = np.array(loc_lb[8])
bond(b, l, 'v',10)

b = 'R150-F10'
l = np.array(loc_lb[9])
bond(b, l, 'n',10)

b = 'L30-F10'
l = np.array(loc_lb[10])
bond(b, l, 'el',10)

b = 'L30-F10'
l = np.array(loc_lb[10])
bond(b, l, 'er',10)

plt.xlim(0,6)
plt.ylim(0,5)
    
plt.savefig('C:/Users/konar/Desktop/SKIT4.png', dpi=300,bbox_inches="tight")
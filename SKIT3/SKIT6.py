"""SKIT6: major revision: rewrote bond function"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
font_properties = {'family':'Cambria', #name
                   'weight':'bold',            #type
                   'size':15}                  #size
rc('font',**font_properties)
from matplotlib .patches import Arc, Circle
    
def turtle(cmd, loc, stp=np.array([0.1,0])):
    def rot(angle):
        return np.array([[np.cos(angle),-np.sin(angle)],
                         [np.sin(angle), np.cos(angle)]])
    cmd = cmd.split(sep='-')
    loc = np.array(loc)
    loc_list = [loc]
    for c in cmd:
        # moves 'F'orward 
        if c[0] == 'f' or c[0] == 'F':
            loc=loc+float(c[1:])*stp
            loc_list.append(loc) 
        # moves 'B'ackward
        elif c[0] == 'b' or c[0] == 'B':
            loc=loc-float(c[1:])*stp
            loc_list.append(loc)   
        # applying the rotational matrix
        else:
            # Turns 'L'eft
            if c[0] == 'l' or c[0] == 'L':
                T = rot(np.deg2rad(float(c[1:])))
                stp = T@stp
            # Turns 'R'ight
            elif c[0] == 'r' or c[0] == 'R':
                T = rot(-np.deg2rad(float(c[1:])))
                stp = T@stp
    return loc_list

def plot(loc_list,s=0,c='k'):
    x,y = zip(*loc_list)
    ax.plot(x[s:],y[s:],c=c)

def text(text,loc_l,loc,ha=0,va=0):
    x,y = loc_l[loc][0], loc_l[loc][1]
    circle = Circle((x,y+0.05), 0.2, 
                    color='white',zorder=3)#, alpha=0.5)
    ax.add_patch(circle)
    ax.text(x+ha, y+va, text, ha='center', va='center')

def bond(loc, theta='L0', steps=10, kind='n', seg=1):
    if theta[0] == 'R' or theta[0] == 'r':
        theta = 360-float(theta[1:])
    else:
        theta = float(theta[1:])
    cmd = f"L{theta}-F{steps}"
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
            cmd = f'l{theta}-f1-l90-f1-r90-f{steps-2}' 
        elif kind[1] == 'r':
            cmd = f'l{theta}-f1-r90-f1-l90-f{steps-2}'
        loc_list = turtle(cmd,loc)
        plot(loc_list,s=2,c='k') 
    # bonds above n below the plane and co-ord bonds
    else:
        for i,(x,y) in enumerate(zip(x,y)):
            # if m = 1: solid bond; if m = 10: dashed bond
            if i%seg==0:
                # v for 'v'type
                if kind == 'v': 
                    cmd = f'l{abs(90+theta)}-f{i/100}-b{i/100}-b{i/100}'
                # n for normal
                elif kind =='n': 
                    cmd = f'l{abs(90+theta)}-f0.5-b0.5-b0.5'
                loc = np.array((x,y))
                loc_list = turtle(cmd,loc)
                plot(loc_list,c='k')   

fig = plt.figure('stick_figures', figsize =(5 , 5), dpi = 300) 
ax = fig. add_subplot(aspect='equal')

bb = 'L30-F10-L60-F10-R60-F10-L60-F10-B10-R120-F10-R60-F10-L60-F10-B10-R120-F10-R60-F10'
lb = np.array([1,1])
loc_lb = turtle(bb, lb)
plot(loc_lb)

bond(loc=loc_lb[1], theta='l90',steps=10,kind='er',seg=5)
bond(loc=loc_lb[3], theta='r30',steps=10,kind='er',seg=5)
bond(loc=loc_lb[10], theta='l30',steps=10,kind='el',seg=5)

text('N',loc_lb, 2)
text('N',loc_lb, 6)    
text('N',loc_lb, 10)

text('H$_{2}$N',loc_lb, 0, ha=-0.17)  
text('NH$_{2}$',loc_lb, 4, ha=0.19) 
text('NH$_{2}$',loc_lb, 8, ha=0.15) 

plt.xlim(0,6)
plt.ylim(0,6)
    
plt.savefig('C:/Users/konar/Desktop/SKIT6.png', dpi=300,bbox_inches="tight")


"""
Created on Fri Nov 11 17:38:12 2022
SKIT 8.1: brackets, some more examples
@author: konar
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
font_properties = {'family':'Cambria', 'weight':'bold', 'size':12} 
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

def text(text,loc_l,loc,ha=0,va=0,halo=0.2, haloha = 0, halova = 0):
    x,y = loc_l[loc][0], loc_l[loc][1]
    circle = Circle((x+ha,y+va+0.05), halo, 
                    color='white',zorder=3)#, alpha=0.5)
    ax.add_patch(circle)
    ax.text(x+ha, y+va, text, ha='center', va='center')

def bracket(loc_l, loc=(0,-1), rad = 2, angle = 0, theta = 30):
    loc1, loc2 = loc
    brac_loc = (loc_l[loc1]+loc_l[loc2])/2
    x,y = brac_loc
    arc = Arc(xy=(x,y), width=rad, height=rad, 
              angle=angle, theta1=-theta, theta2=theta)
    ax.add_patch(arc)
    arc = Arc(xy=(x,y), width=rad, height=rad,
              angle=angle, theta1=180-theta, theta2=theta-180)
    ax.add_patch(arc)

def direc_angle(theta):
    if theta[0] == 'R' or theta[0] == 'r':
        theta = 360-float(theta[1:])
    else:
        theta = float(theta[1:])
    return theta

def bond(loc, theta='L0', kind='n',steps=10, seg=1):
    theta = direc_angle(theta)
    cmd = f"L{theta}-F{steps}"
    loc_list = turtle(cmd,loc)    
    bond = np.linspace(loc_list[0],loc_list[1],10*steps)
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

fig = plt.figure('stick_figures', figsize = (5,5), dpi = 300) 
ax = fig. add_subplot(aspect='equal')

bb = 'r30-f10-L60-F10-r60-f10-L60-F10-r60-f10'
lb = [2,3]
loc_lb = turtle(bb, lb)
plot(loc_lb)

bracket(loc_l = loc_lb, loc=(0,3), rad = 1.5)
text('x', loc_lb, 2, ha = 0.4, va = -0.8, halo = 0)

bracket(loc_l = loc_lb, loc=(2,-1), rad = 1.5)
text('1-x', loc_lb, 4, ha = 0.55, va = -0.8, halo = 0)

bb = 'L90-F2-r15-f2-r15-f2-r15-f2-r15-f2-r15-f2-r15-f2'
lb = loc_lb[2]
loc_lb = turtle(bb, lb)
# plot(loc_lb)

bond(loc=loc_lb[0],theta='l90',kind='w',steps=3)
bond(loc=loc_lb[1],theta='l75',kind='w',steps=3)
bond(loc=loc_lb[2],theta='l60',kind='w',steps=3)
bond(loc=loc_lb[3],theta='l45',kind='w',steps=3)
bond(loc=loc_lb[4],theta='l30',kind='w',steps=3)
bond(loc=loc_lb[5],theta='l15',kind='w',steps=3)
# bond(loc=loc_lb[6],theta='l0',kind='w',steps=3)

bb = 'r30-f10-L60-F10-r60-f10'
lb = loc_lb[7]
loc_lb = turtle(bb, lb)
plot(loc_lb)

text('CH$_3$',loc_l=loc_lb,loc=3, ha=0.4, va=-0.1, halo = 0.4)

bracket(loc_l = loc_lb, rad = 1.5)
text('n', loc_lb, 2, ha = 0.4, va = -0.8, halo = 0)

#%% PET

bb = 'r30-f10-r60-f10-b10-l120-f10-l60-f10-r60-f10-r60-f10-l60-f10-l60-f10-b10-r120-f10-l60-f10-r60-f10-l60-f10-r60-f10'
lb = [0.5,6]
loc_lb = turtle(bb,lb)
plot(loc_lb)

br = 'r30-f10-l60-f10-l60-f10'
lr = loc_lb[4]
loc_lr = turtle(br,lr)
plot(loc_lr)

bond(loc=loc_lb[4],theta = 'l90', kind = 'er')
bond(loc=loc_lb[6],theta = 'r30', kind = 'er')
bond(loc=loc_lr[1],theta = 'l30', kind = 'el')

bond(loc=loc_lb[1],theta = 'r90', kind = 'el')
bond(loc=loc_lb[8],theta = 'l90', kind = 'el')

text('O',loc_l=loc_lb,loc=2, ha=0.048, halo=0.25)
text('O',loc_l=loc_lb,loc=9, ha=-0.05, halo=0.25)
text('O',loc_l=loc_lb,loc=11)
text('O',loc_l=loc_lb,loc=14)

bracket(loc_l=loc_lb, rad = 8.25, theta = 20)
text('n', loc_lb, loc=-1, ha = -0.2, va = -2, halo = 0)

plt.xlim(0,10)
plt.ylim(0,10)
    
plt.savefig('C:/Users/konar/Desktop/branch.png', dpi=300,bbox_inches="tight")



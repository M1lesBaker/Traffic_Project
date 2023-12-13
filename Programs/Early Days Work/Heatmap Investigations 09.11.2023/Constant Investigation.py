import numpy as np
import matplotlib.pyplot as plt
import pygame
import math

pygame.init()

#constants
min_distance = 5 #pixels
accel_max = 2 #pixels/second^2 Comfortable accleration
decel_max = 2.4 #pixels/second^2 Comfortable deceleration
n = 5 #number of cars
dt = 0.016667
fps = 60
timer = pygame.time.Clock()

position_transfer = 0
velocity_transfer = 0
acceleration_transfer = 0

class Car:

    def __init__(self, lane,start, pos, speed, acceleration, length, mass, colour,speed_des, t_react, id):
        self.lane = lane
        self.start = start
        self.pos = pos
        self.speed = speed
        self.acceleration = acceleration
        self.length = length
        self.mass = mass
        self.colour = colour
        self.speed_des = speed_des
        self.t_react = t_react
        self.id = id

    def draw(self):
        self.rectangle = pygame.draw.polygon(screen, self.colour,[(self.start, self.pos), (self.start + 15, self.pos), (self.start + 15,self.pos + self.length),(self.start, self.pos + self.length)])
        #self.rectangle = pygame.draw.polygon(screen, self.colour, [(400, self.pos), (400 + 15, self.pos),
                                                                   #(400 + 15, 400 + self.length),
                                                                   #(400, self.pos + self.length)])




    def suvat(self):
        #if self.speed < 41:
        self.speed += (self.acceleration * dt)

        #elif self.speed < 0:
        #self.speed = 0


        #else:
        #    self.speed = 31
        return self.speed

    def pos_update(self):
        self.pos += (self.speed * dt) + (0.5 * self.acceleration * (dt ** 2))
        return self.pos

    def data_collect(self):
        position.append(self.pos)
        velocity1.append(self.speed)
        acceleration1.append(self.acceleration)

    def point_data(self):
        position_transfer = self.pos
        velocity_transfer = self.speed
        acceleration_transfer = self.acceleration


class Road:

    def __init__(self, lanes, lanewidth, x_pos):
        self.lanes = lanes
        self.lanewidth = lanewidth
        self.x_pos = x_pos

    def draw(self):
        self.rectangle = pygame.draw.polygon(screen, 'black',
                                             [(self.x_pos, 0), (self.x_pos + (self.lanes * self.lanewidth), 0),
                                              (self.x_pos + (self.lanes * self.lanewidth), HEIGHT),
                                              (self.x_pos, HEIGHT)])

#acceleration calculation
def accel(velocity, reaction, speed_diff, position_diff,max_speed,smoothness):
    s_star = min_distance + velocity*reaction + ((velocity * speed_diff) / (2*np.sqrt(accel_max * decel_max)))
    return accel_max * (1 - ((velocity / max_speed) ** smoothness) - ((s_star / position_diff) ** 2))

#objects


#while loop breaking structures
import time as tn

def sim_length(time): #in seconds
    frames = time / 0.0166666666666666667
    return math.trunc(frames)





delta = []
sample_length = 45

frame_tot = sim_length(sample_length) #
position = np.zeros((49,frame_tot))
print('WARNING! This Graph will take '+ str((sample_length*49)/60)+ ' minutes to compute')
for i in range(1,50): #cannot get decimals so will build this into code/
    car1 = Car(1,400,250, 15, 1, 5, 1000, 'blue', 30, 1.5,0) #reset car each interation
    r_delta = i/10
    # graph lists


    time = []

    n = 0

    run = True
    while run:
        #frame rate control
        timer.tick(fps)

        #calculate car position,acceleration at nth frame
        car1.acceleration = accel(car1.speed, car1.t_react, 0, 100000000000000000000, car1.speed_des,r_delta) # calculates acceleration
        car1.suvat() #calulcates speed
        car1.pos_update() # calculates position

        position[i-1,n] = car1.acceleration #f(x,y)
        #velocity1.append(car1.speed)
        #acceleration1.append(car1.acceleration)







        #car1.point_data()
        #print(position_transfer)
        #print(velocity_transfer)
        n += 1
        if n > frame_tot-1:
            break
    delta.append(r_delta)
    #print(position)

#graph plotting

def time_tick(interval, frames):
    for i in range(frames):
        t = i * interval
        time.append(t)
    return time

#3D Graph
from mpl_toolkits import mplot3d
fig = plt.figure()
X,Y = np.meshgrid(time_tick(dt,frame_tot),delta) # makes the grid to plot on
Z = position #what we are investigating
ax = plt.axes(projection='3d')
ax.plot_surface(X,Y,Z,cmap='viridis', edgecolor='none')
ax.set_title('Surface plot')
ax.set_xlabel('Time', labelpad=20)
ax.set_ylabel('Delta', labelpad=20)
ax.set_zlabel('Acceleration', labelpad=20)

#Heat Map


plt.show()

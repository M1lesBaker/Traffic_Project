import numpy as np
import matplotlib.pyplot as plt
import pygame
import math
from datetime import datetime
pygame.init()


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


    def suvat(self): #controls speed calculated from acceleration
        self.speed += (self.acceleration * dt)
        return self.speed

    def pos_update(self): #controls position calculated from speed
        self.pos += (self.speed * dt) + (0.5 * self.acceleration * (dt ** 2))
        return self.pos

    def data_collect(self):
        position.append(self.pos)
        velocity1.append(self.speed)
        acceleration1.append(self.acceleration) #not used

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
def accel(velocity, reaction, speed_diff, position_diff,max_speed,decel_max):
    s_star = min_distance + velocity*reaction + ((velocity * speed_diff) / (2*np.sqrt(accel_max * decel_max)))
    return accel_max * (1 - ((velocity / max_speed) ** delta) - ((s_star / position_diff) ** 2))


#Simulation time calculator - necessary to show warning at beginning of code
def sim_length(time): #in seconds
    frames = time / 0.01666667
    return math.trunc(frames)

def sim_time_calcuclator(sample_length,start,stop,increment):
    if (sample_length*(stop-start))/(60*increment) < 1:
        return 'WARNING! This Graph will take '+ str(int((sample_length*(stop-start))/(increment))) + ' seconds to compute'
    else:
        return 'WARNING! This Graph will take '+ str(int((sample_length*(stop-start))/(60*increment)))+ ' minutes to compute'

def total_time(sample_length,start,stop,increment):
    return (sample_length*(stop-start))/(increment) #total time in seconds


#constants
min_distance = 2 #pixels
accel_max = 2 #pixels/second^2 Comfortable accleration
#decel_max = 3 #pixels/second^2 Comfortable deceleration
delta = 3 #dimensionless
reaction = 0.67
dt = 0.016667
fps = 60
timer = pygame.time.Clock()

#setup
sample_length = 95 #in seconds/increment
start = 1 #start variable
stop =  5 #end variable
increment = 1 #difference between 1 point and the next point in variable under investigation

#lists
variable = [] #variable is the thing we are iterating over and investigating
time = []

#START CALCULATION OF SIM TIME
frame_tot = sim_length(sample_length) #total frames per variable (delta/a/b/etc.)
Z = np.zeros((int((stop-start)/increment),frame_tot))
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
print(sim_time_calcuclator(sample_length,start,stop,increment))

#WIDTH = 1000
#HEIGHT = 800
#screen = pygame.display.set_mode([WIDTH, HEIGHT])

#START MAIN LOOP
for i in range(int(start/increment),int(stop/increment)): #cannot get decimals so will build this into code/
    car1 = Car(1,400,2000, 0, 0, 5, 1000, 'blue', 30, reaction,0) #reset car each interation
    car2 = Car(1, 400, 1, 0, 0, 5, 1000, 'green', 30, reaction, 1)
    r_variable= i*increment

    print('NEW R_Variable' + str(r_variable))
    n = 0
    del_s2 = 1000000000000000000000000000
    del_v2 = 0

    run = True
    while run:
        #frame rate control
        timer.tick(fps)
        #screen.fill('darkgreen')



        #calculate car position,acceleration at nth frame

        #car1.acceleration = accel(car1.speed, 0.67, 0, 100000000000000000000, car1.speed_des, 3) # calculates acceleration
        car1.suvat() #calclates speed
        car1.pos_update() # calculates position from speed

        # speed difference between vehicle in front and current vehicle (lower number is in front)
        del_v2 = car2.speed - car1.speed
        del_s2 = car2.pos - car1.pos - car2.length

        car2.acceleration = accel(car2.speed, car2.t_react, del_v2, del_s2, car2.speed_des, r_variable)
        car2.suvat()
        car2.pos_update()

        #print(car2.acceleration)
        #car1.draw()
        #car2.draw()
        Z[int(stop/increment)-1-i,n] = car2.acceleration #f(x,y) #calculate start/increment and subtract this off i
        #pygame.display.flip()
        n += 1
        if n > frame_tot-1:
            break
    variable.append(r_variable)

print(Z)
print(variable)
#graph plotting
def time_tick(interval, frames):
    for i in range(frames):
        t = i * interval
        time.append(t)
    return time

#3D Graph
from mpl_toolkits import mplot3d
#fig = plt.figure()
X,Y = np.meshgrid(time_tick(dt,frame_tot),variable) # makes the grid to plot on
 #what we are investigating
#ax1 = plt.axes(projection='3d')
#ax1.plot_surface(X,Y,Z,cmap='viridis', edgecolor='none')
#ax1.set_title('Surface plot')
#ax1.set_xlabel('Time', labelpad=20)
#ax1.set_ylabel('Delta', labelpad=20)
#ax1.set_zlabel('Acceleration', labelpad=20)
T = time_tick(dt,frame_tot)
np.save("datax.npy", X)
np.save("datay.npy", Y)
np.save("dataz.npy", Z)
np.save('datat.npy',T)

np.savetxt('datax.txt', X, delimiter = ',' )
np.savetxt('datay.txt', Y, delimiter = ',' )
np.savetxt('dataz.txt', Z, delimiter = ',' )
np.savetxt('datat.txt', T, delimiter = ',' )


#Heat Map
plt.figure(figsize=(7,7), dpi=100)
plt.contour(X,Y, Z, linewidths = 0.01, colors = 'k')
plt.imshow(Z, cmap = 'jet', interpolation = 'none', extent = [min(time_tick(dt,frame_tot)),max(time_tick(dt,frame_tot)),min(variable),max(variable)])
plt.xlabel('Time $(s)$', labelpad=20)
plt.ylabel('$b$ - Comfortable Acceleration $(m/s/s)$', labelpad=20)
plt.colorbar().set_label("Acceleration $(m/s/s)$")


plt.show()
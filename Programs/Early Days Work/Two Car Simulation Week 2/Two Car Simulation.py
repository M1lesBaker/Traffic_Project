import numpy as np
import matplotlib.pyplot as plt
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 60
timer = pygame.time.Clock()





# simulation variables same for all cars
min_distance = 2 #pixels
smoothness = 2 #acceleration exponent (might move to variable soon)
accel_max = 2 #pixels/second^2 Comfortable accleration
decel_max = 5 #pixels/second^2 Comfortable deceleration
n = 5 #number of cars
dt = 0.016667

#data structures
baker_matrix = np.zeros((n,3)) #3 elements for car id, position and speed

# graph lists
position = []
velocity1 = []
acceleration1 = []
time = []


# simulation classes
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

    def data_collect(self):
        position.append(self.pos)
        velocity1.append(self.speed)
        acceleration1.append(self.acceleration)


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

#objects
car1 = Car(1,400,500, 15, 0, 5, 1000, 'blue', 15, 1.5,0)
car2 = Car(1,400,20, 30, 0, 5, 1000, 'green', 30, 2,2)
#car3 = Car(1,400,100, 30, 1, 5, 1000, 'red', 30, 1.5,3)
#car4 = Car(1,400,50, 30, 1, 5, 1000,'white', 30, 1.5,4)
#car5 = Car(1,400,0, 30, 1, 5, 1000, 'yellow', 30, 1.5,5)
road1 = Road(1, 21, 397)
#cars = [car1, car2, car3, car4, car5]

#acceleration calculation
def accel(velocity, reaction, speed_diff, position_diff,max_speed):
    s_star = min_distance + velocity*reaction + ((velocity * speed_diff) / (2*np.sqrt(accel_max * decel_max)))
    return accel_max * (1 - ((velocity / max_speed) ** smoothness)  - ((s_star / position_diff) ** 2))

# simulation loop
run = True
while run:
    timer.tick(fps)

    #draw road and background
    screen.fill('darkgreen')
    road1.draw()
    #car1.acceleration = accel(car1.speed, car1.t_react, 0, 100000000000000000000, car1.speed_des)

    # speed difference between vehicle in front and current vehicle (lower number is in front)
    del_v2 = (car2.speed - car1.speed)
    del_s2 = car1.pos - car2.pos - car2.length
    car2.acceleration = accel(car2.speed, car2.t_react, del_v2, del_s2,car2.speed_des)

    #print(car1.speed)
 #   del_v3 = car3.speed - car2.speed
  #  del_s3 = car3.pos - car2.pos - car3.length
   # car3.acceleration = accel(car3.speed, car3.t_react, del_v3, del_s3, car3.speed_des)

   # del_v4 = car4.speed - car3.speed
   # del_s4 = car4.pos - car3.pos - car4.length
   # car4.acceleration = accel(car4.speed, car4.t_react, del_v4, del_s4, car4.speed_des)

   # del_v5 = car5.speed - car4.speed
   # del_s5 = car5.pos - car4.pos - car5.length
   # car5.acceleration = accel(car5.speed, car5.t_react, del_v5, del_s5, car5.speed_des)

#car 1
    car1.suvat()
    car1.pos_update()
    car1.draw()
#car 2
    car2.suvat()
    car2.pos_update()
    car2.draw()
#car 3
 #   car3.suvat()
 #   car3.pos_update()
 #   car3.draw()
#car 4
 #   car4.suvat()
 #   car4.pos_update()
 #   car4.draw()
#car 5
 #   car5.suvat()
 #   car5.pos_update()
 #   car5.draw()

#data collection
    car2.data_collect()
    #car2.data_collect()
    #car3.data_collect()
    #print(car2.speed-car1.speed)
    #car4.data_collect()
    #car5.data_collect()
#print(car2.pos,car2.speed,car2.acceleration)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()


# Graph 1 (Outside Simulation Loop)
def time_tick(interval, frames):
    for i in range(frames):
        t = i * interval
        time.append(t)
    return time


def suvat_graph(time, graph_position, graph_speed, graph_acceleration):
    #plt.xlabel('Time ($s$)')
    #plt.ylabel('Velocity ($v$)')
    fig, ax1 = plt.subplots()


    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Acceleration (ms$^{-2}$)')
    ax1.plot(time, graph_acceleration, color = 'red', label = 'Acceleration $(m/s/s)$')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Velocity (ms$^{-1}$)')
    ax2.plot(time, graph_speed, color = 'blue', label = 'Velocity $(m/s)$')

    #ax3 = ax1.twinx()
    #ax3.set_ylabel('Acceleration $(m/s/s)$')
    #ax3.plot(time, graph_acceleration, color = 'red', label = 'Acceleration $(m/s/s)$')
    #plt.legend(loc='upper right')
    plt.show()


# time_tick(0.016666667, len(velocity1))
suvat_graph(time_tick(dt, len(position)), position,velocity1, acceleration1)

#saving data
T = time_tick(dt, len(position))
X = velocity1
Y = acceleration1
Z = position
print(X)
print(Y)
np.save("datax.npy", X)
np.save("datay.npy", Y)
np.save("dataz.npy", Z)
np.save('datat.npy',T)

np.savetxt('datax.txt', X, delimiter = ',' )
np.savetxt('datay.txt', Y, delimiter = ',' )
np.savetxt('dataz.txt', Z, delimiter = ',' )
np.savetxt('datat.txt', T, delimiter = ',' )





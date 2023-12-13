import numpy as np
import matplotlib.pyplot as plt
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 60
timer = pygame.time.Clock()

# simulation variables same for all cars
min_distance = 2 #pixels
smoothness = 1 #acceleration exponent (might move to variable soon)
accel_max = 2 #pixels/second^2 Comfortable accleration
decel_max = 2 #pixels/second^2 Comfortable deceleration
dt = 0.016667

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
        if self.lane == 1:
            self.rectangle = pygame.draw.polygon(screen, self.colour,[(self.start, self.pos), (self.start + 15, self.pos), (self.start + 15,self.pos + self.length),(self.start, self.pos + self.length)])
        elif self.lane == 2:
            self.rectangle = pygame.draw.polygon(screen, self.colour,
                                                 [(self.start + 21, self.pos), (self.start + 21 + 15, self.pos),
                                                  (self.start +21 + 15, self.pos + self.length),
                                                  (self.start +21, self.pos + self.length)])
    def suvat(self):
        self.speed += (self.acceleration * dt)
        return self.speed

    def pos_update(self):
        self.pos += (self.speed * dt) + (0.5 * self.acceleration * (dt ** 2))
        return self.pos

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

def accel(velocity, reaction, speed_diff, position_diff,max_speed):
    s_star = min_distance + velocity*reaction + ((velocity * speed_diff) / (2*np.sqrt(accel_max * decel_max)))
    return accel_max * (1 - ((velocity / max_speed) ** smoothness)  - ((s_star / position_diff) ** 2))
#make cars

carA = Car(1,400,2, 100, 0, 5, 1000, 'darkgreen', 100, 0.67,1)
carB = Car(1,400,400, 15, 0, 5, 1000, 'red', 15, 0.2,2)
#carC = Car(1,400,50, 30, 0, 5, 1000, 'green', 30, 1.5,3)
#carD = Car(1,400,70, 12, 0, 5, 1000, 'purple', 30, 1.5,4)
#carE = Car(1,400,90, 13, 0, 5, 1000, 'yellow', 30, 1.5,5)
#carF = Car(1,400,110, 10, 0, 5, 1000, 'blue', 30, 1.5,6)
#carG = Car(1,400,130, 14, 0, 5, 1000, 'pink', 30, 1.5,7)
#carH = Car(1,400,150, 15, 0, 5, 1000, 'blue', 30, 1.5,8)
#carZ = Car(1,400,400, 20, 0, 5, 1000, 'green', 30, 1.5,9)
carEND = Car(1,400,1, 0, 0, 5, 1000, 'black', 30, 1.5,10)
carSTART = Car(1,400,500000, 0, 0, 5, 1000, 'black', 30, 1.5,10)
cars = [carA,carB]#, carC, carD, carE, carF, carG, carH, carZ] # carB, carC, carD, carE, carF, carG,
road1 = Road(2, 21, 397)
from operator import attrgetter
lane1 = []
lane2 = []
lane3 = []
lane4 = []
def sort_lanes(cars): # sorts cars by lane and then pos
    cars = sorted(cars, key=attrgetter('lane', 'pos'))
    for car in cars:
        if car.lane == 1:
            lane1.append(car)
        if car.lane == 2:
            lane2.append(car)
        if car.lane == 3:
            lane3.append(car)
        if car.lane == 4:
            lane4.append(car)

sort_lanes(cars)
carspos = cars

carspos = sorted(carspos, key=attrgetter('pos'), reverse = True)

run = True
while run:
    timer.tick(fps)
    screen.fill('darkgreen')
    road1.draw()
    sort_lanes(cars)
    lane1_rev = lane1[::-1]
    lane2_rev = lane2[::-1]
    carspos = sorted(carspos, key=attrgetter('pos'), reverse=True)
    carspos[0].acceleration = accel(carspos[0].speed, 0.67, 0, 100000000000000000000, carspos[0].speed_des)  # calculates acceleration
    carspos[0].suvat()
    carspos[0].pos_update()
    carspos[0].draw()
    for index, car in enumerate(carspos):
        if index < len(carspos) - 1:
            del_v1 = carspos[index+1].speed - carspos[index].speed
            del_s1 = carspos[index].pos - carspos[index+1].pos - carspos[index].length
            carspos[index+1].acceleration = accel(car.speed, car.t_react, del_v1, del_s1, car.speed_des)
            carspos[index+1].suvat()
            carspos[index+1].pos_update()
            carspos[index+1].draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()
import numpy as np
import matplotlib.pyplot as plt
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 90
timer = pygame.time.Clock()

# simulation variables same for all cars
min_distance = 5 #pixels
smoothness = 2 #acceleration exponent (might move to variable soon)
accel_max = 2 #pixels/second^2 Comfortable accleration
decel_max = 3 #pixels/second^2 Comfortable deceleration
dt = 0.01111111111112

# simulation classes
class Car:

    def __init__(self, lane,start, pos, speed, acceleration, length, politeness, colour,speed_des, t_react, thresh, id):
        self.lane = lane
        self.start = start
        self.pos = pos
        self.speed = speed
        self.acceleration = acceleration
        self.length = length
        self.politeness = politeness
        self.colour = colour
        self.speed_des = speed_des
        self.t_react = t_react
        self.thresh = thresh
        self.id = id

    def draw(self):
        if self.lane == 1:
            self.rectangle = pygame.draw.polygon(screen, self.colour,[(self.start, self.pos), (self.start + 15, self.pos), (self.start + 15,self.pos - self.length),(self.start, self.pos - self.length)])
        elif self.lane == 2:
            self.rectangle = pygame.draw.polygon(screen, self.colour,
                                                 [(self.start + 21, self.pos), (self.start + 21 + 15, self.pos),
                                                  (self.start +21 + 15, self.pos - self.length),
                                                  (self.start +21, self.pos - self.length)])
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

#carA = Car(2,400,250, 30, 0, 5, 1000, 'darkgreen', 30, 1.5,1)
carB = Car(1,400,500,5 , 0, 250, 0.1, 'red', 5, 1.5, 0.5,2)
carC = Car(2,400,280, 30, 0, 5, 1, 'green', 30, 1.5, 0.5,3)
carD = Car(2,400,220, 30, 0, 5, 1, 'purple', 30, 1.5,0.5,4)
carE = Car(1,400,200, 30, 0, 5, 1, 'yellow', 30, 1.5,0.5,5)
carF = Car(1,400,180, 30, 0, 5, 0, 'blue', 30, 1.5,0.5,6)
carG = Car(1,400,150, 30, 0, 5, 1, 'pink', 30, 1.5,0.5,7)
carH = Car(1,400,130, 30, 0, 5, 0, 'blue', 30, 1.5,0.5,8)
carZ = Car(1,400,100, 30, 0, 5, 1, 'green', 30, 1.5,0.5,9)
car1 = Car(2,400,90, 30, 0, 30, 10, 'purple', 30, 1.5,0.5,11)
car2 = Car(1,400,700, 0, 0, 30, 0, 'yellow', 0.1, 1.5,0.5,12)
#car3 = Car(2,400,70, 10, 0, 5, 1, 'blue', 30, 1.5,0.5,13)
#car4 = Car(2,400,250, 14, 0, 5, 1, 'pink', 30, 1.5,0.5,14)
#car5 = Car(2,400,700, 15, 0, 5, 1, 'blue', 30, 1.5,0.5,15)
#car6 = Car(2,400,180, 20, 0, 5, 1, 'green', 30, 1.5,0.5,16)
#car7 = Car(2,400,230, 30, 0, 5, 1, 'purple', 30, 1.5,0.5,17)
#car8 = Car(2,400,255, 15, 0, 5, 1, 'yellow', 15, 1.5,0.5,18)
#car9 = Car(2,400,366, 10, 0, 5, 1, 'blue', 30, 1.5,0.5,19)
#car10 = Car(2,400,320, 14, 0, 5, 1, 'pink', 30, 1.5,0.5,20)
#car11 = Car(2,400,310, 15, 0, 5, 1, 'blue', 30, 1.5,0.5,21)
#car12 = Car(2,400,500, 5, 0, 5, 1, 'green', 5, 1.5,0.5,22)
#carEND = Car(1,400,50000000, 0.00001, 0, 5, 1000, 'blue', 0.00001, 1.5,10)
#carSTART = Car(1,400,0, 0.000001, 0, 5, 1000, 'pink', 0.00001, 1.5,10)
cars = [carB, carC, carD, carE, carF, carG, carH, carZ, car1, car2]#, car3, car4,car5,car6]#,car7,car8,car9,car10,car11,car12] # carB, carC, carD, carE, carF, carG,
road1 = Road(2, 21, 397)
from operator import attrgetter

lane1 = []
lane2 = []
lane3 = []
lane4 = []

#import functions necessary:
def identify_carN_for(car): #returns carN for a given car
    if car.lane == 1:
        if len(lane2) > 0:
            for c2, car2 in enumerate(lane2):
                if car.pos > car2.pos:
                    carN = car2
                    break
                else:
                    carN = carEND
                    carN.lane = 2
        elif len(lane2) == 0:
            carN = carEND
            carN.lane = 2
    elif car.lane == 2:
        if len(lane1) > 0:
            for c1, car1 in enumerate(lane1):
                if car.pos > car1.pos:
                    carN = car1
                    break
                else:
                    carN = carEND
                    carN.lane = 1
        elif len(lane1) == 0:
            carN = carEND
            carN.lane = 1
    return carN

def identify_carO_for(car): #returns car O for given car
    if car.lane == 1:
        if len(lane1) > 0:
            for c1, car1 in enumerate(lane1):
                if car.pos > car1.pos:
                    carO = car1
                    break
                else:
                    carO = carEND
                    carO.lane = 1
        elif len(lane1) == 0:
            carO = carEND
            carO.lane = 1
    elif car.lane == 2:
        if len(lane2) > 0:
            for c2, car2 in enumerate(lane2):
                if car.pos > car2.pos:
                    carO = car2
                    break
                else:
                    carO = carEND
                    carO.lane = 2
        elif len(lane2) == 0:
            carO = carEND
            carO.lane = 2
    return carO

def identify_carlo_for(car):
    if car.lane == 1:
        if len(lane1_rev) > 0:
            for c1, car1 in enumerate(lane1_rev):
                if car1.pos > car.pos:
                    carlo = car1
                    break
                else:
                    carlo = carSTART
                    carlo.lane = 1
        elif len(lane1_rev) == 0:
            carlo = carSTART
            carlo.lane = 1
    elif car.lane == 2:
        if len(lane2_rev) > 0:
            for c2, car2 in enumerate(lane2_rev):
                if car2.pos > car.pos:
                    carlo = car2
                    break
                else:
                    carlo = carSTART
                    carlo.lane = 2
        elif len(lane2_rev) == 0:
            carlo = carSTART
            carlo.lane = 2
    return carlo

def identify_carln_for(car):
    if car.lane == 1:
        if len(lane2_rev) > 0:
            for c2, car2 in enumerate(lane2_rev):
                if car2.pos > car.pos:
                    carln = car2
                    break
                else:
                    carln = carSTART
                    carln.lane = 2
        elif len(lane2_rev) == 0:
            carln = carSTART
            carln.lane = 2
    elif car.lane == 2:
        if len(lane1_rev) > 0:
            for c1, car1 in enumerate(lane1_rev):
                if car1.pos > car.pos:
                    carln = car1
                    break
                else:
                    carln = carSTART
                    carln.lane = 1
        elif len(lane1_rev) == 0:
            carln = carSTART
            carln.lane = 1
    return carln

def del_v(leader,follower):
    return abs(leader.speed - follower.speed)

def del_s(leader,follower):
    return abs(leader.pos - follower.pos - leader.length)

def lane_change(car, a_th, politeness,carN,carO,carlo,carln): #safety criterion for car
    #calculate the 6 accelerations


    #calculating a_car:
    a_car = accel(car.speed, car.t_react, del_v(carlo, car), del_s(carlo, car), car.speed_des)
    a_tilde_car = accel(car.speed, car.t_react, del_v(carln, car), del_s(carln, car), car.speed_des)

    #calculating a_O
    a_O = accel(carO.speed, carO.t_react, del_v(car,carO),del_s(car,carO), carO.speed_des)
    a_tilde_O = accel(carO.speed, carO.t_react, del_v(carlo,carO), del_s(carlo,carO), carO.speed_des)

    #calculating a_N
    a_N = accel(carN.speed, carN.t_react, del_v(carln,carN),del_s(carln,carN),carN.speed_des)
    a_tilde_N = accel(carN.speed, carN.t_react, del_v(car,carN),del_s(car,carN),carN.speed_des)

    if car.lane == 1:
        if (a_tilde_N > -9) and ((a_tilde_car - a_car) + politeness*((a_tilde_N - a_N) + (a_tilde_O - a_O)) > a_th) and ((car.pos - carN.pos) >= car.length) and ((carln.pos - car.pos) >= carln.length):
            car.lane = 2
            return True
        else:
            car.lane = 1
            return False

    elif car.lane == 2:
        if (a_tilde_N > -9) and ((a_tilde_car - a_car) + politeness*((a_tilde_N - a_N) + (a_tilde_O - a_O)) > a_th) and ((car.pos - carN.pos) >= car.length) and ((carln.pos - car.pos) >= carln.length):
            car.lane = 1
            return True
        else:
            car.lane = 2
            return False
def sort_lanes(cars): # sorts cars by lane and then pos
    lane1.clear()
    lane2.clear()
    lane3.clear()
    lane4.clear()
    for car in cars:
        if car.lane == 1:
            lane1.append(car)
        elif car.lane == 2:
            lane2.append(car)
        elif car.lane == 3:
            lane3.append(car)
        elif car.lane == 4:
            lane4.append(car)

def car_accel(car,lane_change_criterion,carln,carlo):
    if lane_change_criterion == True:
        del_v4 = del_v(carln,car)
        del_s4 = del_s(carln,car)

        car.acceleration = accel(car.speed, car.t_react, del_v4, del_s4, car.speed_des)
        car.suvat()
        car.pos_update()
        car.draw()
    elif lane_change_criterion == False:
        del_v2 = del_v(carlo, car)
        del_s2 = del_s(carlo, car)
        car.acceleration = accel(car.speed, car.t_react, del_v2, del_s2, car.speed_des)
        car.suvat()
        car.pos_update()
        car.draw()
lane_carB = []
velocity_carB = []
acceleration_carB = []
position_carB = []
time =[]
carspos = cars

carspos = sorted(carspos, key=attrgetter('pos'), reverse = True)
sort_lanes(carspos)
for car in lane2:
    print(car.pos)
red = (255,0,0)
run = True
while run:
    #print('new frame')
    timer.tick(fps)
    screen.fill('darkgreen')
    road1.draw()
    font = pygame.font.SysFont('Arial', 20)
    speedometer = font.render(str(carB.speed), True, red)
    screen.blit(speedometer, (200 - speedometer.get_width(), 150 - speedometer.get_height()))
    carSTART = Car(1, 400, 50000000, 0.0001, 0, 5, 1, 'blue', 0.0001, 1.5, 3,10)
    carEND = Car(1, 400, 0, 0.0001, 0, 5, 1, 'pink', 0.0001, 1.5, 3,10)

    #data collection
    car_of_interest = car1
    lane_carB.append(car_of_interest.lane)
    velocity_carB.append(car_of_interest.speed)
    acceleration_carB.append(car_of_interest.acceleration)
    position_carB.append(car_of_interest.pos)

    carspos = sorted(carspos, key=attrgetter('pos'), reverse=True)
    sort_lanes(carspos)
    lane1_rev = lane1[::-1]
    lane2_rev = lane2[::-1]
    print(identify_carlo_for(carB).id)
    for index, car in enumerate(carspos):

        #if index < len(carspos):
        carspos = sorted(carspos, key=attrgetter('pos'), reverse=True)

        sort_lanes(carspos)
        lane1_rev = lane1[::-1]
        lane2_rev = lane2[::-1]
        carN = identify_carN_for(car)  # find new follower
        carO = identify_carO_for(car)  # find old follower
        carlo = identify_carlo_for(car)  # find old leader
        carln = identify_carln_for(car)  # find new leader
        lane_change_criterion = lane_change(car, car.thresh, car.politeness, carN, carO, carlo, carln)
        car_accel(car,lane_change_criterion,carln,carlo)
        carspos = sorted(carspos, key=attrgetter('pos'), reverse=True)
        sort_lanes(carspos)
        lane1_rev = lane1[::-1]
        lane2_rev = lane2[::-1]
        #sys.time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()


#graph plotting
#saving data
def time_tick(interval, frames):
    for i in range(frames):
        t = i * interval
        time.append(t)
    return time

T = time_tick(dt, len(position_carB))
X = velocity_carB
Y = acceleration_carB
Z = position_carB
L = lane_carB

np.save("datax.npy", X)
np.save("datay.npy", Y)
np.save("dataz.npy", Z)
np.save('datat.npy',T)
np.save('datal.npy', L)

np.savetxt('datax.txt', X, delimiter = ',' )
np.savetxt('datay.txt', Y, delimiter = ',' )
np.savetxt('dataz.txt', Z, delimiter = ',' )
np.savetxt('datat.txt', T, delimiter = ',' )
np.savetxt('datal.txt', L, delimiter = ',' )






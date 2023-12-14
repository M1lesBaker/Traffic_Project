import numpy as np
import matplotlib.pyplot as plt
import pygame
from operator import attrgetter

#pygame stuff
pygame.init()
WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()

#lists required
generation_times = []
lane1 = []
lane2 = []
lane3 = []
lane4 = []



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
                                                 [(self.start + 21, self.pos), (self.start + 21+ 15, self.pos),
                                                  (self.start +21 + 15, self.pos - self.length),
                                                  (self.start +21, self.pos - self.length)])
        elif self.lane == 3:
            self.rectangle = pygame.draw.polygon(screen, self.colour,
                                                 [(self.start + 21 + 21 + 3, self.pos), (self.start + 21 + 21 + 15 + 3, self.pos),
                                                  (self.start + 21 + 21 + 3 + 15, self.pos - self.length),
                                                  (self.start + 21 + 21 + 3, self.pos - self.length)])
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



carB = Car(1,400,100,20 , 0, 16.5, 0.1, 'red', 30, 1.5, 0.5,2)
carBLOCK1 = Car(1,400,1000,0.1 , 0, 500, 0, 'red', 0.11, 1.5, 100,3)
#carBLOCK2 = Car(2,400,1000,0.1 , 0, 250, 0, 'red', 0.11, 1.5, 100,3)
cars = [carB, carBLOCK1]#,carBLOCK2]
road1 = Road(3, 21, 397)

#car generator - generates one car and appends onto the end of cars

def car_generate(cars): #generates a sinlge car and appends the new car to the list called cars
    # length
    lengths = [4.4, 5.2, 12, 16.5] #car, van, rigid hgv, articulated hgv
    length_weights = [0.600601991, 0.243111831, 0.069460523, 0.086825654] #probability of these vehicles bein generated
    length = np.random.choice(lengths, p = length_weights)

    #politeness
    mean_politeness = 0.2
    std_politeness = 0.05
    min_politeness = 0.05
    max_politeness = 0.3
    politeness = np.random.normal(mean_politeness,std_politeness)
    if politeness > max_politeness:
        politeness = max_politeness
    elif politeness < min_politeness:
        politeness = min_politeness

    #speed - SOURCE AVERAGE TRAFFIC SPEEDS GOV
    #car - ~normally distributed
    std_speed_des_car = 3.76
    max_speed_des_car = 40.23
    min_speed_des_car = 20.12
    mean_speed_des_car = 30.39

    #van - ~normally distributed
    std_speed_des_van = 3.89
    max_speed_des_van = 40.23
    min_speed_des_van = 20.12
    mean_speed_des_van = 30.99

    #rigid hgv - ~half-normal distribution - to fix to make continuous in future update
    rigid_speeds = [20.11622709, 23.4689316, 25.70406795, 27.93920429, 30.17434063, 32.40947698, 34.64461332, 37.99731784]
    rigid_weights = [0.05, 0.2, 0.27, 0.16, 0.17, 0.1, 0.035, 0.015]
    max_speed_des_rigid = 37.99
    min_speed_des_rigid = 20.12

    #articulated hgv - ~half-normal distribution - to fix to make continuous in future update
    arctic_speeds = [20.11622709, 23.4689316, 25.70406795, 27.93920429]
    arctic_weights = [0.07, 0.465, 0.455, 0.01]
    max_speed_des_arctic = 27.94
    min_speed_des_arctic = 20.12

    if length == 4.4: #i.e if car
        speed = np.random.normal(mean_speed_des_car, std_speed_des_car)
        if speed > max_speed_des_car:
           speed = max_speed_des_car
        elif speed < min_speed_des_car:
           speed = min_speed_des_car
    elif length == 5.2: #i.e if van
        speed = np.random.normal(mean_speed_des_van, std_speed_des_van)
        if speed > max_speed_des_van:
            speed = max_speed_des_van
        elif speed < min_speed_des_van:
            speed = min_speed_des_van
    elif length == 12: #i.e if rigid hgv
        speed = np.random.choice(rigid_speeds, p = rigid_weights)
        if speed > max_speed_des_rigid:
            speed = max_speed_des_rigid
        elif speed < min_speed_des_rigid:
            speed = min_speed_des_rigid

    elif length == 16.5: #i.e if articulated hgv
        speed = np.random.choice(arctic_speeds, p=arctic_weights)
        if speed > max_speed_des_arctic:
            speed = max_speed_des_arctic
        elif speed < min_speed_des_arctic:
            speed = min_speed_des_arctic

    #t_react
    mean_t_react = 1.2
    max_t_react = 1.7
    min_t_react = 0.5
    std_t_react = 0.3
    t_react = np.random.normal(mean_t_react,std_t_react)
    if t_react > max_t_react:
        t_react = max_t_react
    elif t_react < min_t_react:
        t_react = min_t_react

    #colours
    colours = ['rosybrown', 'firebrick', 'red', 'salmon', 'chocolate','peru','darkorange','gold','orange','olivedrab','darkolivegreen','lime','green','forestgreen','turquoise','teal','dodgerblue','cadetblue','blueviolet','purple','blue','crimson','royalblue']
    colour = np.random.choice(colours)

    #lane-changing threshold - guessing it is normally distrubted need to do more research on this
    mean_thresh = 0.1
    std_thresh = 0.05
    min_thresh = 0.01
    max_thresh = 0.2
    threshold = np.random.normal(mean_thresh,std_thresh)
    if threshold > max_thresh:
        threshold = max_thresh
    elif threshold < min_thresh:
        threshold = min_thresh

    #lane
    lanes = [1,2,3]
    lane = np.random.choice(lanes)



    #car number
    car_number = len(cars) + 1

    # make car
    globals()['car' + str(car_number)] = Car(lane, 400, 1, speed, 0, length, politeness, colour, speed, t_react, threshold, car_number)
    cars.append(globals()['car' + str(car_number)])

#identify functions
def identify_carFO_for(car):  #identifys the old follower of a car
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

    elif car.lane == 3:
        if len(lane3) > 0:
            for c3, car3 in enumerate(lane3):
                if car.pos > car3.pos:
                    carO = car3
                    break
                else:
                    carO = carEND
                    carO.lane = 3
        elif len(lane3) == 0:
            carO = carEND
            carO.lane = 3

    elif car.lane == 4:
        if len(lane4) > 0:
            for c4, car4 in enumerate(lane4):
                if car.pos > car4.pos:
                    carO = car4
                    break
                else:
                    carO = carEND
                    carO.lane = 4
        elif len(lane4) == 0:
            carO = carEND
            carO.lane = 4
    return carO
def identify_carLO_for(car): #identifys the old leader of a car
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

    elif car.lane == 3:
        if len(lane3_rev) > 0:
            for c3, car3 in enumerate(lane3_rev):
                if car3.pos > car.pos:
                    carlo = car3
                    break
                else:
                    carlo = carSTART
                    carlo.lane = 3
        elif len(lane3_rev) == 0:
            carlo = carSTART
            carlo.lane = 3

    elif car.lane == 4:
        if len(lane4_rev) > 0:
            for c4, car4 in enumerate(lane4_rev):
                if car4.pos > car.pos:
                    carlo = car4
                    break
                else:
                    carlo = carSTART
                    carlo.lane = 4
        elif len(lane4_rev) == 0:
            carlo = carSTART
            carlo.lane = 4
    return carlo


def identify_carNFL_for(car): #identifys new left lane follower (only works for cars in lane 2 and 3)
    if car.lane == 2:
        if len(lane1) > 0:
            for c1, car1 in enumerate(lane1):
                if car.pos > car1.pos:
                    carNFL = car1
                    break
                else:
                    carNFL = carEND
                    carNFL.lane = 1
        elif len(lane1) == 0:
            carNFL = carEND
            carNFL.lane = 1
    elif car.lane == 3:
        if len(lane2) > 0:
            for c2, car2 in enumerate(lane2):
                if car.pos > car2.pos:
                    carNFL = car2
                    break
                else:
                    carNFL = carEND
                    carNFL.lane = 2
        elif len(lane2) == 0:
            carNFL = carEND
            carNFL.lane = 2
    return carNFL

def identify_carNFR_for(car): #identifys new follower right lane (only works for cars in lanes 1 and 2)
    if car.lane == 1:
        if len(lane2) > 0:
            for c2, car2 in enumerate(lane2):
                if car.pos > car2.pos:
                    carNFR = car2
                    break
                else:
                    carNFR = carEND
                    carNFR.lane = 2
        elif len(lane2) == 0:
            carNFR = carEND
            carNFR.lane = 2
    elif car.lane == 2:
        if len(lane3) > 0:
            for c3, car3 in enumerate(lane3):
                if car.pos > car3.pos:
                    carNFR = car3
                    break
                else:
                    carNFR = carEND
                    carNFR.lane = 3
        elif len(lane3) == 0:
            carNFR = carEND
            carNFR.lane = 3
    return carNFR

def identify_carNLL_for(car): #identifys new leader in left lane (only works for lanes 2 and 3)
    if car.lane == 2:
        if len(lane1_rev) > 0:
            for c1, car1 in enumerate(lane1_rev):
                if car1.pos > car.pos:
                    carNLL = car1
                    break
                else:
                    carNLL = carSTART
                    carNLL.lane = 1
        elif len(lane1_rev) == 0:
            carNLL = carSTART
            carNLL.lane = 1
    elif car.lane == 3:
        if len(lane2_rev) > 0:
            for c2, car2 in enumerate(lane2_rev):
                if car2.pos > car.pos:
                    carNLL = car2
                    break
                else:
                    carNLL = carSTART
                    carNLL.lane = 2
        elif len(lane1_rev) == 0:
            carNLL = carSTART
            carNLL.lane = 2
    return carNLL

def identify_carNLR_for(car): #identifys new leader in right lane (only works for lane 1 and 2)
    if car.lane == 1:
        if len(lane2_rev) > 0:
            for c2, car2 in enumerate(lane2_rev):
                if car2.pos > car.pos:
                    carNLR = car2
                    break
                else:
                    carNLR = carSTART
                    carNLR.lane = 2
        elif len(lane2_rev) == 0:
            carNLR = carSTART
            carNLR.lane = 2
    elif car.lane == 2:
        if len(lane3_rev) > 0:
            for c3, car3 in enumerate(lane3_rev):
                if car3.pos > car.pos:
                    carNLR = car3
                    break
                else:
                    carNLR = carSTART
                    carNLR.lane = 3
        elif len(lane3_rev) == 0:
            carNLR = carSTART
            carNLR.lane = 3
    return carNLR
def del_v(leader,follower):
    return abs(leader.speed - follower.speed)

def del_s(leader,follower):
    return abs(leader.pos - follower.pos - leader.length)

def lane_change(car, a_th, politeness): #identifys the necessary followers and leaders, calculates the necessary MOBIL accelerations and then works out what lane to draw the vehicle in
    #calculate the 6 accelerations
    if car.lane == 1:
        carNLR = identify_carNLR_for(car)
        carFO = identify_carFO_for(car)
        carLO = identify_carLO_for(car)
        carNFR = identify_carNFR_for(car)

        a_car = accel(car.speed, car.t_react, del_v(carLO, car), del_s(carLO, car), car.speed_des)
        a_tilde_car = accel(car.speed, car.t_react, del_v(carNLR, car), del_s(carNLR, car), car.speed_des)

        # calculating a_O
        a_O = accel(carFO.speed, carFO.t_react, del_v(car, carFO), del_s(car, carFO), carFO.speed_des)
        a_tilde_O = accel(carFO.speed, carFO.t_react, del_v(carLO, carFO), del_s(carLO, carFO), carFO.speed_des)

        # calculating a_N
        a_N = accel(carNFR.speed, carNFR.t_react, del_v(carNLR, carNFR), del_s(carNLR, carNFR), carNFR.speed_des)
        a_tilde_N = accel(carNFR.speed, carNFR.t_react, del_v(car, carNFR), del_s(car, carNFR), carNFR.speed_des)
        if (a_tilde_N > -9) and ((a_tilde_car - a_car) + politeness*((a_tilde_N - a_N) + (a_tilde_O - a_O)) > a_th) and ((car.pos - carNFR.pos) >= car.length) and ((carNLR.pos - car.pos) >= carNLR.length):
            car.lane = 2
            car.acceleration = accel(car.speed, car.t_react, del_v(carNLR, car), del_s(carNLR,car), car.speed_des)
            car.suvat()
            car.pos_update()
            car.draw()
            return True
        else:
            car.lane = 1
            car.acceleration = accel(car.speed, car.t_react, del_v(carLO, car), del_s(carLO, car), car.speed_des)
            car.suvat()
            car.pos_update()
            car.draw()
            return False

    elif car.lane == 2:
        carNLR = identify_carNLR_for(car)
        carFO = identify_carFO_for(car)
        carLO = identify_carLO_for(car)
        carNFR = identify_carNFR_for(car)
        carNFL = identify_carNFL_for(car)
        carNLL = identify_carNLL_for(car)

        # calculating a_O
        a_O = accel(carFO.speed, carFO.t_react, del_v(car, carFO), del_s(car, carFO), carFO.speed_des)
        a_tilde_O = accel(carFO.speed, carFO.t_react, del_v(carLO, carFO), del_s(carLO, carFO), carFO.speed_des)
        a_car = accel(car.speed, car.t_react, del_v(carLO, car), del_s(carLO, car), car.speed_des)

        #LEFT
        a_tilde_car_LEFT = accel(car.speed, car.t_react, del_v(carNLL, car), del_s(carNLL, car), car.speed_des)
        a_N_LEFT = accel(carNFL.speed, carNFL.t_react, del_v(carNLL, carNFL), del_s(carNLL, carNFL), carNFL.speed_des)
        a_tilde_N_LEFT = accel(carNFL.speed, carNFL.t_react, del_v(car, carNFL), del_s(car, carNFL), carNFL.speed_des)

        #RIGHT
        a_tilde_car_RIGHT = accel(car.speed, car.t_react, del_v(carNLR, car), del_s(carNLR, car), car.speed_des)
        a_N_RIGHT = accel(carNFR.speed, carNFR.t_react, del_v(carNLR, carNFR), del_s(carNLR, carNFR), carNFR.speed_des)
        a_tilde_N_RIGHT = accel(carNFR.speed, carNFR.t_react, del_v(car, carNFR), del_s(car, carNFR), carNFR.speed_des)

        RIGHT = ((a_tilde_car_RIGHT - a_car) + politeness*((a_tilde_N_RIGHT - a_N_RIGHT) + (a_tilde_O - a_O))) #right bias
        LEFT = ((a_tilde_car_LEFT - a_car) + politeness*((a_tilde_N_LEFT - a_N_LEFT) + (a_tilde_O - a_O))) #left bias
        if RIGHT > LEFT:
            if (a_tilde_N_RIGHT > -9) and (RIGHT > a_th) and ((car.pos - carNFR.pos) >= car.length) and ((carNLR.pos - car.pos) >= carNLR.length):
                car.lane = 3
                car.acceleration = accel(car.speed, car.t_react, del_v(carNLR, car), del_s(carNLR, car), car.speed_des)
                car.suvat()
                car.pos_update()
                car.draw()
                return True
            else:
                car.lane = 2
                car.acceleration = accel(car.speed, car.t_react, del_v(carLO, car), del_s(carLO, car), car.speed_des)
                car.suvat()
                car.pos_update()
                car.draw()
                return False
        elif LEFT > RIGHT:
            if (a_tilde_N_LEFT > -9) and (LEFT > a_th) and ((car.pos - carNFL.pos) >= car.length) and ((carNLL.pos - car.pos) >= carNLL.length):
                car.lane = 1
                car.acceleration = accel(car.speed, car.t_react, del_v(carNLL, car), del_s(carNLL, car), car.speed_des)
                car.suvat()
                car.pos_update()
                car.draw()
                return True
            else:
                car.lane = 2
                car.acceleration = accel(car.speed, car.t_react, del_v(carLO, car), del_s(carLO, car), car.speed_des)
                car.suvat()
                car.pos_update()
                car.draw()
                return False
    elif car.lane == 3:
        carNLL = identify_carNLL_for(car)
        carFO = identify_carFO_for(car)
        carLO = identify_carLO_for(car)
        carNFL = identify_carNFL_for(car)

        a_car = accel(car.speed, car.t_react, del_v(carLO, car), del_s(carLO, car), car.speed_des)
        a_tilde_car = accel(car.speed, car.t_react, del_v(carNLL, car), del_s(carNLL, car), car.speed_des)

        # calculating a_O
        a_O = accel(carFO.speed, carFO.t_react, del_v(car, carFO), del_s(car, carFO), carFO.speed_des)
        a_tilde_O = accel(carFO.speed, carFO.t_react, del_v(carLO, carFO), del_s(carLO, carFO), carFO.speed_des)

        # calculating a_N
        a_N = accel(carNFL.speed, carNFL.t_react, del_v(carNLL, carNFL), del_s(carNLL, carNFL), carNFL.speed_des)
        a_tilde_N = accel(carNFL.speed, carNFL.t_react, del_v(car, carNFL), del_s(car, carNFL), carNFL.speed_des)

        if (a_tilde_N > -9) and ((a_tilde_car - a_car) + politeness * ((a_tilde_N - a_N) + (a_tilde_O - a_O)) > a_th) and ((car.pos - carNFL.pos) >= car.length) and ((carNLL.pos - car.pos) >= carNLL.length):
            car.lane = 2
            car.acceleration = accel(car.speed, car.t_react, del_v(carNLL, car), del_s(carNLL, car), car.speed_des)
            car.suvat()
            car.pos_update()
            car.draw()
            return True
        else:
            car.lane = 3
            car.acceleration = accel(car.speed, car.t_react, del_v(carLO, car), del_s(carLO, car), car.speed_des)
            car.suvat()
            car.pos_update()
            car.draw()
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

def display_information(variable_name, dynamic_value, unit, information_number): #a useful function that can display real time date on the screen
    font = pygame.font.SysFont('Arial', 20)
    speedometer = font.render(str(variable_name) + str(dynamic_value) + str(unit), True, 'white')
    screen.blit(speedometer, (50, 100 + information_number*50 - speedometer.get_height()))


def average_speed(cars):
    speed_cars = []#
    for car in cars:
        speed_cars.append(car.speed)
    if len(cars) == 0:
        return ("N/A")
    else:
        return round(sum(speed_cars)/len(cars),1)



# simulation variables same for all cars
min_distance = 5 #pixels
smoothness = 2 #acceleration exponent (might move to variable soon)
accel_max = 2 #pixels/second^2 Comfortable accleration
decel_max = 3 #pixels/second^2 Comfortable deceleration
dt = 0.01111111111112
car_generation_rate = 0.2 #car/second MAX 1 car/second
fps = 90

#pre-loop start list creation
lane_carB = []
velocity_carB = []
acceleration_carB = []
position_carB = []
carspos = cars
carspos = sorted(carspos, key=attrgetter('pos'), reverse = True)
sort_lanes(carspos)
time = []
frame_counter = 0
for i in range(1,120,1):
    generation_times.append(int(i/car_generation_rate))

#begin main while loop - runs until the red X is clicked in pygame
run = True
while run:
    timer.tick(fps)
    screen.fill('darkgreen')
    road1.draw()

    #time
    frame_counter += 1
    current_time = frame_counter/fps
    time.append(current_time)
    #print(current_time)
    for i in generation_times:
        if i == (current_time):
            car_generate(carspos)

    display_information('Average Speed:  ', average_speed(carspos), ' m/s', 1)
    display_information('Average Speed Lane 1:  ', average_speed(lane1), ' m/s', 2)
    display_information('Average Speed Lane 2:  ', average_speed(lane2), ' m/s', 3)
    display_information('Average Speed Lane 3:  ', average_speed(lane3), ' m/s', 4)

    carSTART = Car(1, 400, 50000000, 0.0001, 0, 5, 1, 'blue', 0.0001, 1.5, 3,10)
    carEND = Car(1, 400, 0, 0.0001, 0, 5, 1, 'pink', 0.0001, 1.5, 3,10)

    #data collection
    car_of_interest = carB
    lane_carB.append(car_of_interest.lane)
    velocity_carB.append(car_of_interest.speed)
    acceleration_carB.append(car_of_interest.acceleration)
    position_carB.append(car_of_interest.pos)

    carspos = sorted(carspos, key=attrgetter('pos'), reverse=True)
    sort_lanes(carspos)



    for index, car in enumerate(carspos): #cycles through all cars on road

        #sorting before
        carspos = sorted(carspos, key=attrgetter('pos'), reverse=True)
        sort_lanes(carspos)
        lane1_rev = lane1[::-1]
        lane2_rev = lane2[::-1]
        lane3_rev = lane3[::-1]
        #lane4_rev = lane4[::-1]

        lane_change_criterion = lane_change(car, car.thresh, car.politeness)

        #sorting after
        carspos = sorted(carspos, key=attrgetter('pos'), reverse=True)
        sort_lanes(carspos)
        lane1_rev = lane1[::-1]
        lane2_rev = lane2[::-1]
        lane3_rev = lane3[::-1]
        #lane4_rev = lane4[::-1]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()


#graph plotting
#saving data
def time_tick(interval, frames): #not necessary anymore now time can be collected from current_time
    for i in range(frames):
        t = i * interval
        time.append(t)
    return time

T = time#_tick(dt, len(position_carB))
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






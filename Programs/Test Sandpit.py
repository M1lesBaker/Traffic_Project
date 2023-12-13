import numpy as np

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
def car_generate(cars):

    #politeness
    mean_politeness = 0.5
    std_politeness = 0.35
    min_politeness = 0.05
    max_politeness = 1
    politeness = np.random.normal(mean_politeness,std_politeness)
    if politeness > max_politeness:
        politeness = max_politeness
    elif politeness < min_politeness:
        politeness = min_politeness

    #speed
    std_speed_des = 5
    max_speed_des = 40
    min_speed_des = 20
    mean_speed_des = 25
    speed = np.random.normal(mean_speed_des, std_speed_des)
    if speed > max_speed_des:
        speed = max_speed_des
    elif speed < min_speed_des:
        speed = min_speed_des

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
    colours = ['rosybrown', 'firebrick', 'red', 'salmon', 'chocolate','peru','darkorange','gold','orange','olivedrab','darkolivegreen','lime','green','forestgreen','turquoise','teal','dodgerblue','cadetblue','blueviolet','purple','blue','crimson','royalblue','rebeccapurple']
    colour = np.random.choice(colours)

    #lane-changing threshold
    mean_thresh = 0.1
    std_thresh = 0.05
    min_thresh = 0.01
    max_thresh = 0.5
    threshold = np.random.normal(mean_thresh,std_thresh)
    if threshold > max_thresh:
        threshold = max_thresh
    elif threshold < min_thresh:
        threshold = min_thresh

    #lane
    lanes = [1,2,3]
    lane = np.random.choice(lanes)

    #length
    lengths = [5,5,5,5,5,5,5,5,5,5,10,10,16.5,16.5,16.5]
    length = np.random.choice(lengths)

    #car number
    car_number = len(cars) + 1

    # make car
    globals()['car' + str(car_number)] = Car(lane, 400, 1, speed, 0, length, politeness, 'rebeccapurple', speed, t_react, threshold, car_number)
    cars.append(globals()['car' + str(car_number)])
cars = []
car_generate(cars)
car_generate(cars)
car_generate(cars)
car_generate(cars)
print(cars[3].colour)

print((cars))

car_generation_rate = 0.33333 #car/second

generation_times = []
for i in range(1,120,1):
    generation_times.append(int(i/car_generation_rate))

print(generation_times)
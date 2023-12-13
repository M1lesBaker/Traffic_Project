import numpy as np
import matplotlib.pyplot as plt
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 60
timer = pygame.time.Clock()
#time = timer.get_time()
#simulation variables

time = []



#graph lists
position = []
velocity = []
time = []
#simulation classes
class Car:

    def __init__(self, lane, pos, speed, accel, length, mass, colour, id):
        self.lane = lane
        self.pos = pos
        self.speed = speed
        self.accel = accel
        self.length = length
        self.mass = mass
        self.colour = colour
        self.id = id

    def draw(self):
        self.rectangle = pygame.draw.polygon(screen, self.colour, [(400,self.pos),(415,self.pos),(415,self.pos+self.length),((400,self.pos+self.length))])

    def suvat(self):
        if self.speed < 31:
            self.speed += self.accel*0.016667

        else:
            self.speed = 31
        return self.speed

    def pos_update(self):
        self.pos += self.speed*0.016667 + 0.5*self.accel*(0.016667**2)

    def data_collect(self):
        position.append(self.pos)
        velocity.append(self.speed)

    #def speedometer(self):
    #    self.rectangle = pygame.draw.polygon(screen, 'black', [(50,50),(50,200),(200,200),(200,50)])
    #    self..render('Hello!', True, (255, 0, 0), (200, 100))




class Road:

    def __init__(self, lanes, lanewidth, x_pos):
        self.lanes = lanes
        self.lanewidth = lanewidth
        self.x_pos = x_pos

    def draw(self):
        self.rectangle = pygame.draw.polygon(screen, 'black', [(self.x_pos,0),(self.x_pos + (self.lanes*self.lanewidth),0),(self.x_pos + (self.lanes*self.lanewidth),HEIGHT),(self.x_pos, HEIGHT)])

    

car1 = Car(1,0, 17.8,2,50,1000,'red',1)
road1 = Road(3,20,397)

#simulation loop
run = True
while run:
    timer.tick(fps)
    screen.fill('darkgreen')
    road1.draw()
    car1.suvat()
    car1.pos_update()
    car1.draw()
    car1.data_collect()
    #car1.speedometer()
    print(car1.suvat())


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()

#Graph 1 (Outside Simulation Loop)
def time_tick(interval,frames):
    for i in range(frames):
        t = i*interval
        time.append(t)
    return time

def suvat_graph(time,velocity):
    plt.xlabel('Time ($s$)')
    plt.ylabel('Velocity ($v$)')
    plt.legend(loc = 'upper right')
    plt.plot(time,velocity)
    plt.plot()
    plt.show()


#time_tick(0.016666667, len(velocity))
suvat_graph(time_tick(0.016666667, len(velocity)),velocity)


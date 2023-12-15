# Modelling Motorway Traffic using Microscopic Techniques

## Introduction
This code was developed to implement both the intelligent driver model, IDM [1] and the model, minimizing.
overall braking induced by lane change (MOBIL) [2] to create a microscopic simulation of
traffic on multi-lane motorways. The simulation environment features stochastic vehicle
generation based on real life data from the UK Government to make it as realistic as possible
and the ability collect data from almost any metric related to the vehicles on the road making
it very versatile. In the future this environment will be used to investigate and evaluate
whether two parallel two lane motorways are better or worse for traffic flow than one four
lane motorway.

## How to View the Code
The GitHub contains all code used to make the simulation. This guide will explain what each program is and where to find them:

[1 Lane Simulation](https://github.com/M1lesBaker/Traffic_Project/blob/master/Programs/Early%20Days%20Work/1%20Lane%20Simulation/1%20Lane%20Simulation%20Finished.py): 
A simple 1 lane simulation using only IDM [1]. The cars are pregenerated as the stochastic car generator has not been added yet.

[2 Lane Simulation](https://github.com/M1lesBaker/Traffic_Project/blob/master/Programs/Multi-Lane%20Simulation/2%20Lane%20Version%202/Two%20Lane%20Simulation%20Finished.py): 
A more advanced 2 lane simulation which now uses MOBIL [2]. The are pregenerated as the stochastic car generator has not been added yet.

[3 Lane Simulation](https://github.com/M1lesBaker/Traffic_Project/blob/master/Programs/Multi-Lane%20Simulation/3%20Lane%20Version%201/Three%20Lane%20Simulation.py): 
Currently the most advanced simulation featuring 3 lanes. This simulation uses stochastic vehicle generation utilising data from the UK Government Department for Transport [3]

Each simulation has graphs that can be used to visualise the data exported from them. To do this the simulation code must be in the same folder as the graph code.


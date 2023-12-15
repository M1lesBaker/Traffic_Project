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

## Physics of the Code

If you are interested in the physical models implemented in this program please [click here](https://github.com/M1lesBaker/Traffic_Project/blob/master/Explanation%20of%20MOBIL%20and%20IDM.pdf) to view an explanation of how they work

## How to View the Code
The GitHub contains all code used to make the simulation. This guide will explain what each program is and where to find them:

[1 Lane Simulation](https://github.com/M1lesBaker/Traffic_Project/blob/master/Programs/Early%20Days%20Work/1%20Lane%20Simulation/1%20Lane%20Simulation%20Finished.py): 
A simple 1 lane simulation using only IDM [1]. The cars are pregenerated as the stochastic car generator has not been added yet.

[2 Lane Simulation](https://github.com/M1lesBaker/Traffic_Project/blob/master/Programs/Multi-Lane%20Simulation/2%20Lane%20Version%202/Two%20Lane%20Simulation%20Finished.py): 
A more advanced 2 lane simulation which now uses MOBIL [2]. The are pregenerated as the stochastic car generator has not been added yet.

[3 Lane Simulation](https://github.com/M1lesBaker/Traffic_Project/blob/master/Programs/Multi-Lane%20Simulation/3%20Lane%20Version%201/Three%20Lane%20Simulation.py): 
Currently the most advanced simulation featuring 3 lanes. This simulation uses stochastic vehicle generation utilising data from the UK Government Department for Transport [3]

Each simulation has graphs that can be used to visualise the data exported from them. To do this the simulation code must be in the same folder as the graph code.

## References

[1] Martin Treiber, Ansgar Hennecke, and Dirk Helbing. Congested traffic states in empirical observa-
tions and microscopic simulations. Phys. Rev. E, 62:1805–1824, Aug 2000

[2] Arne Kesting, Martin Treiber, and Dirk Helbing. General lane-changing model mobil for car-
following models. Transportation Research Record, 1999(1):86–94, 2007.

[3] Department for Transport 2023, *Department for Transport Website*, UK Government, accessed 5th November 2023, <https://www.gov.uk/government/statistics/vehicle-speed-compliance-statistics-for-great-britain-2022/vehicle-speed-compliance-statistics-for-great-britain-2022#exceeding-the-speed-limit-by-day-of-the-year>

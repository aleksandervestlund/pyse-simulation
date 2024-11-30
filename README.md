# TTM4110 - Smart City Bus Simulations

> By: Andreas Kolstad Bertelsen and Aleksander Thornes Vestlund.

## Requirements

- Python 3.10 or newer.
- The contents of `requirements.txt`.

## System Description

In a smart city you should expect a smart and flexible city transportation system (Intelligent Transportation System, ITS).
A modern, smart citizen focuses on the need for transportation-as-a-service (TaaS), and does not need to own a vehicle that occupies valuable area in the city (e.g., a private car is parked most of the time).
What we need is to get from A to B whenever we want, as convenient and fast as possible.

We are going to focus on a smarter bus system as one part of such a transportation system.
The bus routes are more flexible than they are today and adapts to the current needs for transportation (from, to, when, how many).
A passenger’s Quality of Experience (QoE) with such a smart bus service depends to a great extent on the travel time, but also other factors not directly linked to this.

The technical system that is used in this assignment consists of:

- $E_i$ - end bus stops, ($i = 1, \cdots , n_e, n_e = 4$),
- $S_{id}$ - intermediate bus stops eastbound $e$ and westbound $w$, ($i = 1, \cdots , n_s, n_s = 7, d = e, w$), and
- $R_i$ - bidirectional roads connecting the bus stops. ($i = 1, \cdots , n_r, n_r = 15$)

There is a finite number of busses, $n_b$, in the system that operates several alternative routes.
A bus has a finite capacity (maximum number of passengers allowed, $c$) and the travel time on a road $R_i$ is $t_i$.
The current number of passengers who want to travel from bus stop $S_{id}$ is denoted $P_{id}$.
A passenger on a bus will leave the bus at bus stop $S_{id}$ (bus stop $i$ going $d$-bound) along the route with a probability $q$ (for simplicity we assume that this probability is the same for all stops).
A bus route is described by two sets:

- $S_{i,j}$ - route between and end stops $E_i$ and $E_j$, with bus stops $S_{kd}$, $d = e$ if $i > j$ and $d = w$ otherwise.
- $R_{i,j}$ - route between and end stops $E_i$ and $E_j$, with the roads that connect the bus stops in $S_{i,j}$.

The next route for a bus that is ready for departure from any of the end bus stops, should include the bus stops with the current highest demand (e.g., current number of passengers $P_{id}$ who want to travel from bus stop $S_{id}$, longest waiting passengers, or largest queue of passengers).
To reduce the number of alternative routes, we assume that a bus can only travel between $E_i$, ($i = 1, 2$), and $E_j$, ($j = 3, 4$), and that every combination of $E_i$ and $E_j$ has only one route, i.e., this gives $2 \cdot 4$ combinations in total (unless you make the routes symmetric between $E_i$ and $E_j$).

The objective is to assess the city bus transportation service with respect to the utilization of the busses and the travel time (including the waiting time at the bus stop) for the passengers.
The parameters that should be used in the simulations are given for the travel time for each road, the passenger arrival rates to the bus stops, and the rest.
The passenger loading time (time for a passenger to enter the bus) is assumed to be negligible.
The total travel time for a passenger from he/she arrives at the bus stop until his/her end station is reached is, therefore, the time waiting for the bus and the travel time between bus stops.

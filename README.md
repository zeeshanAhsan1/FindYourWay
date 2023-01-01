# FindYourWay
A grid environment with walls where the exact location of drone has to be found without any prior information about the drone location.

## Environment and Drone
The drone is capable of moving from cell to cell within the reactor, working on and repairing internal mechanisms. However, while you can issue commands to the sub drone (Up, Down, Left, Right), due to the manner in which you gained access, you don’t have the ability to access the drone’s sensors - you can command it, but you can’t see where it is or get any feedback from it about its position. You are blind. But not helpless.

## Program to find exact location of drone after a set of allowed commands to the drone ( Left, Right, Up, Down ).
This is implemented in the droneLocation.py file. After a certain number of moves, we can exactly find the drone location using the probability distribution of drone being in each cell and modifying those probabilities after every command so as to get a final probability of 1 in a particular cell where we can say that the drone is certainly present.

## Program to create a new grid using the randomized Prim's Algorithm.
This is implemented in grid.py. This generates a text file with a new grid which has only 1 entry and only 1 exit in the grid. Here, all the cells are connected to each other by some path.

import numpy as np
import random

#Method to create a grid using Randomized Prim's Algorithm
def createGrid(rows,cols):
    #Initialize with all 1's denoting all walls 
    grid = np.ones((rows,cols),dtype=(int))
    visited_dict = {}
    print(grid[0][0])
    unvisited = []
    walls = []
        
    #Start with a random cell
    x_random = int(random.random()*rows)
    y_random = int(random.random()*cols)
    
    #Make the values of all cells 3 -> Denoting all cells are unvisited in the beginning
    for i in range(rows):
        for j in range(cols):
            grid[i][j] = 3
    
    #Make sure we don't start at the edge/boundary of the grid
    if x_random == 0:
        x_random += 1
    if x_random == rows-1:
        x_random -= 1
    if y_random == 0:
        y_random += 1
    if y_random == cols-1:
        y_random -= 1
    
    
    #Make this (x_random,y_random) as an open path
    grid[x_random][y_random] = 0
    #Add the surrounding cells to the walls list
    walls.append((x_random, y_random - 1))
    walls.append((x_random,y_random + 1))
    walls.append((x_random - 1, y_random))
    walls.append((x_random + 1, y_random))
    
    grid[x_random][y_random - 1] = 1
    grid[x_random][y_random + 1] = 1
    grid[x_random - 1][y_random] = 1
    grid[x_random + 1][y_random - 1] = 1
    
    while(walls):
        #Pick a randoim wall
        r_wall = walls[int(random.random()*len(walls))-1]
        
        # Check if it is a left wall
        if (r_wall[1] != 0):
            if (grid[r_wall[0]][r_wall[1]-1] == 3 and grid[r_wall[0]][r_wall[1]+1] == 0):
                # Find number of surrounding cells
                s_cells = surroundingCells(grid,r_wall)
                
                if (s_cells < 2):
                    # Denote the new path
                    grid[r_wall[0]][r_wall[1]] = 0
                    
                    # Mark the new walls
                    # Upper cell
                    if (r_wall[0] != 0):
                        if (grid[r_wall[0]-1][r_wall[1]] != 0):
                            grid[r_wall[0]-1][r_wall[1]] = 1
                        if ((r_wall[0]-1, r_wall[1]) not in walls):
                            walls.append((r_wall[0]-1, r_wall[1]))
                            
                    # Bottom cell
                    if (r_wall[0] != rows-1):
                        if (grid[r_wall[0]+1][r_wall[1]] != 0):
                            grid[r_wall[0]+1][r_wall[1]] = 1
                        if ((r_wall[0]+1, r_wall[1]) not in walls):
                            walls.append((r_wall[0]+1, r_wall[1]))
                            
                    # Leftmost cell
                    if (r_wall[1] != 0):
                        if (grid[r_wall[0]][r_wall[1]-1] != 0):
                            grid[r_wall[0]][r_wall[1]-1] = 1
                        if ((r_wall[0], r_wall[1]-1) not in walls):
                            walls.append((r_wall[0], r_wall[1]-1))
                
                # Delete wall
                for wall in walls:
                    if (wall[0] == r_wall[0] and wall[1] == r_wall[1]):
                        walls.remove(wall)
                    
                continue
            
        # Check if it is an upper wall
        if (r_wall[0] != 0):
            if (grid[r_wall[0]-1][r_wall[1]] == 3 and grid[r_wall[0]+1][r_wall[1]] == 0):
                
                #Find number of surrounding cells
                s_cells = surroundingCells(grid,r_wall)
                
                if (s_cells < 2):
                    # Denote the new path
                    grid[r_wall[0]][r_wall[1]] = 0
                    
                    #Mark new walls
                    # Upper cell
                    if (r_wall[0] != 0):
                        if (grid[r_wall[0]-1][r_wall[1]] != 0):
                            grid[r_wall[0]-1][r_wall[1]] = 1
                        if ((r_wall[0]-1, r_wall[1]) not in walls):
                            walls.append((r_wall[0]-1, r_wall[1]))
                        
                    # Leftmost cell
                    if (r_wall[1] != 0):
                        if (grid[r_wall[0]][r_wall[1]-1] != 0):
                            grid[r_wall[0]][r_wall[1]-1] = 1
                        if ((r_wall[0], r_wall[1]-1) not in walls):
                            walls.append((r_wall[0], r_wall[1]-1))
                        
                    # Rightmost cell
                    if (r_wall[1] != cols-1):
                        if (grid[r_wall[0]][r_wall[1]+1] != 0):
                            grid[r_wall[0]][r_wall[1]+1] = 1
                        if ((r_wall[0], r_wall[1]+1) not in walls):
                            walls.append((r_wall[0], r_wall[1]+1))
                        
                # Delete wall
                for wall in walls:
                    if (wall[0] == r_wall[0] and wall[1] == r_wall[1]):
                        walls.remove(wall)
                        
                continue

        # Check the bottom wall 
        if (r_wall[0] != rows-1):
            if (grid[r_wall[0]+1][r_wall[1]] == 3 and grid[r_wall[0]-1][r_wall[1]] == 0):
                
                s_cells = surroundingCells(grid,r_wall)
                if (s_cells < 2):
                    # Denote the new path
                    grid[r_wall[0]][r_wall[1]] = 0
                    
                    # Mark the new walls
                    if (r_wall[0] != cols-1):
                        if (grid[r_wall[0]+1][r_wall[1]] != 0):
                            grid[r_wall[0]+1][r_wall[1]] = 1
                        if ((r_wall[0]+1, r_wall[1]) not in walls):
                            walls.append((r_wall[0]+1, r_wall[1]))
                    
                    if (r_wall[1] != 0):
                        if (grid[r_wall[0]][r_wall[1]-1] != 0):
                            grid[r_wall[0]][r_wall[1]-1] = 1
                        if ((r_wall[0], r_wall[1]-1) not in walls):
                            walls.append((r_wall[0], r_wall[1]-1))
                        if (r_wall[1] != cols-1):
                            if (grid[r_wall[0]][r_wall[1]+1] != 0):
                                grid[r_wall[0]][r_wall[1]+1] = 1
                            if ((r_wall[0], r_wall[1]+1) not in walls):
                                walls.append((r_wall[0], r_wall[1]+1))
                    
                # Delete wall
                for wall in walls:
                    if (wall[0] == r_wall[0] and wall[1] == r_wall[1]):
                        walls.remove(wall)
                        
                continue                   
    
        # Check the right wall
        if (r_wall[1] != cols-1):
            if (grid[r_wall[0]][r_wall[1]+1] == 3 and grid[r_wall[0]][r_wall[1]-1] == 0):
                
                s_cells = surroundingCells(grid,r_wall)
                if (s_cells < 2):
                    # Denote the new path
                    grid[r_wall[0]][r_wall[1]] = 0
                    
                    # Mark the new walls
                    if (r_wall[1] != cols-1):
                        if (grid[r_wall[0]][r_wall[1]+1] != 0):
                            grid[r_wall[0]][r_wall[1]+1] = 1
                        if ((r_wall[0], r_wall[1]+1) not in walls):
                            walls.append((r_wall[0], r_wall[1]+1))
                        
                    if (r_wall[0] != rows-1):
                        if (grid[r_wall[0]+1][r_wall[1]] != 0):
                            grid[r_wall[0]+1][r_wall[1]] = 1
                        if ((r_wall[0]+1, r_wall[1]) not in walls):
                            walls.append((r_wall[0]+1, r_wall[1]))
                        
                    if (r_wall[0] != 0):
                        if (grid[r_wall[0]-1][r_wall[1]] != 0):
                            grid[r_wall[0]-1][r_wall[1]] = 1
                        if ((r_wall[0]-1, r_wall[1]) not in walls):
                            walls.append((r_wall[0]-1, r_wall[1]))
                            
                # Delete wall
                for wall in walls:
                    if (wall[0] == r_wall[0] and wall[1] == r_wall[1]):
                        walls.remove(wall)
                        
                continue
    
        
        # Delete the wall from the list
        for wall in walls:
            if (wall[0] == r_wall[0] and wall[1] == r_wall[1]):
                walls.remove(wall)
                
    # Mark the unvisited cells as walls
    for i in range(0, rows):
        for j in range(0, cols):
            if(grid[i][j] == 3):
                grid[i][j] = 1
    
    # Set start and end
    for i in range(0, cols):
        if (grid[1][i] == 0):
            grid[0][i] = 0
            break
    
    for i in range(cols - 1, 0, -1):
        if(grid[rows - 2][i] == 0):
            grid[rows-1][i] = 0
            break
    
    return grid
    

#Find the number of surrounding cells    
def surroundingCells(grid,r_wall):
    count = 0
    #If Up Cell is free
    if (grid[r_wall[0]-1][r_wall[1]] == 0):
        count += 1
    #If down cell is free
    if(grid[r_wall[0]+1][r_wall[1]] == 0):
        count +=1 
    #If left cell is free
    if (grid[r_wall[0]][r_wall[1]-1] == 0):
        count +=1
    #If right cell is free
    if (grid[r_wall[0]][r_wall[1]+1] == 0):
        count += 1
    
    return count
    

#Create the text file of grid from Grid Matrix
def create_file_from_grid(grid):
    
    with open('/Users/zeeshanahsan/Code/CS520Final_exam/ZeeGrid.txt', 'w') as f:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                #If wall then write 'X'
                if(grid[i][j] == 1):
                    f.write('X')
                #If free cell then write '_'
                elif(grid[i][j] == 0):
                    f.write('_')
            #Go to new line
            f.write('\n')
            
#Driver code
grid = createGrid(19,19)
print(grid)
create_file_from_grid(grid)
                    
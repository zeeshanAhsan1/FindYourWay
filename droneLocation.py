import numpy as np
import matplotlib.pyplot as plt

#method to read file and process input
def readFile_and_returnGrid():
    #Read text File
    with open("CS520Final_exam/question_grid.txt") as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
    
    no_of_rows = len(lines)
    no_of_cols = len(lines[0]) - 1
    
    print("No of rows : ", no_of_rows)
    print("No. of Cols :", no_of_cols)
    
    #Make a grid with 1's as walls and 0's as open cells
    grid = np.zeros((no_of_rows,no_of_cols),dtype=(int))
    #print(grid)
    for i in range(no_of_rows):
        for j in range(no_of_cols):
            #If character is 'X' -> it is a wall -> assign 1 to the matrix
            if(lines[i][j] == 'X'):
                grid[i][j] = 1
    
    #print(grid)
    return(grid)

#method to initialize the belief/probability matrix of agent for each cell in grid of the drone being there
def initialize_beliefMatrix(grid):
    
    no_of_rows = len(grid)
    no_of_cols = len(grid[0])
    
    #Belief Matrix to capture belief of containing drone in each cell
    beliefMatrix = np.zeros((no_of_rows,no_of_cols),dtype=(float))
    
    #Count number of open cells in the grid
    countCells = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if(grid[i][j] == 0):
                countCells += 1
    
    # Divide Belief equally for all open cells
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if(beliefMatrix[i][j] == 0):
                beliefMatrix[i][j] = 1/countCells
                
    #Set Belief of walls to be zero
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if(grid[i][j] == 1):
                beliefMatrix[i][j] = 0
    
    return beliefMatrix
    
#method to move left and do the corresponding probability updates
def moveLeft(grid,beliefMatrix):
    copy_of_beliefs = np.copy(beliefMatrix)
    rows = len(grid)
    cols = len(grid[0])
     
    #ITERATING ROW WISE       
    for i in range(rows):
        for j in range(cols):
            #belief(col1) = belief(col1) + belief(col2) if col1 is not wall 
            if(j == 0 and grid[i][j] != 1 and grid[i][j+1] != 1): 
                beliefMatrix[i][j] = copy_of_beliefs[i][j] + copy_of_beliefs[i][j+1]
            
            #General Case for no left wall or right wall
            if(j+1 <= cols-1 and j != 0 and grid[i][j] !=1 and grid[i][j+1] != 1 and grid[i][j-1] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j+1]
                           
            #When left cell is wall and right cell is no wall
            if(j+1 <= cols-1 and j != 0 and grid[i][j] !=1 and grid[i][j+1] != 1 and grid[i][j-1] == 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j] + copy_of_beliefs[i][j+1]
                
            #When there's a wall on the right side
            if(j+1 <= cols-1 and j != 0 and grid[i][j] !=1 and grid[i][j+1] == 1):
                beliefMatrix[i][j] = 0
        
            #Set Last Col as Zero if it is in the last column and doesn't have wall on the left
            if(j == (cols-1) and grid[i][j] != 1 and grid[i][j-1] != 1):
                beliefMatrix[i][j] = 0
            
            #If Left and Right both walls -> No change in belief
            if(j != 0 and j+1 <= cols - 1 and j-1 >=0 and grid[i][j] != 1 and grid[i][j-1] == 1 and grid[i][j+1] == 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j]  
                    
    #Return Updated Probability Matrix           
    return beliefMatrix

#method to move right and do the corresponding probability updates
def moveRight(grid,beliefMatrix):
    copy_of_beliefs = np.copy(beliefMatrix)
    rows = len(grid)
    cols = len(grid[0])
    
    #Iterating Row Wise
    for i in range(rows):
        for j in range(cols):
            #belief(col'n') = belief(col'n-1') + belief(col'n') and col'n' is not wall
            if(j == cols - 1 and grid[i][j] != 1 and grid[i][j-1] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j] + copy_of_beliefs[i][j-1]
            
            #General Case for no left or right wall
            if(j-1 >= 0 and j != cols -1 and grid[i][j] != 1 and grid[i][j+1] != 1 and grid[i][j-1] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j-1]
            
            #When right cell is wall and left cell is no wall
            if(j-1 >= 0 and j != cols -1 and grid[i][j] != 1 and grid[i][j+1] == 1 and grid[i][j-1] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j] + copy_of_beliefs[i][j-1]
            
            #When there's a wall on the left side
            if(j-1 >= 0 and j != cols -1 and grid[i][j] != 1 and grid[i][j-1] == 1):
                beliefMatrix[i][j] = 0
                
            #Set 1st Col as zero and doesn't have wall on the right
            if(j == 0 and grid[i][j] != 1 and grid[i][j+1] != 1):
                beliefMatrix[i][j] = 0
            
            #If Left and Right both walls -> No change in belief
            if(j != 0 and j+1 <= cols - 1 and j-1 >=0 and grid[i][j] != 1 and grid[i][j-1] == 1 and grid[i][j+1] == 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j] 
    
    #Return Updated Probability Matrix           
    return beliefMatrix
            
#method to move up and do the corresponding probability updates            
def moveUp(grid,beliefMatrix):
    copy_of_beliefs = np.copy(beliefMatrix)
    rows = len(grid)
    cols = len(grid[0])
    
    # Iterating Column wise
    for j in range(cols):
        for i in range(rows):
            #belief row1 = belief(row1) + belief(row2) if row is not wall
            if(i==0 and grid[i][j] != 1 and grid[i+1][j] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j] + copy_of_beliefs[i+1][j]
            
            #General case for no up wall or down wall
            if(i+1 <= rows - 1 and i != 0 and grid[i][j] != 1 and grid[i+1][j] != 1 and grid[i-1][j] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i+1][j]
            
            #When Cell Up is Wall and Cell Down is no wall
            if(i+1 <= rows - 1 and i != 0 and grid[i][j] != 1 and grid[i+1][j] != 1 and grid[i-1][j] == 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j] + copy_of_beliefs[i+1][j]
            
            #When there's a Wall Down
            if(i+1 <= rows-1 and i != 0 and grid[i][j] != 1 and grid[i+1][j] == 1):
                beliefMatrix[i][j] = 0
            
            #Set Last Row as Zero
            if(i == rows - 1 and grid[i][j] != 1 and grid[i-1][j] != 1):
                beliefMatrix[i][j] = 0
            
            #If Up and down both walls -> No change in belief
            if(i != 0 and i+1 <= rows - 1 and i-1 >=0 and grid[i][j] != 1 and grid[i+1][j] == 1 and grid[i-1][j] == 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j]
            
    #Return updated Probability Matrix
    return beliefMatrix
    
#method to move down and do the corresponding probability updates   
def moveDown(grid,beliefMatrix):
    copy_of_beliefs = np.copy(beliefMatrix)
    rows = len(grid)
    cols = len(grid[0])
    
    #Iterating column wise
    for j in range(cols):
        for i in range(rows):
            #belief row'n' = belief(row'n') + belief(row'n-1') if row is not wall
            if(i== rows -1 and grid[i][j] != 1 and grid[i-1][j] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j] + copy_of_beliefs[i-1][j]
            
            #General case for no up wall or down wall
            if(i+1 <= rows - 1 and i != 0 and grid[i][j] != 1 and grid[i+1][j] != 1 and grid[i-1][j] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i-1][j]
            
            #When Cell Down is Wall and Cell Up is no wall
            if(i+1 <= rows - 1 and i != 0 and grid[i][j] != 1 and grid[i+1][j] == 1 and grid[i-1][j] != 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j] + copy_of_beliefs[i-1][j]
            
            #When there's a Wall Up
            if(i-1 >= 0 and i != rows - 1 and grid[i][j] != 1 and grid[i-1][j] == 1):
                beliefMatrix[i][j] = 0
            
            #Set First Row as Zero
            if(i == 0 and grid[i][j] != 1 and grid[i+1][j] != 1):
                beliefMatrix[i][j] = 0
            
            #If Up and down both walls -> No change in belief
            if(i != 0 and i+1 <= rows - 1 and i-1 >=0 and grid[i][j] != 1 and grid[i+1][j] == 1 and grid[i-1][j] == 1):
                beliefMatrix[i][j] = copy_of_beliefs[i][j]
    
    #Return Updated Belief Matrix
    return beliefMatrix
   
#method to build the reverse path from dijkstra dictionary      
def buildPath(revPath,start,end):
    path = {}   # Empty path dictionary
    # end = (50,50)

    x,y = end[0],end[1]

    while ((x,y) != (start[0],start[1])):   # Traverse the dictionary till we reach the start cell from goal cell
        path[revPath[(x,y)]] = (x,y)    #   Make the path dict with key as Reverse path Value for that key
        (x,y) = revPath[(x,y)]      # Update the co-ordinates

    return path     # Return the path dictionary    

#Dijkstra search on the grid from start cell to end cell 
def djikstra(grid,start,end):

    n_rows = len(grid)
    n_cols = len(grid[0])
    unvisited = {}
    curCell = start
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            unvisited[(i,j)] = float('inf') #Instantiate the unvisted dictionary for all keys to infinity cost
    
    unvisited[start] = 0    # Set the start cell as zero cost
    visited = {}    # Make an empty visited dictionary
    revPath = {}    # Make an empty reverse path Dictionary

    curCell = min(unvisited, key=unvisited.get) # Assign the current cell as the lowest cost cell frem the dictionary of unvisited cells
    #print(curCell)

    while unvisited:    # Traverse till unvisited dictionary gets empty
        curCell = min(unvisited, key=unvisited.get) # Assign the current cell as the lowest cost cell frem the dictionary of unvisited cells
        x,y = curCell[0],curCell[1] # Take the x and y cio-ordinates of the current cell
        visited[curCell] = unvisited[curCell] # Add the Value of Unvisited dictionary for current cell to the corresponding key in visited dictionary
        if(curCell == end): # If we reach goal cell
            if(end in revPath.keys()):  # If goal is in keys of the reverse path dictionary
                path = buildPath(revPath,start,end) # Then build a path
                pathList = []   # Make an empty path 
                for key,val in path.items():
                    pathList.append(val)    # Make an array of cells which only contain reverse path
                return (pathList)
            else:
                return(-2)
         
            
        #Check Neighbors of the current Cell
        neighborList = []
        if(y+1 <= n_cols - 1 and grid[x][y+1] !=1 ): #Rneighbor
            neighbor = (x,y+1)
            neighborList.append(neighbor)
            #print("curCell :" ,neighbor)
        if(y-1 >= 0 and grid[x][y-1] !=1): #Lneigh
            neighbor = (x,y-1)
            neighborList.append(neighbor)
            #print("curCell :" ,neighbor)
        if(x+1 <= n_rows - 1 and grid[x+1][y] !=1): #DNeigh
            neighbor = (x+1,y)
            neighborList.append(neighbor)
            #print("curCell :" ,neighbor)
        if(x-1 >= 0 and grid[x-1][y] != 1): #UNeigh
            neighbor = (x-1,y)
            neighborList.append(neighbor)
            #print("curCell :" ,neighbor)


        #Check if Neighbor is already present in visited dict
        for nbr in neighborList:
            if(nbr in visited): # For each valid neighbor if it ios already visited then do nothing and continue to the next neighbor
                continue    
            tempDist = unvisited[curCell] + 1   
            if(tempDist < unvisited[nbr]):
                unvisited[nbr] = tempDist   # Update the distance of neighbor cell if the current distance is less than previous distance in the dictionary for this cell
                revPath[nbr] = curCell  # Set the reverse path key of neighbor cell to current cell value

        unvisited.pop(curCell)  # Remove the current cell from visited cell dictionary

#method for generating the actions to move on the shortest distance path
def shortestDistance_ActionsList(grid,beliefMatrix,start,end):
    # Reverse Path List of the path of cells using dijkstra algorithm from start to end
    pathList = djikstra(grid, start, end)
    # Appending the start cell to the list
    pathList.append(start)
    # Reversing the reverse Path to get a forward path from start to end
    pathList.reverse()
    # Build the executable actions list
    actionList = []
    for i in range(len(pathList) - 1):
        #Extract the current cell from path list
        curCell = pathList[i]
        #Extract the x & y co-ordinates of the cell
        x_curCell,y_curCell = curCell[0],curCell[1]
        #Extract the next cell in the path list
        nextCell = pathList[i+1]
        #Extract the x & y co-ordinates of the next cell in the path list
        x_nextCell,y_nextCell = nextCell[0],nextCell[1]
        
        # Formulate moves required to go from one cell to the next cell
        
        #Same Row, Diff Col -> Left or Right
        if(x_curCell == x_nextCell):
            #Move Right
            if(y_curCell + 1 == y_nextCell):
                actionList.append("right")
            #Move Left
            elif(y_curCell - 1 == y_nextCell):
                actionList.append("left")
        
        #Same Col, Diff Row -> Up or Down
        elif(y_curCell == y_nextCell):
            #Move Down
            if(x_curCell + 1== x_nextCell):
                actionList.append("down")
            #Move Up
            elif(x_curCell - 1 == x_nextCell):
                actionList.append("up")
    #Return the list of actions required to move from start to end
    return actionList

#Method to find 2 nearest cells with non-zero probabilities row-wise    
def find_2_Cells(grid,beliefMatrix):
    rows = len(grid)
    cols = len(grid[0])
    cells_list = []
    count = 0
    #iterate through the belief matrix row-wise
    for i in range(rows):
        for j in range(cols):
            # If there are 2 cells in the cells_list break and return
            if(count == 2):
                break
            #Find the non-zero entries in the matrix and append their locations to the cells_list
            if(beliefMatrix[i][j] != 0):
                cells_list.append((i,j))
                count +=1
    
    #Return the cells_list with locations(x,y) of the 2 non-zero values in the beliefMatrix    
    return cells_list

#Methodn to solve the problem in lowest number of steps        
def solve_shortest(grid, beliefMatrix):
    rows = len(grid)
    cols = len(grid[0])
    #List containing the final moves
    movesList = []
    flag = 0
    while(True):
        #Find 2 nearest cells from top with non-zero probability
        cells_list = find_2_Cells(grid, beliefMatrix)
        #If only 1 non-zero cell left in beliefMatrix -> Drone found
        if(len(cells_list) == 1):
            flag = 1
        # Print Results
        if(flag == 1):
            print()
            print("Moves : ")
            print(movesList)
            print()
            print("BELIEF MATRIX : ")
            print()
            print(beliefMatrix)
            print("Drone Position with 100% Certainity : ", cells_list[0])
            print("Number of Moves Taken : ", len(movesList))
            # plt.imshow(beliefMatrix, cmap = 'Blues')
            # plt.show()
            break
        cell1 = cells_list[0]
        cell2 = cells_list[1]
        print("Cell 1: ", cell1)
        print("Cell 2: ", cell2)
        #Build Action List
        actionList = shortestDistance_ActionsList(grid, beliefMatrix, cell1, cell2)
        #Execute the actions built
        for i in range(len(actionList)):
            #If action is down -> Execute down move
            if(actionList[i] == "down"):
                beliefMatrix = moveDown(grid, beliefMatrix)
                movesList.append("Down")
                print("Down")
             #If action is up -> Execute up move
            elif(actionList[i] == "up"):
                beliefMatrix = moveUp(grid, beliefMatrix)
                movesList.append("Up")
                print("Up")
             #If action is left -> Execute Left move
            elif(actionList[i] == "left"):
                beliefMatrix = moveLeft(grid, beliefMatrix)
                movesList.append("Left")
                print("Left")
             #If action right down -> Execute right move
            elif(actionList[i] == "right"):
                beliefMatrix = moveRight(grid, beliefMatrix)
                movesList.append("Right")
                print("Right")


#Driver Code
grid = readFile_and_returnGrid()
beliefMatrix = initialize_beliefMatrix(grid)
solve_shortest(grid, beliefMatrix)







                
                




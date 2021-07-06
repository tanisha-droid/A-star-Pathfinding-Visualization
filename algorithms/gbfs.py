import pygame, random
from queue import PriorityQueue

# config var
WIDTH = 800
clock = pygame.time.Clock()

# display
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Pathfinding Algorithm')

#colors
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
PURPLE = (153,50,204)
ORANGE = (255,165,0)
TEAL = (0,255,255)
GREY = (100,100,100)

# fonts
pygame.font.init()
font = pygame.font.SysFont("comicsans", 50)

# settings
gridSize = 16
gameSpeed = 30
gridDimensions = WIDTH // gridSize

class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * gridSize
        self.y = col * gridSize
        self.color = WHITE
        self.neighbors = []
    
    def getPosition(self):
        return(self.row, self.col)

    def isClosed(self):
        return(self.color == RED)

    def isOpen(self):
        return(self.color == GREEN)

    def isBarrier(self):
        return(self.color == BLACK)

    def isStart(self):
        return(self.color == ORANGE)
    
    def isEnd(self):
        return(self.color == TEAL)

    def isPath(self):
        return(self.color == PURPLE)

    def reset(self):
        self.color = WHITE

    def makeClosed(self):
        self.color = RED

    def makeOpen(self):
        self.color = GREEN

    def makeBarrier(self):
        self.color = BLACK

    def makeStart(self):
        self.color = ORANGE

    def makeEnd(self):
        self.color = TEAL

    def makePath(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(screen, self.color, (self.x, self.y, gridSize, gridSize))

    def updateNeighbors(self, grid):
        self.neighbors = []

        # going down
        if self.row < gridDimensions - 1 and not grid[self.row+1][self.col].isBarrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # going up
        if self.row > 0 and not grid[self.row-1][self.col].isBarrier():
            self.neighbors.append(grid[self.row-1][self.col])
        # going right
        if self.col < gridDimensions - 1 and not grid[self.row][self.col+1].isBarrier():
            self.neighbors.append(grid[self.row][self.col+1])
        # going left
        if self.col > 0 and not grid[self.row][self.col-1].isBarrier():
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return(False)

# heuristic function
def h(spot1, spot2):
    x1 = spot1.x
    y1 = spot1.y
    x2 = spot2.x
    y2 = spot2.y
    return(abs(x1 - x2) + abs(y1 - y2))

def reconstructPath(cameFrom, current, draw, start, end):
    # goes thru the found path and draws it all
    while current in cameFrom:
        clock.tick(50)
        current.makePath()
        if current == start:
            current.makeStart()
        elif current == end:
            current.makeEnd()
        current = cameFrom[current]
        draw()

# returns the coords of all the lowest heuristics
def getLowestHeuristic(hGrid):
    lowestH = float("inf")
    coords = []
    for rowIndex, row in enumerate(hGrid):
        for itemIndex, item in enumerate(row):
            if item < lowestH:
                lowestH = item
                coords = [[rowIndex, itemIndex]]
            elif item == lowestH:
                coords.append([rowIndex, itemIndex])
        
    # only returns the first one, the others might be used earlier
    return(coords[0])

# THIS ALGORITHM WAS DEVISED BY ME:
# it is probably not the best. I couldn't find much to go off of, so there is probably a lot of improvement that can be made
# that being said; its pretty cool
def algorithm(draw, grid, start, end):

    heuristicGrid = [[float("inf") for i in range(gridDimensions)] for j in range(gridDimensions)]
    heuristicGrid[start.row][start.col] = h(start, end)
    cameFrom = {}

    # main algorithm loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # getting the lowest heuristic from my grid that is open
        lowestCoords = getLowestHeuristic(heuristicGrid)

        # getting the current spot object from the grid
        currSpot = grid[lowestCoords[0]][lowestCoords[1]]

        # loops thru the neighbors of the current spot
        for neighbor in currSpot.neighbors:
            if neighbor.isClosed():
                continue
            heuristicGrid[neighbor.row][neighbor.col] = h(neighbor, end)
            neighbor.makeOpen()
            cameFrom[neighbor] = currSpot
            if neighbor == end:
                reconstructPath(cameFrom, end, draw, start, end)
                return True
        heuristicGrid[lowestCoords[0]][lowestCoords[1]] = float("inf")
        currSpot.makeClosed()

        draw()

    return False


def makeGrid():
    grid = []
    for i in range(gridDimensions):
        grid.append([])
        for j in range(gridDimensions):
            grid[i].append(Spot(i, j))
    return(grid)

def drawGrid(screen, grid):
    for i in range(gridDimensions):
        pygame.draw.line(screen, GREY, (0, i * gridSize), (WIDTH, i * gridSize))
    for j in range(gridDimensions):
        pygame.draw.line(screen, GREY, (j * gridSize, 0), (j * gridSize, WIDTH))

def draw(screen, grid):
    screen.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(screen)
    drawGrid(screen, grid)
    pygame.display.update()

def getClickedPosition(position):
    y, x = position
    row = y // gridSize
    col = x // gridSize
    return(row, col)

def main(screen):
    grid = makeGrid()
    start = None
    end = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # left mouse
            if pygame.mouse.get_pressed()[0]:
                clickPosition = pygame.mouse.get_pos()
                row, col = getClickedPosition(clickPosition)
                spot = grid[row][col]
                if not start and end != spot:
                    start = spot
                    start.makeStart()
                elif not end and start != spot:
                    end = spot
                    end.makeEnd()
                elif spot != end and spot != start:
                    spot.makeBarrier()


            # right mouse
            elif pygame.mouse.get_pressed()[2]:
                clickPosition = pygame.mouse.get_pos()
                row, col = getClickedPosition(clickPosition)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    
                    # getting neighbors of elements
                    for row in grid:
                        for spot in row:
                            spot.updateNeighbors(grid)
                            if spot.isOpen():
                                spot.reset()
                            elif spot.isClosed():
                                spot.reset()
                            elif spot.isPath():
                                spot.reset()

                    # calling the actual algorithm
                    algorithm(lambda: draw(screen, grid), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = makeGrid()

        draw(screen, grid)

if __name__ == "__main__":
    main(screen)
import sys
import string, random
import pygame

from grid import Grid
from terrain import TerrainData, MeteorTerrainGenerator

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
DEFAULT_ZOOM = 10 # zoom by changing block size!
ZOOM_INCREMENT = 5
X_SCROLL = 3
Y_SCROLL = 3

# intiialize and blank the screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
pygame.display.set_caption('Project D.O.R.F.')

viewportX = 0
viewportY = 0
viewportZ = 0
zoom = DEFAULT_ZOOM
columns = SCREEN_WIDTH / zoom
rows = SCREEN_HEIGHT / zoom

# create the grid, fill it with nodes
# this is currently a bit slow...
gameGrid = Grid()
for x in range(-160,160):
    for y in range(-120,120):
        terrain = TerrainData()
        gameGrid.add_node((x, y, 0), terrain)

#gameGrid.connect_grid()

generator = MeteorTerrainGenerator()
generator.apply(gameGrid)

font_file = pygame.font.match_font('freemono')
font = pygame.font.Font(font_file, 14)
font.set_bold(True)

# updates the screen to show the appropriate visible nodes
def updateDisplay():
    screen.fill((0,0,0))
    for x in range(viewportX, viewportX + columns):
        for y in range(viewportY, viewportY + rows):
            terrainNode = gameGrid.get_node_at((x, y, viewportZ))
            if terrainNode != None:
                rectx, recty, rectz = terrainNode.location
                newrectx = (rectx - viewportX) * zoom
                newrecty = recty * zoom
                rect = pygame.Rect(newrectx, newrecty, zoom, zoom)
                terrainNode.contents.render(rect, screen)

    # show current x, y, z in top left corner
    current_view = (viewportX, viewportY, viewportZ)
    text = font.render(str(current_view), 1, (0, 255, 0))
    rect = text.get_rect()
    rect.x, rect.y = (0,0)
    screen.blit(text, rect)

    pygame.display.update()

updateDisplay()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                viewportY -= Y_SCROLL
            if event.key == pygame.K_UP:
                viewportY += Y_SCROLL
            if event.key == pygame.K_LEFT:
                viewportX -= X_SCROLL
            if event.key == pygame.K_RIGHT:
                viewportX += X_SCROLL
            if event.key == pygame.K_PAGEUP:
                viewportZ += 1
            if event.key == pygame.K_PAGEDOWN:
                viewportZ -= 1
            if event.key == pygame.K_z:
                zoom += ZOOM_INCREMENT
                columns = SCREEN_WIDTH / zoom
                rows = SCREEN_HEIGHT / zoom
            if event.key == pygame.K_x:
                if (zoom - ZOOM_INCREMENT) > 0:
                    zoom -= ZOOM_INCREMENT
                    columns = SCREEN_WIDTH / zoom
                    rows = SCREEN_HEIGHT / zoom
            updateDisplay()

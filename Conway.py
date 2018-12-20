import pygame
import time
import random
import os
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (122,122,122)

#initialize
pygame.init()

#set the size
print ("NOTE: The minimum size allowed is 500x500 pixels, while the max is 1400x1000.")
print ("      Any of the larger patterns in the simulation need at least 500 pixels of")
print ("      space to work. If any size outside of these parameters is entered. The")
print ("      simulation will set the size to the default amount of 500x500.")
sizeX = int(input("X length of Screen (in Pixels): "))
sizeY = int(input("Y length of Screen (in Pixels): "))

if (sizeX < 500) or (sizeX > 1400) or (sizeY < 500) or (sizeY > 1000):
    sizeX = 500
    sizeY = 500

# Set the width and height of the screen [width, height]
size = (sizeX, sizeY)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Conway's Game of Life")

# Loop until the user clicks the close button.
done = False
end = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
    
# Setup variables
gridX = []
gridY = []
organismsX = []
organismsY = []
deathX = []
deathY = []
placementX = 20
placementY = 20
pause = False
addpattern = False
firstpress = True
generation = 0
going = False
checkingturn = 1
checkorganismsX = []
checkorganismsY = []
continuelifemode = "off"
borders = "off"

addY = 40
addYadd = 0
rectY = 35
rectYadd = 0

# Preset arrangements                                                                                                                                                                V--this is the last point in the original
GliderGunX = [30, 30, 40, 40, 370, 380, 370, 380, 120, 130, 110, 130, 110, 120, 260, 270, 250, 270, 250, 260, 190, 200, 190, 210, 190, 270, 280, 290, 270, 280, 380, 390, 380, 400, 380] 
GliderGunY = [20, 30, 20, 30, 0, 0, 10, 10, 20, 20, 30, 30, 40, 40, 0, 0, 10, 10, 20, 20, 40, 40, 50, 50, 60, 120, 120, 120, 130, 140, 70, 70, 80, 80, 90]
#GliderX = [70, 80, 60, 70, 80]                                                                                                                                                      #^--this is the last point in the original
#GliderY = [70, 80, 90, 90, 90]
GliderX = [10, 20, 0, 10, 20]
GliderY = [10, 20, 30, 30, 30]
SquareX = [0, 10, 0, 10]
SquareY = [0, 0, 10, 10]
DiamondX = [10, 0, 20, 0, 20, 10]
DiamondY = [0, 10, 10, 20, 20, 30]
SpaceshipX = [20, 20, 30, 40, 50, 60, 60, 60, 50]
SpaceshipY = [30, 50, 20, 20, 20, 20, 30, 40, 50]
MothershipX = [60, 70, 80, 30, 40, 50, 80, 40, 50, 60, 70, 80, 40, 50, 50, 40, 40, 20, 20, 20, 20, 40, 40, 50, 50, 40, 40, 50, 60, 70, 80, 30, 40, 50, 60, 70, 80, 80, 50, 60, 70, 80, 90, 100, 50, 60, 70, 80, 90, 100, 110, 120, 120, 120, 110, 100, 100, 90, 110, 120, 120, 120, 110, 100, 100, 90]
MothershipY = [20, 20, 20, 30, 30, 30, 30, 40, 40, 40, 40, 40, 50, 50, 80, 90, 100, 90, 100, 120, 130, 120, 130, 140, 170, 170, 180, 180, 180, 180, 180, 190, 190, 190, 200, 200, 200, 190, 100, 100, 100, 100, 100, 100, 120, 120, 120, 120, 120, 120, 90, 80, 70, 60, 60, 70, 80, 80, 130, 140, 150, 160, 160, 150, 140, 140]
NukeX = [20, 20, 20, 20, 20, 40, 60, 60, 60, 60, 60, 40]
NukeY = [20, 30, 40, 50, 60, 60, 60, 50, 40, 30, 20, 20]
newshipX = []
newshipY = []

#this loop sets up the grid
currentgridX = 20
currentgridY = 20
for i in range(int((sizeY-40)/10)):
    for i in range(int((sizeX-110)/10)):
        gridX.append(currentgridX)
        gridY.append(currentgridY)
        currentgridX+=10
    currentgridX = 20
    currentgridY += 10

#initial view
for i in range(len(gridX)):
    pygame.draw.rect(screen,WHITE,[gridX[i],gridY[i],10,10], 1)
for i in range(len(organismsX)):
    pygame.draw.rect(screen,WHITE,[organismsX[i],organismsY[i],10,10])
pygame.display.flip()

# ----------- Main Program Loop --------------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            end = True
        elif event.type == pygame.KEYDOWN:
        # Figure out if it was an arrow key. If so
        # adjust speed.
            if event.key == pygame.K_DOWN:
                continuelifemode = "off"
            elif event.key == pygame.K_UP:
                continuelifemode = "on"
            elif event.key == pygame.K_RIGHT:
                borders = "on"
            elif event.key == pygame.K_LEFT:
                borders = "off"
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)

    # Program Logic:

    #adds to the generation count
    if going == True:
        generation += 1

    #This section is for checking to see if the organisms on the screen aren't
    #doing anything. It copies a list to check it later and does it every two
    #turns to avoid having trouble with the shapes that oscilate.
    if (checkingturn == 1) and (pause == False):
        del checkorganismsX[:]
        del checkorganismsY[:]
        for i in range(len(organismsX)):
            checkorganismsX.append(organismsX[i])
            checkorganismsY.append(organismsY[i])
        checkingturn = 2
    else:
        checkingturn = 1

    
    if pause == False: #this way you can pause the game to draw in patterns
        # loop that checks each currently alive square to see if it stays alive
        for i in range(len(organismsX)):
            lifecount = 0
            for b in range(len(organismsX)):
                if (abs(organismsX[i]-organismsX[b])<=10) and (abs(organismsY[i]-organismsY[b])<=10):
                    if (organismsX[i] == organismsX[b]) and (organismsY[i] == organismsY[b]):
                        nothing = 0
                    else:
                        lifecount+=1
                if (borders == "on"):
                    if (abs(organismsX[i]-organismsX[b])==(sizeX-120)) and (abs(organismsY[i]-organismsY[b])<=10):
                        lifecount+=1
                    if (abs(organismsX[i]-organismsX[b])<=10) and (abs(organismsY[i]-organismsY[b])==(sizeY-50)):
                        lifecount+=1
            if (lifecount<2) or (lifecount>3):
                deathX.append(i)
                deathY.append(i)

        """this is for the new life loop"""
        try:
            testorganismsX = organismsX.copy()
            testorganismsY = organismsY.copy()
        except Exception:
            testorganismsX = []
            testorganismsY = []

        """The "Grim Reaper" Loop"""
        if len(deathX)>0:
            for index in sorted(deathX, reverse=True):
                organismsX.pop(index)
                organismsY.pop(index)

        #this loop sees of there is any new life
        for i in range(len(gridX)):
            lifecount = 0
            already_exists = False
            for b in range(len(testorganismsX)):
                if (abs(gridX[i]-testorganismsX[b])<=10) and (abs(gridY[i]-testorganismsY[b])<=10):
                    if (gridX[i] == testorganismsX[b]) and (gridY[i] == testorganismsY[b]):
                        nothing = 0
                    else:
                        lifecount+=1
                if (borders == "on"):
                    if (abs(gridX[i]-testorganismsX[b])==(sizeX-120)) and (abs(gridY[i]-testorganismsY[b])<=10):
                        lifecount+=1
                    if (abs(gridX[i]-testorganismsX[b])<=10) and (abs(gridY[i]-testorganismsY[b])==(sizeY-50)):
                        lifecount+=1

            if (lifecount==3):
                for a in range(len(testorganismsX)):
                    if (gridX[i] == testorganismsX[a]) and (gridY[i] == testorganismsY[a]):
                        already_exists = True 
                if already_exists == False:
                    organismsX.append(gridX[i])
                    organismsY.append(gridY[i])
        del deathX[:]
        del deathY[:]
        del testorganismsX[:]
        del testorganismsY[:]

    #Mouse detection
    pos = pygame.mouse.get_pos()
    mouseX = pos[0]
    mouseY = pos[1]
    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

    #code that follows the mouse
    conflict = False
    for i in range(len(gridX)):
        if (mouseX-gridX[i]<10) and (mouseX-gridX[i]>0) and (mouseY-gridY[i]<10) and (mouseY-gridY[i]>0):
            pygame.draw.rect(screen, WHITE, [gridX[i],gridY[i],10,10])
            placementX = gridX[i]
            placementY = gridY[i]
    if pressed1:
        if (firstpress == True):
            if (pause == False):
                going = True
            firstpress = False
            if (mouseX >= 20) and (mouseX <= sizeX-60) and (mouseY >= 20) and (mouseY <= sizeY-20):
                for i in range(len(organismsX)):
                    if (organismsX[i] == placementX) and (organismsY[i] == placementY):
                        conflict = True
                if conflict == False:
                    organismsX.append(placementX)
                    organismsY.append(placementY)
                    if pause == True:
                        newshipX.append(placementX)
                        newshipY.append(placementY)

            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 35) and (mouseY <= 55):
                addchoiceX = GliderGunX
                addchoiceY = GliderGunY
                addpattern = True
            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 77) and (mouseY <= 97):
                addchoiceX = GliderX
                addchoiceY = GliderY
                addpattern = True
            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 119) and (mouseY <= 139):
                addchoiceX = SquareX
                addchoiceY = SquareY
                addpattern = True
            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 161) and (mouseY <= 181):
                addchoiceX = SpaceshipX
                addchoiceY = SpaceshipY
                addpattern = True
            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 203) and (mouseY <= 223):
                addchoiceX = MothershipX
                addchoiceY = MothershipY
                addpattern = True
            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 245) and (mouseY <= 265):
                addchoiceX = NukeX
                addchoiceY = NukeY
                addpattern = True
            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 287) and (mouseY <= 307):
                if pause == False:
                    going = False
                    pause = True
                elif pause == True:
                    pause = False
            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 329) and (mouseY <= 349):
                del organismsX[:]
                del organismsY[:]
                generation = 0
                going = False
            if (mouseX >= sizeX-84) and (mouseX <= sizeX-24) and (mouseY >= 371) and (mouseY <= 391):
                del organismsX[:]
                del organismsY[:]
                for i in range(len(gridX)):
                    birthchance = random.randint(1,6)
                    if (birthchance == 1):
                        organismsX.append(gridX[i])
                        organismsY.append(gridY[i])

            if (addpattern == True):
                if (addchoiceX != GliderGunX):
                    patternXadd = random.randint(2,(sizeX-200)/10)
                else:
                    patternXadd = 0
                patternXadd *= 10

                if (addchoiceY != SpaceshipY):
                    patternYadd = random.randint(2,(sizeY-100)/10)
                else:
                    patternYadd = random.randint(2,(sizeY-200)/10)
                patternYadd *= 10
                
                for i in range(len(addchoiceX)):
                    conflict = False
                    patternXposition = addchoiceX[i]+patternXadd
                    patternYposition = addchoiceY[i]+patternYadd
                    for b in range(len(organismsX)):
                        if (patternXposition == organismsX[b]) and (patternYposition == organismsY[b]):
                            conflict = True
                    if (conflict == False):
                        organismsX.append(patternXposition)
                        organismsY.append(patternYposition)
            addpattern = False
    else:
        firstpress = True
    if pressed3:
        print (newshipX)
        print (newshipY)
        print (" ")
    # Draw the grid
    for i in range(len(gridX)):
        pygame.draw.rect(screen,WHITE,[gridX[i],gridY[i],10,10], 1)
    if len(organismsX)>0 and len(organismsY)>0:
        for i in range(len(organismsX)):
            pygame.draw.rect(screen,WHITE,[organismsX[i],organismsY[i],10,10])
        
    #Draw the box that has creation options
    pygame.draw.rect(screen,WHITE,[sizeX-88,20,68,sizeY-40], 1)
    for i in range(9):
        pygame.draw.rect(screen,WHITE,[sizeX-84,rectY+rectYadd,60,20])
        rectYadd+=42
    rectYadd = 0

    """The text:"""
    startfont = pygame.font.SysFont('Calibri', 12, True, False)
    text = startfont.render("Glider Gun",True,WHITE)
    screen.blit(text, [sizeX-80, 22])
    text = startfont.render("Glider",True,WHITE)
    screen.blit(text, [sizeX-68, 64])
    text = startfont.render("Square",True,WHITE)
    screen.blit(text, [sizeX-69, 106])
    text = startfont.render("Spaceship",True,WHITE)
    screen.blit(text, [sizeX-78, 148])
    text = startfont.render("Mothership",True,WHITE)
    screen.blit(text, [sizeX-80, 190])
    text = startfont.render("Nuke",True,WHITE)
    screen.blit(text, [sizeX-66, 232])
    text = startfont.render("Pause",True,WHITE)
    screen.blit(text, [sizeX-68, 274])
    text = startfont.render("Clear Screen",True,WHITE)
    screen.blit(text, [sizeX-83, 316])
    text = startfont.render("Clear &",True,WHITE)
    screen.blit(text, [sizeX-74, 350])
    text = startfont.render("Randomize",True,WHITE)
    screen.blit(text, [sizeX-82, 360])
    text = startfont.render("Continue Life",True,WHITE)
    screen.blit(text, [sizeX-86, sizeY-52])
    text = startfont.render("Borders on?",True,WHITE)
    screen.blit(text, [sizeX-84, sizeY-82])
    text = startfont.render("Generation: "+str(generation),True,WHITE)
    screen.blit(text, [25, 5])

    addYadd = 0
    text = startfont.render("ADD",True,BLACK)
    for i in range(9):
        screen.blit(text, [sizeX-66, addY+addYadd])
        addYadd += 42

    #drawing the continuelifemode boxes
    pygame.draw.rect(screen,GREY,[sizeX-75,sizeY-40,40,15])
    if continuelifemode == "off":
        pygame.draw.rect(screen,RED,[sizeX-75,sizeY-40,20,15])
        placetext = startfont.render("NO",True,WHITE)
        screen.blit(placetext, [sizeX-72, sizeY-37])
    else:
        pygame.draw.rect(screen,GREEN,[sizeX-55,sizeY-40,20,15])
        placetext = startfont.render("YES",True,WHITE)
        screen.blit(placetext, [sizeX-54, sizeY-37])

    pygame.draw.rect(screen,GREY,[sizeX-75,sizeY-70,40,15])
    if borders == "off":
        pygame.draw.rect(screen,RED,[sizeX-75,sizeY-70,20,15])
        placetext = startfont.render("OFF",True,WHITE)
        screen.blit(placetext, [sizeX-74, sizeY-67])
    else:
        pygame.draw.rect(screen,GREEN,[sizeX-55,sizeY-70,20,15])
        placetext = startfont.render("ON",True,WHITE)
        screen.blit(placetext, [sizeX-52, sizeY-67])

    #checking to see if the screen is the same
    if len(organismsX) == len(checkorganismsX) and (continuelifemode == "on") and (pause == False):
        conflict = True
        for i in range(len(organismsX)):
            for a in range(len(checkorganismsX)):
                if (organismsX[i] != checkorganismsX[i]):
                    conflict = False
        if conflict == True:
            for i in range(len(gridX)):
                birthchance = random.randint(1,6)
                if (birthchance == 1):
                    organismsX.append(gridX[i])
                    organismsY.append(gridY[i])
        
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 90 frames per second
    clock.tick(180)

pygame.quit()
    

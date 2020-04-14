import math
import time
import matplotlib.pyplot as plotter
from PIL import Image


#Values are in minecraft blocks
global width
global height
global catConstant

#user configurable values. Values are expressed in minecraft blocks
width = 100
height = 10

#internal values
catConstant = 0.1

#returns the y position of arch as a function of x
def arch(xPos):
    global width
    global height
    global catConstant
    return (catConstant * math.cosh(((width / 2) / catConstant))) - (catConstant * math.cosh((xPos / catConstant)))

#itertively calulates the catConstant
def calculateCatConstant():
    global catConstant
    global height

    maxima = arch(0)
    while not(math.isclose(maxima, height,rel_tol= 0.00001, abs_tol=0.01) and (maxima) < height):
        catConstant = 0.0001 + catConstant
        maxima = arch(0)



#calulate arch
print("Starting calculation...")
millis = int(round(time.time() * 1000))

try:
    calculateCatConstant()
except OverflowError:
    print("Your values are out of range. Please use smaller height and/or width values")
    exit(1)
print(catConstant)
print(arch(0))
print("Completed in " + str(int(round(time.time() * 1000)) - millis) + " milliseconds")


print("Constructing plotter")
#construct scatter plot
archData = []
xData = []
for x in range(int(-width/2), int(width/2) + 1):
    archData.append(round(arch(x)))
    xData.append(x)


#construct smooth plot
smoothArchData = []
smoothXData = []
x = -width/2
while x < width/2:
    smoothArchData.append(arch(x))
    smoothXData.append(x)
    x = x + 0.01

plotter.plot(smoothXData, smoothArchData, 'g')


#construct x.5 (xHalf) plot
xHalfArchData = []
xHalfData = []
x = -width/2

if x.is_integer():
    x = x + 0.5
else:
    x = x + 1

print("Initital 0.5X: " + str(x))

while x < (width / 2):
    xHalfArchData.append(round(arch(x)))
    xHalfData.append(x)
    x = x + 1

#construct final block data
finalY = []
finalX =[]

index = 0
#print("===========================================================================================================================================")
#print("Data set:")
#print(archData)
#print(xHalfArchData)
#print("===========================================================================================================================================")

while index < math.floor(width / 2): # do the first half of the arch
    print()
    print("===========================================================================================================================================")
    print("index: " + str(index))
    print("archData: " + str(archData[index]))
    print("halfXArchData: " + str(xHalfArchData[index - 1]))
    print()

    #Below
    subtractor = 1
    for i in range(xHalfArchData[index - 1], archData[index]):
        finalX.append(index - math.floor(width / 2))
        finalY.append(archData[index] - subtractor)
        subtractor = subtractor + 1

    #Above
    for i in range(archData[index], xHalfArchData[index] + 1):
        finalX.append(index - math.floor(width / 2))
        finalY.append(i)

    #Adds it's own posistion
    finalX.append(index - math.floor(width / 2))
    finalY.append(archData[index])

    index = index + 1

#add the middle block to the final data
finalX.append(0)
finalY.append(height)

#reverse and append for the other half of the arch

for i in reversed(finalY):
    finalY.append(i)

for i in reversed(finalX):
    finalX.append(i*-1)

plotter.scatter(finalX, finalY)

#format and show plots
plotter.axis([math.ceil(-width / 2) - 1, math.floor(width / 2) + 1, 0, height + 1])
plotter.xticks(xData, range(0, width + 1))
plotter.xticks(xData)
plotter.yticks(range(0, height + 1))
plotter.grid(True, which= "major", axis = "both")
plotter.gca().set_aspect('equal', adjustable='box')

#image result section =================================================================================================

#image height in pixels = 14 + 12 * height
#image width in pixels = 14 + 12 *

imgHeight = 14 + (12 * height)
imgWidth = 14 + (12 * height)

image = Image.new("RGB", (imgWidth, imgHeight), "white")

#create bars on side
image.paste((0, 0, 0), (0, 0, 2, imgWidth))
image.paste((0, 0, 0), (0, 0, imgHeight, 2))

#shift finalX so that it starts at 0
shift = finalX[0] * (-1)

for i in range(0, len(finalX)):
    finalX[i] = finalX[i]+ shift


#create and populate the grid - reflects blocks in game
grid = [] #2D array arranged x, y
for i in range(0, width + 1):
    gridY = []
    for k in range(0, height + 1):
        gridY.append(False)
    grid.append(gridY)

for i in range(0, len(finalX) - 1):
    grid[finalX[i]][finalY[i]] = True

#paste in images based on grid
empty = Image.open('empty.bmp')
full = Image.open('full.bmp')

cursorX = 2
cursorY = 2
for i in range(0, len(grid)):
    cursorY = 2
    for k in range(0, len(grid[i])):
        print("x: " + str(cursorX))
        print("y: " + str(cursorY))
        print()
        if grid[i][k] == True:
            image.paste(full, (cursorX, cursorY))
        else:
            image.paste(empty, (cursorX, cursorY))
        cursorY = cursorY + 12
    cursorX = cursorX + 12






#finish and display outputs ===========================================================================================

image = image.rotate(180)
image.show()
plotter.show()


print("Finished")


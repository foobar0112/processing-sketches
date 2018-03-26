from random import randint
from math import copysign
from time import time

add_library('minim')
minim = Minim(this)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def setVerts(dx, dy, minV, maxV):
    d = int(min(width / (dx * 2), height / (dy * 2)) * 0.9)
    v = [[{} for j in range(dy)] for i in range(dx)] 
    for i in range(0, dx):
        for j in range(0, dy):
            numVert = randint(minV, maxV)
            for k in range(numVert):
                v[i][j][k] = (randint(-d, d),
                                  randint(-d, d),
                                  randint(-d, d))
    return v, d

def setup():
    global tick, verts, mousing, INPUT, CAGE_SIZE, DIM_X, DIM_Y, ROTATION_SPEED, SHAKE_VAL, SHAKE_VAL_NORM, COLOR_THRESH
    
    # some helpers
    mousing = False
    tick = 0
    
    # invers rotation speed, the grater, the slower; if 0 no rotation
    ROTATION_SPEED = 20
    
    # shaking value (needed twice to reset after mouse action)
    SHAKE_VAL, SHAKE_VAL_NORM = 0.001, 0.001
    
    # dimensions of the grid
    DIM_X, DIM_Y = 6, 4
    
    # value of the mean amplitude to show colors and rotate randomly
    COLOR_THRESH = 0.3
    
    verts, CAGE_SIZE = setVerts(DIM_X, DIM_Y, 4, 8)
    
    #size(2560 / 2, 1440, P3D)
    fullScreen(P3D)
    
    # set color mode to HSB
    colorMode(HSB)
    strokeJoin(ROUND) #not sure if this has any effect in 3D
    noFill()
    noCursor()
    background(0)
    
    # enable antialising
    smooth(4)
    
    # zoom in z coordinate
    camera(width/2.0, height/2.0, (height/2.0) / tan(PI*30.0 / 180.0) * 0.85, 
           width/2.0, height/2.0, 0, 
           0, 1, 0)
    
    # get systems default audio input
    INPUT = minim.getLineIn(minim.STEREO)

# monitor time, mouse is pressed
def mousePressed():
    global mouseTime, mousing
    mouseTime = time()
    mousing = True

# if released generate new shapes and reset effect values
def mouseReleased():
    global verts, CAGE_SIZE, SHAKE_VAL, mousing
    mousing = False
    SHAKE_VAL = SHAKE_VAL_NORM
    numV = int((time() - mouseTime) * 10) + 5
    verts, CAGE_SIZE = setVerts(DIM_X, DIM_Y, max(3, min(32, numV/2)), min(64, numV))

def draw():
    global tick, SHAKE_VAL
    tick = tick + 1
    
    clear()
    # adapt view point to mouse position
    camera(width/2.0, height/2.0, (height/2.0) / tan(PI*30.0 / 180.0) * 0.85, 
           width/2.0 + copysign(sqrt(abs(mouseX - width/2.0)), mouseX - width/2.0), 
           height/2.0 + copysign(sqrt(abs(mouseY - height/2.0)), mouseY - height/2.0), 
           0, 
           0, 1, 0)
    
    # color is changing constantly
    hueVal = int(((sin(tick / 500.0) + 1) / 2.0) * 255)
    
    # listen to input (system settings matter!) calc mean and max amplitude value
    amps = INPUT.mix.toArray()
    maxAmp = max(amps)
    meanAmp = max(0, mean(amps)) * 10
    
    # as long as pressed increase shaking and colorfy
    if mousing:
        SHAKE_VAL = SHAKE_VAL * 1.01
        SHAKE_VAL = min(0.05, SHAKE_VAL)
        meanAmp = COLOR_THRESH
    
    # choose color according to current hue and amplitude
    stroke(hueVal, 255 * meanAmp, 150 * maxAmp + 105)
    
    # go through matrix and draw shapes
    for i in range(DIM_X):
        for j in range(DIM_Y):
            
            # initialize sum for normalization
            sumX, sumY, sumZ = 0, 0, 0
            
            pushMatrix()
            
            # move shape to position
            translate((width / (DIM_X + 1)) * (i + 1), (height / (DIM_Y + 1)) * (j + 1))
            
            # scale acording to amplitude; creates zoom effect
            scale(maxAmp * 0.6 + 0.5)
            
            # do random rotation around an axe if music is exploding
            if meanAmp > COLOR_THRESH:
                strokeWeight(4)
                r = randint(0,2)
                if r == 0:
                    rotateX(radians(40 * meanAmp))
                elif r == 1:
                    rotateY(radians(40 * meanAmp))
                else:
                    rotateZ(radians(40 * meanAmp))
            else:
                strokeWeight(2)
            
            # do normal rotation acording to ROTATION_SPEED
            if ROTATION_SPEED > 0:
                rotateX(radians(tick) / ROTATION_SPEED)
                rotateY(radians(tick) / ROTATION_SPEED)
                rotateZ(radians(tick) / ROTATION_SPEED)
            
            beginShape()
            for k in range(len(verts[i][j]) - 1):
                vertex(verts[i][j][k][0], 
                       verts[i][j][k][1], 
                       verts[i][j][k][2])
                
                # calculate new vertex position in x,y according shaking value, but stay in the cage
                newX = min(CAGE_SIZE, max(-CAGE_SIZE, verts[i][j][k][0] + randint(- int(width * SHAKE_VAL), int(width * SHAKE_VAL))))
                newY = min(CAGE_SIZE, max(-CAGE_SIZE, verts[i][j][k][1] + randint(- int(height * SHAKE_VAL), int(height * SHAKE_VAL))))
                
                verts[i][j][k] = (newX, newY, verts[i][j][k][2])
                
                sumX = sumX + verts[i][j][k][0]
                sumY = sumY + verts[i][j][k][1]
                sumZ = sumZ + verts[i][j][k][2]
            endShape(CLOSE)
            popMatrix()
            
            # focus shape to middle of cage
            l = len(verts[i][j]) - 1
            normX = sumX / l
            normY = sumY / l
            normZ = sumZ / l
            for k in range(len(verts[i][j]) - 1):
                verts[i][j][k] = (verts[i][j][k][0] - normX, verts[i][j][k][1] - normY, verts[i][j][k][2] - normZ)
from math import copysign
from time import time

add_library('minim')
minim = Minim(this)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def setVerts(dx, dy, minV, maxV):
    # set new noise seed at first
    noiseSeed(int(time()) % (2 ** 16))
    d = int(min(width / (dx + 1), height / (dy + 1)))
    v = [[{} for j in range(dy)] for i in range(dx)] 
    for i in range(0, dx):
        for j in range(0, dy):
            numVert = int(random(minV, maxV))
            for k in range(numVert + 1):
                v[i][j][k] = (map(noise(i, k, 0), 0, 1, -d, d),
                              map(noise(j, k, 1), 0, 1, -d, d),
                              map(noise(k, k, 2), 0, 1, -d, d))
    return v, d

def setup():
    global tick, verts, mousing, INPUT, CAGE_SIZE, DIM_X, DIM_Y, ROTATION_SPEED, SHAKE_VAL, SHAKE_VAL_NORM, EXPLOSION_TH
    
    # some helpers
    mousing = False
    tick = 0
    
    # rotation speed, if 0 no rotation
    ROTATION_SPEED = 0.5
    
    # shaking value (needed twice to reset after mouse action)
    SHAKE_VAL, SHAKE_VAL_NORM = 0.001, 0.001
    
    # dimensions of the grid
    DIM_X, DIM_Y = 3, 3
    
    # value of amplitude to show colors, rotate randomly and other stuff
    EXPLOSION_TH = 0.8
    
    verts, CAGE_SIZE = setVerts(DIM_X, DIM_Y, 3, 3)
    
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
    global MOUSE_TIME, mousing
    MOUSE_TIME = time()
    mousing = True

# if released generate new shapes and reset effect values
def mouseReleased():
    global verts, CAGE_SIZE, SHAKE_VAL, mousing
    mousing = False
    SHAKE_VAL = SHAKE_VAL_NORM
    numV = int((time() - MOUSE_TIME) * 5) + 2
    verts, CAGE_SIZE = setVerts(DIM_X, DIM_Y, max(3, min(32, numV/2)), min(64, numV))

# change dimension, rotation speed, shaking value and explosion threshold on key press
def keyPressed():
    global DIM_X, DIM_Y, verts, CAGE_SIZE, ROTATION_SPEED, SHAKE_VAL, SHAKE_VAL_NORM, EXPLOSION_TH
    
    dimChanged = False
    if(key == CODED):
        if(keyCode == RIGHT):
            DIM_X = min(30, DIM_X + 1)
            dimChanged = True
        elif(keyCode == LEFT):
            DIM_X = max(1, DIM_X - 1)
            dimChanged = True
        elif(keyCode == UP):
            DIM_Y = min(30, DIM_Y + 1)
            dimChanged = True
        elif(keyCode == DOWN):
            DIM_Y = max(1, DIM_Y - 1)
            dimChanged = True
    elif(key.lower() == 'w'):
        ROTATION_SPEED = min(20, ROTATION_SPEED + 0.2)
    elif(key.lower() == 's'):
        ROTATION_SPEED = max(0, ROTATION_SPEED - 0.2)
    elif(key.lower() == 'd'):
        SHAKE_VAL = min(0.05, SHAKE_VAL * 1.2)
        SHAKE_VAL_NORM = SHAKE_VAL
    elif(key.lower() == 'a'):
        SHAKE_VAL = max(0.0001, SHAKE_VAL / 1.2)
        SHAKE_VAL_NORM = SHAKE_VAL
    elif(key.lower() == 'e'):
        EXPLOSION_TH = min(1, EXPLOSION_TH + 0.05)
    elif(key.lower() == 'q'):
        EXPLOSION_TH = max(0, EXPLOSION_TH - 0.05)
        
    if(dimChanged):
        verts, CAGE_SIZE = setVerts(DIM_X, DIM_Y, 3, 3)

def draw():
    global tick, SHAKE_VAL
    tick += 1
    clear()    
    
    # adapt view point to mouse position
    camera(width/2.0, height/2.0, (height/2.0) / tan(PI*30.0 / 180.0) * 0.85, 
           width/2.0 + copysign(sqrt(abs(mouseX - width/2.0)), mouseX - width/2.0), 
           height/2.0 + copysign(sqrt(abs(mouseY - height/2.0)), mouseY - height/2.0), 
           0, 0, 1, 0)
    
    # color is changing constantly
    hueVal = map(sin(tick/500.0), -1, 1, 0, 255)
    
    # listen to input (system settings matter!) calc mean and max amplitude value
    amps = INPUT.mix.toArray()
    maxAmp = max(amps)
    meanAmp = max(0, mean(amps)) * 10
    
    # as long as pressed increase shaking and colorfy
    if mousing: 
        SHAKE_VAL = min(0.05, SHAKE_VAL * 1.005)
        meanAmp = EXPLOSION_TH
        
        # print number of verts in bottom left corner
        fill(100)
        textSize(18)
        text(min(64, max(3, int((time() - MOUSE_TIME) * 5) + 2)), width * 0.05, height * 0.95, 0)
        noFill()
    
    # choose color according to current hue and amplitude
    stroke(hueVal, map(meanAmp, 0, 1, 0, 150), map(maxAmp, 0, 1, 150, 255))
    
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
            
            # do random rotation around an axe and colorise if music is exploding
            if maxAmp > EXPLOSION_TH:
                strokeWeight(10)
                stroke(hueVal, map(maxAmp, 0, 1, 120, 200), map(maxAmp, 0, 1, 150, 200))
                tick += 50 * meanAmp
                r = int(random(0,2))
                if r == 0:
                    rotateX(-radians(40 * meanAmp))
                elif r == 1:
                    rotateY(-radians(40 * meanAmp))
                else:
                    rotateZ(-radians(40 * meanAmp))
            else:
                strokeWeight(3)
            
            # do normal rotation acording to ROTATION_SPEED with different offset per shape
            if ROTATION_SPEED > 0:
                rotateX(radians(tick + verts[i][j][0][0]) / (1.0/ROTATION_SPEED))
                rotateY(radians(tick + verts[i][j][0][0]) / (1.0/ROTATION_SPEED))
                rotateZ(radians(tick + verts[i][j][0][0]) / (1.0/ROTATION_SPEED))
            
            beginShape()
            for k in range(len(verts[i][j]) - 1):
                vertex(verts[i][j][k][0], 
                       verts[i][j][k][1], 
                       verts[i][j][k][2])
                
                # calculate new vertex position in x,y according shaking value, but stay in the cage
                newX = min(CAGE_SIZE, max(-CAGE_SIZE, verts[i][j][k][0] + random(- int(width * SHAKE_VAL), int(width * SHAKE_VAL))))
                newY = min(CAGE_SIZE, max(-CAGE_SIZE, verts[i][j][k][1] + random(- int(height * SHAKE_VAL), int(height * SHAKE_VAL))))
                
                verts[i][j][k] = (newX, newY, verts[i][j][k][2])
                
                sumX += verts[i][j][k][0]
                sumY += verts[i][j][k][1]
                sumZ += verts[i][j][k][2]
            endShape(CLOSE)
            popMatrix()
            
            # focus shape to middle of cage
            l = len(verts[i][j]) - 1
            normX = sumX / l
            normY = sumY / l
            normZ = sumZ / l
            for k in range(len(verts[i][j]) - 1):
                verts[i][j][k] = (verts[i][j][k][0] - normX, verts[i][j][k][1] - normY, verts[i][j][k][2] - normZ)

add_library('minim')
minim = Minim(this)

def setup():
    fullScreen(P2D)
    colorMode(HSB)
    noCursor()
    background(0)
    stroke(255)
    smooth(8)
    frameRate(25)
    strokeJoin(ROUND)
    
    global A, DIM, DIMX, T, INPUT, BEAT, TICK, THRESH
    INPUT = minim.getLineIn(Minim.STEREO)
    BEAT= BeatDetect(1024, 48000)
    BEAT.setSensitivity(350)
    BEAT.detectMode(BeatDetect.FREQ_ENERGY)
    DIM = 7.0
    T = 20
    TICK = 0
    THRESH = 0.6
    DIMX = ceil(width / (height / DIM))
    print(height, width)
    print(DIMX)
    A = [[45 + int(random(0,3)) * 90 for j in range(int(DIM * 2))] for i in range(DIMX * 3)]

def diff(w, a):
    if a >= 0 and a < 45:
        return (w/2.0) * (1 - tan(radians(45 - a)))
    elif a >=45 and a <= 90:
        return (w/2.0) * (1 + tan(radians(a - 45)))
 
def xd(w, a):
    a = a % 360
    if a > 0 and a < 90:
        return diff(w, a)
    elif a >= 90 and a <= 180:
        return w
    elif a > 180 and a < 270:
        return diff(w, -1 * (a - 270))
    else:
        return 0

def yd(w, a):
    a = a % 360
    if a >= 0 and a <= 90:
        return 0
    elif a > 90 and a < 180:
        return diff(w, a - 90)
    elif a >= 180 and a <= 270:
        return w
    else:
        return diff(w, -1 * (a - 360))
    

def xd1(w, a):
    a = a % 360
    if a > 0 and a < 90:
        return diff(w + T, a)
    elif a >= 90 and a <= 180:
        return w
    elif a > 180 and a < 270:
        return diff(w - T, -1 * (a - 270))
    else:
        return 0

def yd1(w, a):
    a = a % 360
    if a >= 0 and a <= 90:
        return 0
    elif a > 90 and a < 180:
        return diff(w - T, a - 90)
    elif a >= 180 and a <= 270:
        return w
    else:
        return diff(w + T, -1 * (a - 360))

def xd2(w, a):
    a = a % 360
    if a > 0 and a < 90:
        return diff(w - T, a)
    elif a >= 90 and a <= 180:
        return w
    elif a > 180 and a < 270:
        return diff(w + T, -1 * (a - 270))
    else:
        return 0

def yd2(w, a):
    a = a % 360
    if a >= 0 and a <= 90:
        return 0
    elif a > 90 and a < 180:
        return diff(w + T, a - 90)
    elif a >= 180 and a <= 270:
        return w
    else:
        return diff(w - T, -1 * (a - 360))


def tile(x, y, w, angle):
    strokeWeight(5)
    
    #stroke(255, 255, 255)
    #line(x + xd(w, angle), y + yd(w, angle), x + xd(w, angle + 90), y + yd(w, angle + 90))
    
    stroke(255)
    #line(x + xd1(w, angle), y + yd1(w, angle), x + xd1(w, angle + 90), y + yd1(w, angle + 90))
    #line(x + xd2(w, angle), y + yd2(w, angle), x + xd2(w, angle + 90), y + yd2(w, angle + 90))
    
    fill(255)
    beginShape()
    vertex(x + xd1(w, angle), y + yd1(w, angle))
    vertex(x + xd1(w, angle + 90), y + yd1(w, angle + 90))
    vertex(x + xd2(w, angle + 90), y + yd2(w, angle + 90))
    vertex(x + xd2(w, angle), y + yd2(w, angle))
    endShape(CLOSE)
    beginShape()
    vertex(x + xd1(w, angle + 180), y + yd1(w, angle + 180))
    vertex(x + xd1(w, angle + 270), y + yd1(w, angle + 270))
    vertex(x + xd2(w, angle + 270), y + yd2(w, angle + 270))
    vertex(x + xd2(w, angle + 180), y + yd2(w, angle + 180))
    endShape(CLOSE)
    noFill()
    
    stroke(0)
    rect(x, y, w, w)

def draw():
    global A, DIM, TICK, T
    TICK += 0.1
    x_0, y_0 = 200, 200
    background(0)
    
    BEAT.detect(INPUT.mix)
    if BEAT.isKick():
        for i in range(0, DIMX * 2):
            for j in range(0, int(DIM) * 2):
                if noise(i + TICK, j + TICK) > THRESH:
                    A[i][j] += int(random(-2,2)) * 90
    if BEAT.isSnare():
        T = min(80, T * 1.4)
    else:
        T = max(10, T * 0.95)
    
    i = 0
    for x in range(0, width, int(height/DIM)):
        j = 0
        for y in range(0, height, int(height/DIM)):
            tile(x, y, height/DIM, A[i][j])
            j += 1
        i += 1

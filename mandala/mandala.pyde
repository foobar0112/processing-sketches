from math import copysign

add_library('minim')
minim = Minim(this)


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def setup():
    global INPUT, BEAT, t, amp, isB
    amp = 0
    fullScreen(P2D)

    colorMode(HSB)
    strokeJoin(ROUND)
    noFill()
    noCursor()
    background(255)
    stroke(0,0,100)

    smooth(8)

    t = 0
    INPUT = minim.getLineIn(minim.STEREO)
    BEAT= BeatDetect()
    isB = 0


def x1(i):
    return cos(i / map(mouseY, 0, height, 9.0, 10.0)) * 150 + map(mouseX, 0, width, -100, 100) - map(mouseY, 0, height, -100, 100)

def y1(i):
    return sin(i / map(mouseX, 0, width, 10.0, 11.0)) * 200 + sin(i / map(mouseY, 0, height, 15.0, 16.0)) * 100 + map(mouseX, 0, width, -100, 100)

def x2(i):
    return cos(i / map(mouseY, 0, height, 27.0, 28.0)) * 300 - cos(i / map(mouseX, 0, width, 20.0, 19.0)) * 100 - map(mouseX, 0, width, -100, 100)

def y2(i):
    return sin(i / map(mouseX, 0, width, 21.0, 22.0)) * 200 + cos(i / map(mouseY, 0, height, 51.0, 50.0)) * 300 + map(mouseY, 0, height, -100, 100)

def draw():
    global t, amp, isB
    t += 1
    background(0)
    translate(width/2, height/2)
    
    rotate(-radians(t / 5.0))
    
    BEAT.detect(INPUT.mix)
    if BEAT.isOnset():
         isB = 1
    isB *= 0.95

    #j = 1
    for j in range(0, 100):
        i = j
        scale(map(i, 0, 100.0, map(isB, 0, 1, 1.0015, 1.0022), 0.998))
        
        stroke(t % 255, 100, map(i, 0, 100.0, 0, 255), 100)
        strokeWeight(map(i, 0, 100.0, 3, 5))
        point(x1(t + i), y1(t + i))
        point(x2(t + i), y2(t + i))
        
        strokeWeight(map(i, 0, 100.0, 0, 5))
        line(x1(t + i), y1(t + i), x2(t + i), y2(t + i))

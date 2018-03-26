from random import randint

def setup():
    global diff, verts, dimX, dimY
    
    dimX, dimY = 4, 4
    diff = min(width / (dimX * 2), height / (dimY * 2))
    
    verts = [[{} for j in range(dimY)] for i in range(dimX)] 
    for i in range(0, dimX):
        for j in range(0, dimY):
            numVert = randint(5,9)
            for k in range(numVert):
                verts[i][j][k] = (randint(- diff,diff),
                                  randint(- diff,diff),
                                  randint(- diff,diff))
            verts[i][j][len(verts)] = verts[i][j][0]
    
    fullScreen(P3D)
    stroke(255)
    noFill()
    background(0)

def draw():
    clear()
    
    for i in range(dimX):
        for j in range(dimY):
            sumX, sumY, sumZ = 0, 0, 0
            beginShape()
            for k in range(len(verts[i][j])):
                vertex((width / (dimX + 1)) * (i + 1) + verts[i][j][k][0], 
                    (height / (dimY + 1)) * (j + 1) + verts[i][j][k][1], 
                    verts[i][j][k][2])
                verts[i][j][k] = (verts[i][j][k][0] + int(randint(- int(diff * 0.01), int(diff * 0.01))),
                            verts[i][j][k][1] + int(randint(- int(diff * 0.01), int(diff * 0.01))),
                            verts[i][j][k][2] + int(randint(- int(diff * 0.01), int(diff * 0.01))))
                sumX = sumX + verts[i][j][k][0]
                sumY = sumY + verts[i][j][k][1]
                sumZ = sumZ + verts[i][j][k][2]
            endShape()
            
            normX = sumX / (len(verts[i][j]) - 1)
            normY = sumY / (len(verts[i][j]) - 1)
            normZ = sumZ / (len(verts[i][j]) - 1)
            
            for k in range(len(verts[i][j]) - 1):
                verts[i][j][k] = (verts[i][j][k][0] - normX,
                            verts[i][j][k][1] - normY,
                            verts[i][j][k][2] - normZ)
            
            verts[i][j][len(verts[i][j]) - 1] = verts[i][j][0]

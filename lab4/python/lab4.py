#!/usr/bin/python2.7
from numpy import sin, cos, arctan2, sqrt, radians, degrees, matrix, array, pi
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def getM(phi, a, e):
    return (a * (1 - e**2)) / sqrt((1 - e**2 * sin(phi)**2)**3)

def getN(phi, a, e):
    return a / sqrt(1 - e**2 * sin(phi)**2)

def printAngle(thita):
    thita_1 = abs(degrees(thita))
    degree = int(thita_1)
    minute = abs(int((1.0 * thita_1 - degree) * 60))
    second = abs((1.0 * thita_1 - degree - (1.0 * minute / 60)) * 3600)
    if thita < 0:
        print "-%d:%d:%f" % (degree, minute, second)
    else:
        print "%d:%d:%f" % (degree, minute, second)
    
#x,y,z-l,p,h
def xyz2lph(x, y, z, a, e):
    l = arctan2(y, x)
    p0 = arctan2(z, sqrt(x**2 + y**2))
    N0 = getN(p0, a, e)
    p = arctan2((z + N0 * e**2 * sin(p0)), sqrt(x**2 + y**2))
    while not (p - p0 < 10**-12):
        p0 = p
        N0 = getN(p0, a, e)
        p = arctan2((z + N0 * e**2 * sin(p0)), sqrt(x**2 + y**2))
    N = getN(p, a, e)
    he = sqrt(x**2 + y**2 + (z + N * e**2 * sin(p))**2)  - N
    #he2 = sqrt(x**2 + y**2) / cos(p) - N
    return l, p, he

#l,p,h-x,y,z
def lph2xyz(l, p, he, a, e):
    N = getN(p, a, e)
    x = (N + he) * cos(p) * cos(l)
    y = (N + he) * cos(p) * sin(l)
    z = (N * (1 - e**2) + he) * sin(p)
    return x, y, z

#x,y,z-e,n,u
def xyz2enu(x, y, z, xp, yp, zp, a, e):
    lp, pp, hp = xyz2lph(xp, yp, zp, a, e)
    
    Ry = matrix([[cos((pi / 2) - pp), 0, -sin((pi / 2) - pp)], [0, 1, 0], [sin((pi / 2) - pp), 0, cos((pi / 2) - pp)]])

    Rz = matrix([[cos(lp), sin(lp), 0], [-sin(lp), cos(lp), 0], [0, 0, 1]])
    
    X = matrix([[x - xp], [y - yp], [z - zp]])

    Ans = array(Ry * Rz * X)
    N = -Ans[0][0]    
    E = Ans[1][0]    
    U = Ans[2][0]    
    
    return E, N, U

#e,n,u-x,y,z
def enu2xyz(E, N, U, xp, yp, zp, a, e):
    lp, pp, hp = xyz2lph(xp, yp, zp, a, e)
    
    Ry = matrix([[cos((pi / 2) - pp), 0, -sin((pi / 2) - pp)], [0, 1, 0], [sin((pi / 2) - pp), 0, cos((pi / 2) - pp)]])

    Rz = matrix([[cos(lp), sin(lp), 0], [-sin(lp), cos(lp), 0], [0, 0, 1]])
    
    T = matrix([[xp], [yp], [zp]])
    X = [[-N], [E], [U]]

    Ans = array(Rz.T * Ry.T * X + T)

    x = Ans[0][0]    
    y = Ans[1][0]    
    z = Ans[2][0]    

    return x, y, z

def enu2topo(E, N, U):
    Az = arctan2(E, N)
    El = arctan2(U, sqrt(E**2 + N**2))
    Sr = sqrt(E**2 + N**2 + U**2)
    
    return Az, El, Sr

def topo2enu(Az, El, Sr):
    E = Sr * cos(El) * sin(Az)
    N = Sr * cos(El) * cos(Az)
    U = Sr * sin(El)
    
    return E, N, U
    

def gendata(a, e):
    points = []
    lph_old = []
    for i in range(30, 331, 60):
        for j in range(-70, 71, 20):
            points.append(lph2xyz(radians(i), radians(j), 0, a, e))
            lph_old.append((j, i, 0))
    lph_old.append((90, 0, 0))
    lph_old.append((-90, 0, 0))
    points.append(lph2xyz(0, 0.5 * pi, 0, a, e))
    points.append(lph2xyz(0, -0.5 * pi, 0, a, e))
            
    return points, lph_old

def main():
    
    #define initial variable
    a = 6378137.0
    f = 1.0 / 298.257222101 
    b = a - a * f
    e = sqrt((a**2 - b**2) / a**2)
    
    #outp = radians(64 + 1.0 / 60 +  45.33240 / 3600)
    #outl = radians(-(142 + 4.0 / 60 + 32.94873 / 3600))
    #print degrees(outl)
    #h = 745.09
    
    #print lph2xyz(outl, outp, h, a, e)
    #return
    
    
    x0y0z0, lph_old = gendata(a, e)
    lph = []
    enu = []
    AzElSr = []
    xyz = []
    for i in range(50):
        lph.append(xyz2lph(x0y0z0[i][0], x0y0z0[i][1], x0y0z0[i][2], a, e))
        enu.append(xyz2enu(x0y0z0[i][0], x0y0z0[i][1], x0y0z0[i][2], x0y0z0[0][0], x0y0z0[0][1], x0y0z0[0][2], a, e))
        AzElSr.append(enu2topo(enu[i][0], enu[i][1], enu[i][2]))
        xyz.append(lph2xyz(lph[i][0], lph[i][1], lph[i][2], a, e))

    Pt_ID = [i for i in range(1, 51)]
    x0 = [point[0] for point in x0y0z0]
    y0 = [point[1] for point in x0y0z0]
    z0 = [point[2] for point in x0y0z0]
    l = [point[0] for point in lph]
    p = [point[1] for point in lph]
    h = [point[2] for point in lph]
    x = [point[2] for point in xyz]
    y = [point[2] for point in xyz]
    z = [point[2] for point in xyz]
    E = [point[0] for point in enu]
    N = [point[1] for point in enu]
    U = [point[2] for point in enu]
    Az = [point[0] for point in AzElSr]
    El = [point[1] for point in AzElSr]
    Sr = [point[2] for point in AzElSr]
    dx = []
    dy = []
    dz = []
    absdx = []
    absdy = []
    absdz = []
    dx2 = []
    dy2 = []
    dz2 = []
    for i in range(len(x0)):
        print "%d\t%.13f\t%.13f\t%.13f\t%.13f\t%.13f\t%.13f\t%.13f\t%.13f\t%.13f\t%.13f\t%.13f\t%.13f\t" % (Pt_ID[i], x0[i], y0[i], z0[i], p[i], l[i], h[i], E[i], N[i], U[i], Az[i], El[i], Sr[i]) 
        dx.append(x0[i] - x[i])
        dy.append(y0[i] - y[i])
        dz.append(z0[i] - z[i])
        absdx.append(abs(dx[i]))
        absdy.append(abs(dy[i]))
        absdz.append(abs(dz[i]))
        dx2.append(dx[i]**2)
        dy2.append(dy[i]**2)
        dz2.append(dz[i]**2)
    
    #print matrix([Pt_ID, x0, y0, z0, l, p, h])
    
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(x0, y0, z0, c = 'b', marker = '*')
    #ax.scatter(E, N, U, c = 'r', marker = 'x')
    #ax.set_xlabel('X Label')
    #ax.set_ylabel('Y Label')
    #ax.set_zlabel('Z Label')
    #plt.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf([lph_old[i][0] for i in range(48)], [lph_old[i][1] for i in range(48)], dy[:-2], linewidth=1, color='r', cmap=plt.cm.CMRmap)
    #plt.plot([lph_old[i][0] for i in range(50)], dy)
    #plt.plot([lph_old[i][0] for i in range(50)], dz)
    ax.set_xlabel('lat')
    ax.set_ylabel('lon')
    ax.set_zlabel('dx')
    plt.show()
    
    
    
    
    return 0

if __name__ == "__main__":
    main()


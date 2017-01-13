'''
Created on 2014/06/02

@author: otakusaikou1
'''
from numpy import array, set_printoptions, radians, cos, sin, tan, append, random, sqrt, matrix, pi
from numpy.matlib import repmat
from mpl_toolkits.mplot3d import Axes3D, proj3d
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt

#disable scientific notation
set_printoptions(suppress=True)

#define constants
R = 6371000.0

def readData(filename):
    fin = open(filename)
    data = array(map(lambda x: x.split("\t"), fin.readlines())).astype(float)
    fin.close()
    X = data[:,0]
    Y = data[:,1]
    Z = data[:,2]
    T = data[:,3]
    
    return X, Y, Z, T

def readErr(sat, obs):
    fin = open(sat)
    data = array(map(lambda x: x.split("\t"), fin.readlines())).astype(float)
    fin.close()
    Xer = data[:,0]
    Yer = data[:,1]
    Zer = data[:,2]
    
    fin = open(obs)
    data = array(map(lambda x: x.split("\t"), fin.readlines())).astype(float)
    fin.close()
    dS = data[:,0]
    
    return Xer, Yer, Zer, dS
    

def genErr(row, rng, filename):
    X = random.uniform(-rng, rng, size = row)
    Y = random.uniform(-rng, rng, size = row)
    Z = random.uniform(-rng, rng, size = row)

    fout = open(filename, "w")
    for i in range(row):
        fout.write("%.6f\t%.6f\t%.6f\n" % (X[i], Y[i], Z[i]))
        #fout.write("%.6f\n" % (X[i]))
    fout.close()
    
def lph2xyz(l, p, h, r):
    x = (r + h) * cos(p) * cos(l)
    y = (r + h) * cos(p) * sin(l)
    z = (r + h) * sin(p)
    return x, y, z

def addErr(pp, lp, hp, X, Y, Z, T, r, saterr, rngerr):
    xp, yp, zp = lph2xyz(lp, pp, hp, r)
    
    Xer, Yer, Zer, dS = readErr(saterr, rngerr)
    
    #Xer = Xer - Xer
    #Yer = Yer - Yer
    #Zer = Zer - Zer
    #dS = dS - dS
    
    #New sat coordinates have 1 meter error in x y z direction
    Xs = X + Xer
    Ys = Y + Yer
    Zs = Z + Zer
    
    S = sqrt((X - xp)**2 + (Y - yp)**2 + (Z - zp)**2)
    #New range have 20 centimeter error
    Sr = S + dS
    

    
    #fout = open("result1.txt", "w")
    #fout.write("Obs_ID\tS (m)\tSr (m)\tXs (m)\tYs (m)\tZs (m)\n")
    #for i in range(len(X)):
        #fout.write("OBS%02d\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n" % (i + 1, S[i], Sr[i], Xs[i], Ys[i], Zs[i]))
    #fout.close()
        
    return Xs, Ys, Zs, S, Sr        
        
    
    
    #fig = plt.figure("test")
    #ax = fig.add_subplot(111, projection="3d")
    #ax.plot(append(X, xp), append(Y, yp), append(Z, zp), 'r*')
    #ax.plot(Xs, Ys, Zs, 'b*')
    #plt.show()
    
def getRecv(Xs, Ys, Zs, S, Sr, pp, lp, hp, r):
    x0, y0, z0 = lph2xyz(lp, pp, hp, r)
    x1 = x0
    y1 = y0
    z1 = z0
    while True:
        S = sqrt((Xs - x1)**2 + (Ys - y1)**2 + (Zs - z1)**2)
        L = matrix([Sr - S]).T
        A = matrix([(x1 - Xs) / S, (y1 - Ys) / S, (z1 - Zs) / S]).T
        X = (A.T * A).I * (A.T * L)
        x1 += X[0,0]
        y1 += X[1,0]
        z1 += X[2,0]
        if abs(X.sum()) < 10**-8:
            break
    V = array(A * X - L)
    Sig = sqrt((V.T).dot(V)[0, 0] / (len(Xs) - 1))
    Qxx = array((A.T * A).I)
    
    J = matrix([[-sin(pp) * cos(lp), -sin(pp) * sin(lp), cos(pp)], [-sin(lp), cos(lp), 0], [cos(pp) * cos(lp), cos(pp) * sin(lp), sin(pp)]])
    Qenu = (J * Qxx * J.T)

    trueError = sqrt((x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2)
    PDOP = sqrt(Qenu[0, 0] + Qenu[1, 1] + Qenu[2, 2])
    VDOP = sqrt(Qenu[2, 2])
    HDOP = sqrt(Qenu[0, 0] + Qenu[1, 1])

    #print x1, y1, z1, Sig, PDOP, VDOP, HDOP, trueError
    return x1, y1, z1, Sig, PDOP, VDOP, HDOP, trueError, Qxx

def addErr2(pp, lp, hp, X, Y, Z, T, r, Xer, Yer, Zer, dS):
    xp, yp, zp = lph2xyz(lp, pp, hp, r)
    Xs = X + Xer
    Ys = Y + Yer
    Zs = Z + Zer
    
    S = sqrt((X - xp)**2 + (Y - yp)**2 + (Z - zp)**2)
    #New range have 20 centimeter error
    Sr = S + dS
    
    return Xs, Ys, Zs, S, Sr

def getBaseLine():
    X, Y, Z, T = readData("Intersection.txt")
    
    fin = open("Isat_err.txt")
    data = array(map(lambda x: x.split("\t"), fin.readlines())).astype(float)
    fin.close()
    Xer = data[:,0]
    Yer = data[:,1]
    Zer = data[:,2]
    
    fin = open("Irng_err.txt")
    data = array(map(lambda x: x.split("\t"), fin.readlines())).astype(float)
    fin.close()
    dS1 = data[:,0]
    
    fin = open("Irng_err2.txt")
    data = array(map(lambda x: x.split("\t"), fin.readlines())).astype(float)
    fin.close()
    dS2 = data[:,0]
    
    #Xer = Xer - Xer
    #Yer = Yer - Yer
    #Zer = Zer - Zer
    #dS1 = dS1*5# - dS1
    #dS2 = dS2*5# - dS2
    
    
    #use tokyo for observer station
    Tp = radians(35 + 41.0 / 60 + 22.4 / 3600)
    Tl = radians(139 + 41.0 / 60 + 30.2 / 3600)
    Th = 0.0
    
    #use osaka for another observer station
    Op = radians(34 + 41.0 / 60 + 37.5 / 3600)
    Ol = radians(135 + 30.0 / 60 + 7.6 / 3600)
    Oh = 0.0
    
    index = []
    for i in range(len(T)):
        if i % 9 == 0:
            tmp = []
            for j in range(9):
                tmp.append(i + j)
            index.append(tmp)
    index = array(index).T
    #x1, y1, z1 = lph2xyz(Tl, Tp, Th, R)
    #x2, y2, z2 = lph2xyz(Ol, Op, Oh, R)
    #trueBaseline = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    #fig = plt.figure("test")
    #ax = fig.add_subplot(111, projection="3d")
    controlPoints = []
    for _class in index:
        tmp = []
        for i in _class:
            tmp.append([X[i], Y[i], Z[i], T[i], Xer[i], Yer[i], Zer[i], dS1[i], dS2[i]])
        #ax.plot(array(tmp)[:,0], array(tmp)[:,1], array(tmp)[:,2], '*')
        Xs1, Ys1, Zs1, S1, Sr1 = addErr2(Tp, Tl, Th, array(tmp)[:,0], array(tmp)[:,1], array(tmp)[:,2], array(tmp)[:,3], R, array(tmp)[:,4], array(tmp)[:,5], array(tmp)[:,6], array(tmp)[:,7])
        x1, y1, z1, Sig1, PDOP1, VDOP1, HDOP1, trueError1, Qxx1  = getRecv(Xs1, Ys1, Zs1, S1, Sr1, Tp, Tl, Th, R)
        Xs2, Ys2, Zs2, S2, Sr2 = addErr2(Op, Ol, Oh, array(tmp)[:,0], array(tmp)[:,1], array(tmp)[:,2], array(tmp)[:,3], R, array(tmp)[:,4], array(tmp)[:,5], array(tmp)[:,6], array(tmp)[:,8])
        x2, y2, z2, Sig2, PDOP2, VDOP2, HDOP2, trueError2, Qxx2 = getRecv(Xs2, Ys2, Zs2, S2, Sr2, Op, Ol, Oh, R)
        #print x1, y1, z1, Sig1, PDOP1, VDOP1, HDOP1, Sig1 * PDOP1, Sig1 * VDOP1, Sig1 * HDOP1, trueError1
        #print x2, y2, z2, Sig2, PDOP2, VDOP2, HDOP2, Sig2 * PDOP2, Sig2 * VDOP2, Sig2 * HDOP2, trueError2
        #print x2 - x1, y2 - y1, z2 - z1, sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2), sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) - trueBaseline, trueBaseline 
        #print sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) - trueBaseline
        controlPoints.append([x1, y1, z1, x2, y2, z2])
    X1 = array(controlPoints)[:,0]
    Y1 = array(controlPoints)[:,1]
    Z1 = array(controlPoints)[:,2]
    X2 = array(controlPoints)[:,3]
    Y2 = array(controlPoints)[:,4]
    Z2 = array(controlPoints)[:,5]
    
    
    x1, y1, z1 = lph2xyz(Tl, Tp, Th, R)
    x2, y2, z2 = lph2xyz(Ol, Op, Oh, R)
    
    BaseLineStd = (sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)).std()
    estimatedBaseline = (sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)).mean()
    trueBaseline = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    #fig = plt.figure("Baseline error")
    #ax = fig.add_subplot(111)
    #formatter = ScalarFormatter(useOffset = False)
    #ax.xaxis.set_major_formatter(formatter)
    #ax.yaxis.set_major_formatter(formatter)
    #ax.set_title("Baseline error", size = 20)
    #T = array([x for x in range(9000, 33001, 2700)])
    #plt.xlabel("Time (sec)")
    #plt.ylabel("Baseline error (m)")
    
    #ax.plot(T, (sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)) - trueBaseline, 'r-')
    #plt.show()
    
    return trueBaseline, estimatedBaseline, BaseLineStd
    

    
def main():
    #use tokyo for observer station
    Tp = radians(35 + 41.0 / 60 + 22.4 / 3600)
    Tl = radians(139 + 41.0 / 60 + 30.2 / 3600)
    Th = 0.0
    
    #use osaka for another observer station
    Op = radians(34 + 41.0 / 60 + 37.5 / 3600)
    Ol = radians(135 + 30.0 / 60 + 7.6 / 3600)
    Oh = 0.0
    
    #return
    X, Y, Z, T = readData("visible_sat.txt")    
    Xs1, Ys1, Zs1, S1, Sr1 = addErr(Tp, Tl, Th, X, Y, Z, T, R, "sat_err.txt", "rng_err.txt")
    x1, y1, z1, Sig1, PDOP1, VDOP1, HDOP1, trueError1, Qxx1 = getRecv(Xs1, Ys1, Zs1, S1, Sr1, Tp, Tl, Th, R)
    
    X, Y, Z, T = readData("visible_sat2.txt")
    Xs2, Ys2, Zs2, S2, Sr2 = addErr(Op, Ol, Oh, X, Y, Z, T, R, "sat_err2.txt", "rng_err2.txt")
    x2, y2, z2, Sig2, PDOP2, VDOP2, HDOP2, trueError2, Qxx2 = getRecv(Xs2, Ys2, Zs2, S2, Sr2, Op, Ol, Oh, R)
    
    #print x1, y1, z1, Sig1, PDOP1, VDOP1, HDOP1, Sig1 * PDOP1, Sig1 * VDOP1, Sig1 * HDOP1, trueError1
    #print x2, y2, z2, Sig2, PDOP2, VDOP2, HDOP2, Sig2 * PDOP2, Sig2 * VDOP2, Sig2 * HDOP2, trueError2
    
    trueBaseline, estimatedBaseline, BaseLineStd = getBaseLine()
    print estimatedBaseline - trueBaseline
    #print sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    #X1, Y1, Z1 = lph2xyz(Tl, Tp, Th, R)
    #X2, Y2, Z2 = lph2xyz(Ol, Op, Oh, R)
    
    #print sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)
    #print sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2) - sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    #genErr(len(X), 1, "sat_err.txt")
    #genErr(len(X), 0.2, "rng_err.txt")
    
    return 0

if __name__ == "__main__":
    main()

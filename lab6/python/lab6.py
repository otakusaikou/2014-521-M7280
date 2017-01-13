"""
Created on 2014/04/20

@author: otakusaikou1
"""
from numpy import sin, cos, matrix, array, pi, radians, sqrt, arctan2, degrees, around, zeros
from mpl_toolkits.mplot3d import Axes3D, proj3d
import matplotlib.pyplot as plt
import time
import datetime

DEBUG = True
ST_SEC = 86164.09053

def readData(filename, PRN):
    fin = open(filename, "r")
    year = []
    mon = []
    day = []
    h = []
    m = []
    x = []
    y = []
    z = []
    for line in fin.readlines():
        if line.startswith("*"):
            linesplit = line.split()
            year.append(int(linesplit[1]))
            mon.append(int(linesplit[2]))
            day.append(int(linesplit[3]))
            h.append(int(linesplit[4]))
            m.append(int(linesplit[5]))
        elif line.startswith(PRN):
            linesplit = line.split()
            x.append(float(linesplit[1]))
            y.append(float(linesplit[2]))
            z.append(float(linesplit[3]))
            
    return year, mon, day, h, m, x, y, z

def toDMS(deg):
    D = int(deg)
    if D == 0:
        M = int((deg - int(deg)) * 60)
    else:
        M = abs(int((deg - int(deg)) * 60))
        
    if D == 0 and M == 0:
        S = (deg - int(deg) - (1.0 * int((deg - int(deg)) * 60) / 60)) * 3600
    else:
        S = abs((deg - int(deg) - (1.0 * int((deg - int(deg)) * 60) / 60)) * 3600)
    return D, M, S

def getGST(t):
    GST0 = 6 * 60**2 + 37 * 60 + 7.7912
    t0 = 2454100.5 * 86400
    
    dt = (t - t0)
    omega = (360.0 / ST_SEC) * (86400 / 360.0)
    return (GST0 + omega * dt) % 86400

def xyz2XYZT(x, y, z):
    #Start from 2014/04/3 0:00:00, Julian Day is 2456750.5, time offset is 15 minutes, End with 2014/04/4 23:45:00
    ts = 2456750.5 * 86400
    tmpt = 2456750.5 * 86400
    offset = 15.0 * 60
    te = ts + offset * len(x)
    T = []
    X = []
    Y = []
    Z = []
    GST_DMS = []
    index = 0
    while tmpt < te:
        ans = getGST(tmpt)
        hms = toDMS(ans / 3600)
        GST_DMS.append((hms[0] * 60**2 + hms[1] * 60 + hms[2]) * (360.0 / 86400))
        #T.append(int((tmpt - ts) / 60))
        T.append(tmpt / 86400)
        Rz = matrix([[cos(radians(-GST_DMS[index])), sin(radians(-GST_DMS[index])), 0], [-sin(radians(-GST_DMS[index])), cos(radians(-GST_DMS[index])), 0], [0, 0, 1]])
        XYZ = array(Rz * matrix([[x[index]], [y[index]], [z[index]]]))
        X.append(XYZ[0][0])
        Y.append(XYZ[1][0])
        Z.append(XYZ[2][0])
        index += 1
        tmpt += offset
        
    return X, Y, Z, T

#x,y,z-l,p,h, default output unit is radius
def xyz2lph(x, y, z, r):
    L = []
    L0 = []
    P = []
    P0 = []
    H = []
    for i in range(len(x)):
        L.append(toDMS(degrees(arctan2(y[i], x[i]))))
        L0.append(degrees(arctan2(y[i], x[i])))
        P.append(toDMS(degrees(arctan2(z[i], (sqrt(x[i]**2 + y[i]**2))))))
        P0.append(degrees(arctan2(z[i], (sqrt(x[i]**2 + y[i]**2)))))
        H.append(sqrt(x[i]**2 + y[i]**2 + z[i]**2) - r)

    return L, P, H, L0, P0
    

def drawScatter(x, y, z, fig, xlabel = "x (km)", ylabel = "y (km)", zlabel = "z (km)", title = "ECEF Frames"):
    fig = plt.figure(fig)
    ax = fig.add_subplot(111, projection="3d")
    #ax.scatter(x[1:-1], y[1:-1], z[1:-1], c = "b", marker = "*")
    #ax.scatter(x[0], y[0], z[0], c = "r", marker = "^")
    #ax.scatter(x[-1], y[-1], z[-1], c = "g", marker = "v")
    
    #Days
    #ax.scatter(x[:96], y[:96], z[:96], c = "b", marker = "^")
    #ax.scatter(x[96:], y[96:], z[96:], c = "g", marker = "v")
    
    #Days2
    ax.plot(x[:48], y[:48], z[:48], "8", color = "b", label = "4/3 00:00~4/3 11:45")
    ax.plot(x[48:96], y[48:96], z[48:96], ">", color = "c", label = "4/3 12:00~4/3 23:45")
    ax.plot(x[96:144], y[96:144], z[96:144], "s", color = "r", label = "4/4 00:00~4/4 11:45")
    ax.plot(x[144:192], y[144:192], z[144:192], "D", color = "y", label = "4/4 12:00~4/4 23:45")
    #ax.legend(loc = 4, numpoints=1, ncol = 1)
    
    #test
    #to xy
    #ax.plot(x[:48], y[:48], zeros(48), "8", color = "b", label = "4/3 00:00~4/3 11:45")
    #ax.plot(x[48:96], y[48:96], zeros(48), ">", color = "c", label = "4/3 12:00~4/3 23:45")
    #ax.plot(x[96:144], y[96:144], zeros(48), "s", color = "r", label = "4/4 00:00~4/4 11:45")
    #ax.plot(x[144:192], y[144:192], zeros(48), "D", color = "y", label = "4/4 12:00~4/4 23:45")
    #to xz
    #ax.plot(x[:48], zeros(48), z[:48], "8", color = "b", label = "4/3 00:00~4/3 11:45")
    #ax.plot(x[48:96], zeros(48), z[48:96], ">", color = "c", label = "4/3 12:00~4/3 23:45")
    #ax.plot(x[96:144], zeros(48), z[96:144], "s", color = "r", label = "4/4 00:00~4/4 11:45")
    #ax.plot(x[144:192], zeros(48), z[144:192], "D", color = "y", label = "4/4 12:00~4/4 23:45")
    #to yz
    #ax.plot(zeros(48), y[:48], z[:48], "8", color = "b", label = "4/3 00:00~4/3 11:45")
    #ax.plot(zeros(48), y[48:96], z[48:96], ">", color = "c", label = "4/3 12:00~4/3 23:45")
    #ax.plot(zeros(48), y[96:144], z[96:144], "s", color = "r", label = "4/4 00:00~4/4 11:45")
    #ax.plot(zeros(48), y[144:192], z[144:192], "D", color = "y", label = "4/4 12:00~4/4 23:45")
    
    ax.legend(loc = 4, numpoints=1, ncol = 1)
    
    ax.set_xlabel(xlabel, fontsize = 15)
    ax.set_ylabel(ylabel, fontsize = 15)
    ax.set_zlabel(zlabel, fontsize = 15)
    plt.title(title, size=25)
    
def draw2Dmap(year, mon, day, h, m, T, L0, P0, H, fig, x, y, z):
    T = around(((array(T) % 2456750.5) * 24 * 60), 0)

    fig = plt.figure(fig)
    ax = fig.add_subplot(211)
    plt.title("Longitude&Latitude", size=25)
    ax.plot(T, L0)
    ax.plot(T, P0)
    ax.annotate("Longuitude", xy=(T[-1], L0[-1]), 
        xytext=(-50, 70), textcoords="offset points", va="center",
        size=15, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate("Latitude", xy=(T[-1], P0[-1]), 
        xytext=(-50, -70), textcoords="offset points", va="center",
        size=15, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(year[0], mon[0], day[0], h[0], m[0], 0)), xy=(T[0], -200), 
        xytext=(10, 60), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(year[100], mon[100], day[100], h[100], m[100], 0)), xy=(T[100], -200), 
        xytext=(10, 60), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(year[191], mon[191], day[191], h[191], m[191], 0)), xy=(T[191], -200), 
        xytext=(-100, 25), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.set_xlabel("Time (min)", fontsize = 15)
    ax.set_ylabel("Values (deg)", fontsize = 15)
    
    ax = fig.add_subplot(212)
    plt.title("Height", size=25)
    ax.plot(T, H)
    ax.annotate("Height", xy=(T[-1], H[-1]), 
        xytext=(-50, -50), textcoords="offset points", va="center",
        size=15, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(year[0], mon[0], day[0], h[0], m[0], 0)), xy=(T[0], 19900), 
        xytext=(10, 25), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(year[100], mon[100], day[100], h[100], m[100], 0)), xy=(T[100], 19900), 
        xytext=(10, 25), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(year[191], mon[191], day[191], h[191], m[191], 0)), xy=(T[191], 19900), 
        xytext=(-100, 25), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    """
    dxyz = []
    for i in range(len(x) - 1):
        dxyz.append(sqrt((x[i] - x[i + 1])**2 + (y[i] - y[i + 1])**2 + (z[i] - z[i + 1])**2))
    
    dxyz = array(dxyz) - sum(dxyz) / len(dxyz) 
    ax = fig.add_subplot(111)
    ax.plot(T[1:], dxyz)
    
    ax.annotate("dxyz", xy=(T[-1], dxyz[-1]), 
        xytext=(-50, 50), textcoords="offset points", va="center",
        size=15, 
        arrowprops=dict(arrowstyle="->"))"""
    
    
    ax.set_xlabel("Time (min)", fontsize = 15)
    ax.set_ylabel("Values (km)", fontsize = 15)
    
    
def main():
    #define PRN name
    PRN = "PG31"
    
    #define radius of earth
    r = 6371.0
    
    filename = "igs17864.sp3"
    year, mon, day, h, m, x, y, z = readData(filename, PRN)
    
    filename = "igs17865.sp3"
    year2, mon2, day2, h2, m2, x2, y2, z2 = readData(filename, PRN)
    
    year += year2
    mon += mon2
    day += day2
    h += h2
    m += m2
    x += x2
    y += y2
    z += z2
    
    
    drawScatter(x, y, z, 0)
    X, Y, Z, T = xyz2XYZT(x, y, z)

    drawScatter(X, Y, Z, 1, title = "Quasi-Inertial Frames")
    L, P, H, L0, P0 = xyz2lph(x, y, z, r)
    
    #draw2Dmap(year, mon, day, h, m, T, L0, P0, H, "Longitude&Latitude&Height", x, y, z)
    
    #drawScatter(X+x, Y+y, Z+z, 3)
    plt.show()
    
    
    #result1
    fout = open("result.txt", "w")
    fout.write("Time(YYYY-MM-DD HH:MM:SS)\tJD(day)\tPRN\tXin(km)\tYin(km)\tZin(km)\tx(km)\ty(km)\tz(km)\n")
    #print "Time(YYYY-MM-DD HH:MM:SS)\tJD(day)\tPRN\tXin(km)\tYin(km)\tZin(km)\tx(km)\ty(km)\tz(km)"
    for i in range(len(x)):
        fout.write("%04d-%02d-%02d %02d:%02d:00\t%.8f\t%s\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n" % (year[i], mon[i], day[i], h[i], m[i], T[i], PRN, X[i], Y[i], Z[i], x[i], y[i], z[i]))
        #print "%04d-%02d-%02d %02d:%02d:00\t%.8f\t%s\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f" % (year[i], mon[i], day[i], h[i], m[i], T[i], PRN, X[i], Y[i], Z[i], x[i], y[i], z[i]) 
    fout.close()

    #result2
    fout = open("result2.txt", "w")
    fout.write("Time(YYYY-MM-DD HH:MM:SS)\tJD(day)\tlon(deg)\tlon(min)\tlon(sec)\tlat(deg)\tlat(min)\tlat(sec)\tH(km)\n")
    #print "Time(YYYY-MM-DD HH:MM:SS)\tJD(day)\tlon(deg)\tlon(min)\tlon(sec)\tlat(deg)\tlat(min)\tlat(sec)\n"
    for i in range(len(x)):
        fout.write("%04d-%02d-%02d %02d:%02d:00\t%.8f\t%d\t%d\t%.6f\t%d\t%d\t%.6f\t%.6f\n" % (year[i], mon[i], day[i], h[i], m[i], T[i], L[i][0], L[i][1], L[i][2], P[i][0], P[i][1], P[i][2], H[i]))
        #print "%04d-%02d-%02d %02d:%02d:00\t%.8f\t%d\t%d\t%.6f\t%d\t%d\t%.6f\t%.6f\n" % (year[i], mon[i], day[i], h[i], m[i], T[i], L[i][0], L[i][1], L[i][2], P[i][0], P[i][1], P[i][2], H[i]) 
    fout.close()
    return 0
    
if __name__ == "__main__":
    main()
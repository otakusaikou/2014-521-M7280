'''
Created on 2014/05/04

@author: otakusaikou1
'''
from numpy import sin, cos, matrix, array, pi, radians, sqrt, tan, arctan, arctan2, degrees, around, zeros
from mpl_toolkits.mplot3d import Axes3D, proj3d
from matplotlib.ticker import ScalarFormatter 
import matplotlib.pyplot as plt
import time
import datetime

DEBUG = True
ST_SEC = 86164.09053
#ST_SEC = 86164.09053083288

#This function convert degrees to degrees-minute-second format
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

#This function calculate Greenwich Sideral Time, using initial GST of 2006/12/31 00:00:00(Julian Day is 2454100.5) as GST0
def getGST(t):
    GST0 = 6 * 60**2 + 37 * 60 + 7.7912
    t0 = 2454100.5 * 86400
    
    dt = (t - t0)
    omega = (360.0 / ST_SEC) * (86400 / 360.0)
    return (GST0 + omega * dt) % 86400

#This function read YUMA data with file name and satellite ID
def readFile(fileName, id):
    fin = open(fileName, "r")
    #Split and store every lines to list lines 
    lines = [line.split() for line in fin.readlines()]
    fin.close()
    for i in range(1, len(lines), 15):
        if id == lines[i][-1]:
            data = lines[i:i + 13]
            break
    
    #Get kepler six elements
    e0 = float(data[2][-1]) #Eccentricity of satellite orbit
    toa = float(data[3][-1]) #Time of Applicability (second start from gps week)
    I = float(data[4][-1]) #Obital Incilination 
    omegadot = float(data[5][-1]) #Rate of right ascen
    a = float(data[6][-1])**2 #Length of major-axis of satellite orbit
    aw = float(data[7][-1]) #Right ascen at week (angle between ECEF x-axis and satellite ascending node)
    lOmega = float(data[8][-1]) #Argument of perigee (little omega)
    mt0 = float(data[9][-1]) #Mean anomaly of toa
    
    return e0, toa, I, omegadot, a, aw, lOmega, mt0

#This function calculate eccentric argument of perigee
def getE(e0, toa, a, mt0, t):
    #Define constants
    GM = 398600441800000.0
       
    #Get eccentric argument of perigee
    n0 = sqrt(GM / a**3) #Mean motion of satellite
    mt = mt0 + (t - toa) * n0 #Get mean anomaly at t second with given mean anomaly and mean motion of satellite 
    
    E0 = mt
    E1 = E0 - ((E0 - e0 * sin(E0) - mt) / (1 - e0 * cos(E0)))
    
    #Numerical solution
    while abs(E0 - E1) > 10**-12:
        E0 = E1
        E1 = E0 - ((E0 - e0 * sin(E0) - mt) / (1 - e0 * cos(E0)))
    return E1 % (2 * pi)

#This function convert ECEF Cartesian coordinates to ECEF spherical frame
def xyz2lph(x, y, z, r):
    l = arctan2(y, x);
    p = arctan2(z, sqrt(x**2 + y**2));
    h = sqrt(x**2 + y**2 + z**2) - r;
    return l, p, h

#This function can draw 2D map with longitude,latitude and height list 
def draw2Dmap(T, l, p, h, figname):

    fig = plt.figure(figname)
    ax = fig.add_subplot(211)
    plt.title("Longitude&Latitude", size=25)
    ax.plot(T, l)
    ax.plot(T, p)
    ax.annotate("Longuitude", xy=(T[-20], l[-20]), 
        xytext=(-70, 70), textcoords="offset points", va="center",
        size=15, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate("Latitude", xy=(T[-20], p[-20]), 
        xytext=(-40, -70), textcoords="offset points", va="center",
        size=15, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(2014, 5, 4, 0, 0, 0)), xy=(T[0], -200), 
        xytext=(10, 25), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(2014, 5, 5, 0, 0, 0)), xy=(T[288], -200), 
        xytext=(10, 25), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(2014, 5, 6, 0, 0, 0)), xy=(T[576], -200), 
        xytext=(-200, 20), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.set_xlabel("Time (sec)", fontsize = 15)
    ax.set_ylabel("Values (deg)", fontsize = 15)
    
    ax = fig.add_subplot(212)
    plt.title("Height", size=25)
    ax.plot(T, h)
    ax.annotate("Height", xy=(T[-1], h[-1]), 
        xytext=(-50, -20), textcoords="offset points", va="center",
        size=15, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(2014, 5, 4, 0, 0, 0)), xy=(T[0], 1.99*10**7), 
        xytext=(10, 25), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))

    ax.annotate(str(datetime.datetime(2014, 5, 5, 0, 0, 0)), xy=(T[288], 1.99*10**7), 
        xytext=(10, 25), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(str(datetime.datetime(2014, 5, 6, 0, 0, 0)), xy=(T[576], 1.99*10**7), 
        xytext=(-200, 20), textcoords="offset points", va="center",
        size=13, 
        arrowprops=dict(arrowstyle="->"))
    
    #formatter = ScalarFormatter()
    #formatter.set_scientific(False)
    #formatter.set_useOffset(10800)
    #ax.xaxis.set_major_formatter(formatter)

    ax.set_xlabel("Time (sec)", fontsize = 15)
    ax.set_ylabel("Values (m)", fontsize = 15)
    
def drawScatter(x, y, z, fig, xlabel = "x (m)", ylabel = "y (m)", zlabel = "z (m)", title = "ECEF Frames"):
    fig = plt.figure(fig)
    ax = fig.add_subplot(111, projection="3d")

    #Day1
    #ax.plot([x[0]], [y[0]], [z[0]], "*", color = "r", ms = 15, label = "Start")
    #ax.plot(x[1:145], y[1:145], z[1:145], "8", color = "b", label = "5/4 00:00~5/4 12:00")
    #ax.plot(x[145:288], y[145:288], z[145:288], ">", color = "c", label = "5/4 12:05~5/4 24:00")
    #ax.plot([x[288]], [y[288]], [z[288]], "*", color = "g", ms = 15, label = "End")
    #Day2
    ax.plot([x[289]], [y[289]], [z[289]], "*", color = "r", ms = 15, label = "Start")
    ax.plot(x[290:433], y[290:433], z[290:433], "s", color = "r", label = "5/5 00:05~5/5 12:00")
    ax.plot(x[433:576], y[433:576], z[433:576], "D", color = "y", label = "5/5 12:05~5/5 24:00")
    ax.plot([x[576]], [y[576]], [z[576]], "*", color = "g", ms = 15, label = "End")

    ax.legend(loc = 4, numpoints=1, ncol = 1)
    
    ax.set_xlabel(xlabel, fontsize = 15)
    ax.set_ylabel(ylabel, fontsize = 15)
    ax.set_zlabel(zlabel, fontsize = 15)
    
    plt.title(title, size=25)
    
    
#This function calculate ECEF coordinates from YUMA file
def getECEF(e0, toa, I, omegadot, a, aw, lOmega, mt0):
    #ECEF frame
    x = []
    y = []
    z = []
    
    #Inertial frame
    XIN = []
    YIN = []
    ZIN = []
    
    #ECEF Spherical frame
    l = []
    p = []
    h = []
    L = []
    P = []
    H = []
    
    #Time
    T = []
    
    #The rotation rate of earth
    omegae = pi * 2 / ST_SEC
    r = 6371000.0
    
    for t in range(0, 172801, 300):
        #Get current Geodetic longitude of satellite
        omega = aw + omegadot * (t - toa) - omegae * t
        
        #Get eccentric argument of perigee
        E = getE(e0, toa, a, mt0, t)
        #Get true anomaly of satellite
        #thetadot = arctan2((sqrt(1 + e0**2) * sin(E)), (cos(E) - e0))
        thetadot = 2 * arctan(sqrt((1 + e0) / (1 - e0)) * tan(E / 2))

        #Coordinates in 2D satellite-earth coordinate system
        Xw = a * cos(E) - a * e0
        Yw = a * sqrt(1 - e0**2) * sin(E)
        Zw = 0
        
        #Get GST at t second
        ans = getGST(2451412.5 * 86400 + 767 * 7 * 86400 + t)
        hms = toDMS(ans / 3600)
        GST = radians((hms[0] * 60**2 + hms[1] * 60 + hms[2]) * (360.0 / 86400))
        
        
        #Rotation matrix
        Rz = matrix([[cos(-lOmega), sin(-lOmega), 0], [-sin(-lOmega), cos(-lOmega), 0], [0, 0, 1]])
        Rx = matrix([[1, 0, 0], [0, cos(-I), sin(-I)], [0, -sin(-I), cos(-I)]])
        Rz2 = matrix([[cos(-omega), sin(-omega), 0], [-sin(-omega), cos(-omega), 0], [0, 0, 1]])
        Rz3 = matrix([[cos(-GST), sin(-GST), 0], [-sin(-GST), cos(-GST), 0], [0, 0, 1]])

        X = matrix([[Xw], [Yw], [Zw]])
        ECEF = Rz2 * Rx * Rz * X
        IN = Rz3 * ECEF
        lph = xyz2lph(array(ECEF)[0][0], array(ECEF)[1][0], array(ECEF)[2][0], r)
        
        x.append(array(ECEF)[0][0])
        y.append(array(ECEF)[1][0])
        z.append(array(ECEF)[2][0])
        XIN.append(array(IN)[0][0])
        YIN.append(array(IN)[1][0])
        ZIN.append(array(IN)[2][0])
        l.append(toDMS(degrees(lph[0])))
        p.append(toDMS(degrees(lph[1])))
        h.append(lph[2])
        L.append(degrees(lph[0]))
        P.append(degrees(lph[1]))
        H.append(lph[2])
        
        T.append(t)
        
    drawScatter(x, y, z, "figure1")
    drawScatter(XIN, YIN, ZIN, "figure2", title = "Quasi-Inertial Frames")
    draw2Dmap(T, L, P, H, "figure3")
    plt.show()
    
    
    #result1
    fout = open("result.txt", "w")
    fout.write("Time(sec)\tXin(m)\tYin(m)\tZin(m)\tx(m)\ty(m)\tz(m)\n")
    #fout.write("Time(sec)\tXin(m)\tYin(m)\tZin(m)\tx(m)\ty(m)\tz(m)\tXin2(m)\tYin2(m)\tZin2(m)\n")
    for i in range(len(x)):
        #fout.write("%d\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n" % (T[i], XIN[i], YIN[i], ZIN[i], x[i], y[i], z[i], XIN2[i], YIN2[i], ZIN2[i]))
        fout.write("%d\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n" % (T[i], XIN[i], YIN[i], ZIN[i], x[i], y[i], z[i]))
    fout.close()
    
    #result2
    fout = open("result2.txt", "w")
    fout.write("Time(sec)\tlon(deg)\tlon(min)\tlon(sec)\tlat(deg)\tlat(min)\tlat(sec)\tH(m)\n")
    for i in range(len(x)):
        fout.write("%d\t%d\t%d\t%.6f\t%d\t%d\t%.6f\t%.6f\n" % (T[i], l[i][0], l[i][1], l[i][2], p[i][0], p[i][1], p[i][2], h[i]))
    fout.close()
    return 0
    
    
    
    
         
def main():
    #Define YUMA file name, referenced from http://www.navcen.uscg.gov/?pageName=gpsAlmanacs
    #Week number 767 stand from weeks start from 22 Aug 1999 00:00:00 (Julian day is 2451412.5)
    yumaFile = "current.alm"
    
    #Satellite ID
    id = "31"

    e0, toa, I, omegadot, a, aw, lOmega, mt0 = readFile(yumaFile, id)    
    getECEF(e0, toa, I, omegadot, a, aw, lOmega, mt0)
    
    return 0

if __name__ == '__main__':
    main()
"""
Created on 2014/05/19

@author: otakusaikou1
"""
from numpy import sin, cos, matrix, array, pi, radians, sqrt, tan, arctan2, degrees, around, zeros, set_printoptions, log
from matplotlib.ticker import ScalarFormatter 
import matplotlib.pyplot as plt

#disable scientific notation
set_printoptions(suppress=True)

#set constants
R = 6371000.0

#this function project latitude with mercator projection
def lat2y(lat):
    if lat > 89.5:
        lat = 89.5
    elif lat < -89.5:
        lat = -89.5
    
    return 180.0/pi*log(tan(pi/4.0+lat*(pi/180.0)/2.0))

#this function read and draw world land data
def drawPolygon(ax, method = "platte"):
    fin = open("COAST4.dat")
    lines = fin.readlines()
    
    polygons = []
    x = []
    y = []
    if method == "platte" or method == "platte2":
        for line in lines:
            if line.split()[0] == "3":
                if len(x) != 0:
                    polygons.append((x, y))
                    x = []
                    y = []
            x.append(float(line.split()[2]) / 100 / 0.6)
            y.append(float(line.split()[1]) / 100 / 0.6)
    else:
        for line in lines:
            if line.split()[0] == "3":
                if len(x) != 0:
                    polygons.append((x, y))
                    x = []
                    y = []
            x.append(float(line.split()[2]) / 100 / 0.6)
            y.append(lat2y(float(line.split()[1]) / 100 / 0.6))
        
    
    fin.close()
    polygons.append((x, y))
    
    
    threshold = 150
    for polygon in polygons:
        start = 0
        for i in range(len(polygon[0]) - 1):
            if sqrt((polygon[0][i] - polygon[0][i + 1])**2 + (polygon[1][i] - polygon[1][i + 1])**2) > threshold:
                plt.plot(polygon[0][start:i + 1], polygon[1][start:i + 1], c = 'g')
                start = i + 1
        if start == 0:
            ax.plot(polygon[0], polygon[1], c = 'g')

#this function read and draw line of longitude and latitude
def drawLonlat(ax, method = "platte"):
    fin = open("MERIPAR5.dat")
    lines = fin.readlines()
    
    x = []
    y = []
    if method == "platte" or method == "platte2":
        for line in lines:
            x.append(float(line.split()[2]) / 100 / 0.6)
            y.append(float(line.split()[1]) / 100 / 0.6)
    else:
        for line in lines:
            x.append(float(line.split()[2]) / 100 / 0.6)
            y.append(lat2y(float(line.split()[1]) / 100 / 0.6))
        
    
    fin.close()
    
    threshold = 150
    start = 0
    for i in range(len(x) - 1):
        if sqrt((x[i] - x[i + 1])**2 + (y[i] - y[i + 1])**2) > threshold:
            plt.plot(x[start:i + 1], y[start:i + 1], c = 'gray')
            start = i + 1
    if start == 0:
        ax.plot(x, y, c = 'gray')
        
#this function convert ECEF Cartesian coordinates to ECEF spherical frame
def ECEF2lph(ECEF, r, method = "platte"):
    l = array(map(lambda x: degrees(arctan2(x[1], x[0])), ECEF[:,:2]))
    p = array(map(lambda x: degrees(arctan2(x[2], sqrt(x[0]**2 + x[1]**2))), ECEF))
    h = array(map(lambda x: sqrt(x[0]**2 + x[1]**2 + x[2]**2) - r, ECEF))
    if method == "mercator" or method == "mercator2":
        p = array(map(lat2y, p))
        
    return l, p, h 
            
#this function read ECEF coordinates from result.txt which is the result of lab7
def readECEF():
    fin = open("result.txt")
    data = fin.readlines()[1:]
    ECEF = array(map(lambda x: map(float, (x.split()[-3:])), data))
    T = array(map(lambda x: int(x.split()[0]), data))
    fin.close()
    
    return ECEF, T

#this function convert ECEF CRS to Azimuth and Zenith
def xyz2tr(T, ECEF, lp, pp, hp, r):
    xp = (r + hp) * cos(pp) * cos(lp)
    yp = (r + hp) * cos(pp) * sin(lp)
    zp = (r + hp) * sin(pp)
    
    Ry = matrix([[cos((pi / 2) - pp), 0, -sin((pi / 2) - pp)], [0, 1, 0], [sin((pi / 2) - pp), 0, cos((pi / 2) - pp)]])
    Rz = matrix([[cos(lp), sin(lp), 0], [-sin(lp), cos(lp), 0], [0, 0, 1]])
    
    X = array(map(lambda x: matrix([x[0] - xp, x[1] - yp, x[2] - zp]).T, ECEF))
    Ans = array(map(lambda x: array(Ry * Rz * x), X)).T
    N = -Ans[0, 0]    
    E = Ans[0, 1]    
    U = Ans[0, 2] 
    
    Az = arctan2(E, N)
    El = arctan2(U, sqrt(E**2 + N**2))
    Zenith = degrees((pi / 2) - El)
    
    theta = []
    radius = []
    T2 = []
    for i in range(len(Zenith)):
        if Zenith[i] >= 0 and Zenith[i] <= 80:
            theta.append(Az[i])
            radius.append(Zenith[i])
            T2.append(T[i])
        
    return theta, radius, T2

#this function draw satellite track
def drawSat(ax, method = "platte", lp = None, pp = None, hp = None):
    ECEF, T = readECEF()
    l, p, h = ECEF2lph(ECEF, R, method)
    T = list(T)
    
    y = p
    x = l
    if method == "platte2" or method == "mercator2":
        theta, radius, T2 = xyz2tr(T, ECEF, lp, pp, hp, R)
        intersection = list(set(T).intersection(set(T2)))
        difference = list(set(T).difference((set(T2))))
        intersection.sort()
        difference.sort()
        vis = map(lambda x: T.index(x), intersection)
        invis = map(lambda x: T.index(x), difference)
        
        for i in vis:
            ax.plot(x[i], y[i], 'b*')
        for i in invis:
            ax.plot(x[i], y[i], 'r^')
        if method == "platte2":
            ax.plot(degrees(lp), degrees(pp), 'ro')
            ax.annotate("Station", xy=(degrees(lp), degrees(pp)), 
                        xytext=(-25, -40), textcoords="offset points", va="center",
                        size=15, 
                        arrowprops=dict(arrowstyle="->"))
        else:
            ax.plot(degrees(lp), lat2y(degrees(pp)), 'ro')
            ax.annotate("Station", xy=(degrees(lp), lat2y(degrees(pp))), 
                        xytext=(-25, -40), textcoords="offset points", va="center",
                        size=15, 
                        arrowprops=dict(arrowstyle="->"))
    else:
        ax.plot(x, y, 'r*')
        
    for i in range(len(x)):
        if (T[i] % 3600) == 0:
            if (T[i] == 86400):
                pass
            else:
                ax.annotate("%02d" % ((T[i] / 3600 + 10) % 24), xy=(x[i], y[i]), 
                            xytext=(20, -30), textcoords="offset points", va="center",
                            size=15, 
                            arrowprops=dict(arrowstyle="->"))
    
#this function draw math with input projection methods
def drawMap(figname, method = "platte", lp = None, pp = None, hp = None):
    #plot settings for figure1
    fig = plt.figure(figname)
    ax = fig.add_subplot(111)
    ax.axis('equal')
    ax.set_title(figname, size = 20)
    plt.xlabel("x (deg)")
    plt.ylabel("y (deg)")
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    
    if method == "mercator" or method == "mercator2":
        plt.ylim(-90, 90)
    else:
        plt.xlim(-190, 190)
    
    #disable scientific notation of scale
    plt.yticks(range(-150, 151, 15))
    plt.xticks(range(-195, 196, 15))
    ax.set_yticklabels(map(str, range(-150, 151, 15)), fontsize=15)
    ax.set_xticklabels(map(str, range(-195, 196, 15)), fontsize=15)
    plt.grid()
    
    drawPolygon(ax, method)
    drawLonlat(ax, method)
    drawSat(ax, method, lp, pp, hp)
    
#this function draw skyplot with input data
def drawSkyPlot(lp, pp, hp):
    ECEF, T = readECEF()
    theta, radius, T2 = xyz2tr(T, ECEF, lp, pp, hp, R)
    
    fig = plt.figure("Skyplot")
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 100)
    plt.yticks(range(0, 100, 30))
    ax.set_yticklabels(map(str, range(90, -1, -30)), fontsize=15)
    ax.set_title("Skyplot G31 2014/5/4", size = 20, loc = "Left")
    plt.xlabel("Azimuth")
    plt.ylabel("Zenith")
    ax.plot(theta, radius, "r*", label = "G31")
    ax.plot(theta, radius, "r-", label = "G31 Track")
    for i in range(len(theta)):
        if (T2[i] % 3600) == 0:
            ax.annotate("%02d" % ((T2[i] / 3600 + 10) % 24), xy=(theta[i], radius[i]), 
                        xytext=(-10, -30), textcoords="offset points", va="center",
                        size=15, 
                        arrowprops=dict(arrowstyle="->"))
    ax.legend(numpoints=1)
    
    
def xyz2tr2(T, ECEF, lp, pp, hp, r):
    xp = (r + hp) * cos(pp) * cos(lp)
    yp = (r + hp) * cos(pp) * sin(lp)
    zp = (r + hp) * sin(pp)
    
    Ry = matrix([[cos((pi / 2) - pp), 0, -sin((pi / 2) - pp)], [0, 1, 0], [sin((pi / 2) - pp), 0, cos((pi / 2) - pp)]])
    Rz = matrix([[cos(lp), sin(lp), 0], [-sin(lp), cos(lp), 0], [0, 0, 1]])
    
    X = array(map(lambda x: matrix([x[0] - xp, x[1] - yp, x[2] - zp]).T, ECEF))
    Ans = array(map(lambda x: array(Ry * Rz * x), X)).T
    N = -Ans[0, 0]    
    E = Ans[0, 1]    
    U = Ans[0, 2] 
    
    Az = arctan2(E, N)
    El = arctan2(U, sqrt(E**2 + N**2))
    Sr = sqrt(E**2 + N**2 + U**2)
    Zenith = degrees((pi / 2) - El)
    
    theta = []
    radius = []
    T2 = []
    for i in range(len(Zenith)):
        if Zenith[i] >= 0 and Zenith[i] <= 80:
            theta.append(Az[i])
            radius.append(Sr[i] * Zenith[i])
            T2.append(T[i])
        
    return theta, radius, T2

def drawNewSkyPlot1(lp, pp, hp):
    ECEF, T = readECEF()
    x, y, T2 = xyz2tr2(T, ECEF, lp, pp, hp, R)
    
    fig = plt.figure("New Skyplot")
    ax = fig.add_subplot(111, polar = True)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, max(y) + 500000000)
    
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(formatter)
    
    ax.set_title("Skyplot G31 2014/5/4", size = 20, loc = "Left")
    plt.xlabel("Azimuth")
    plt.ylabel("Sr * Zenith")
    ax.plot(x, y, "r*", label = "G31")
    ax.plot(x, y, "r-", label = "G31 Track")
    
    for i in range(len(x)):
        if (T2[i] % 3600) == 0:
            ax.annotate("%02d" % ((T2[i] / 3600 + 10) % 24), xy=(x[i], y[i]), 
                        xytext=(-10, -30), textcoords="offset points", va="center",
                        size=15, 
                        arrowprops=dict(arrowstyle="->"))
    ax.legend(numpoints=1)
    
def xyz2tr3(T, ECEF, lp, pp, hp, r):
    xp = (r + hp) * cos(pp) * cos(lp)
    yp = (r + hp) * cos(pp) * sin(lp)
    zp = (r + hp) * sin(pp)
    
    Ry = matrix([[cos((pi / 2) - pp), 0, -sin((pi / 2) - pp)], [0, 1, 0], [sin((pi / 2) - pp), 0, cos((pi / 2) - pp)]])
    Rz = matrix([[cos(lp), sin(lp), 0], [-sin(lp), cos(lp), 0], [0, 0, 1]])
    
    X = array(map(lambda x: matrix([x[0] - xp, x[1] - yp, x[2] - zp]).T, ECEF))
    Ans = array(map(lambda x: array(Ry * Rz * x), X)).T
    N = -Ans[0, 0]    
    E = Ans[0, 1]    
    U = Ans[0, 2] 
    
    El = arctan2(U, sqrt(E**2 + N**2))
    Zenith = degrees((pi / 2) - El)
    
    x = []
    y = []
    S = []
    T2 = []
    for i in range(len(Zenith)):
        if Zenith[i] >= 0 and Zenith[i] <= 80:
            x.append(E[i])
            y.append(N[i])
            S.append(degrees(El[i]))
            T2.append(T[i])
        
    return x, y, S, T2

def drawNewSkyPlot2(lp, pp, hp):
    ECEF, T = readECEF()
    x, y, S, T2 = xyz2tr3(T, ECEF, lp, pp, hp, R)
    
    fig = plt.figure("New Skyplot2")
    ax = fig.add_subplot(111)
    
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    
    ax.set_title("Skyplot G31 2014/5/4", size = 20)
    
    for i in range(len(S)):
        ax.plot(x[i], y[i], "g*", label = "G31", ms = 5 + 20 * (1.0 * S[i] / 90))
        if (T2[i] % 3600) == 0:
            ax.annotate("%02d" % ((T2[i] / 3600 + 10) % 24), xy=(x[i], y[i]), 
                        xytext=(-30, -30), textcoords="offset points", va="center",
                        size=15, 
                        arrowprops=dict(arrowstyle="->"))
            
    ax.plot(x, y, "g-", label = "G31 Track")
    
    ax.plot(0, 0, "ro", ms = 15)
    ax.annotate("Tokyo", xy=(0, 0), 
                xytext=(-30, -30), textcoords="offset points", va="center",
                size=15, 
                arrowprops=dict(arrowstyle="->"))
    plt.xlabel("E (m)")
    plt.ylabel("N (m)")
    plt.grid()
    
    
def main():
    drawMap("Ground Track G31 2014/5/4 (Platte Carree Projection)", "platte")
    drawMap("Ground Track G31 2014/5/4 (Mercator Projection)", "mercator")
    
    #use tokyo for observr station
    pp = radians(35 + 41.0 / 60 + 22.4 / 3600)
    lp = radians(139 + 41.0 / 60 + 30.2 / 3600)
    hp = 0.0
    drawSkyPlot(lp, pp, hp)  
    drawNewSkyPlot1(lp, pp, hp)  
    drawNewSkyPlot2(lp, pp, hp)
    drawMap("Ground Track2 G31 2014/5/4 (Platte Carree Projection)", "platte2", lp, pp, hp)
    drawMap("Ground Track2 G31 2014/5/4 (Mercator Projection)", "mercator2", lp, pp, hp)
    
    plt.show()

if __name__ == "__main__":
    main()

    
    


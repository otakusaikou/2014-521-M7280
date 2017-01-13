'''
Created on 2014/03/30

@author: otakusaikou1
'''
from numpy import sin, cos, matrix, array, pi, radians
from mpl_toolkits.mplot3d import Axes3D, proj3d
import matplotlib.pyplot as plt
import time
import datetime
DEBUG = False
def toDMS(degrees):
    D = int(degrees)
    M = abs(int((1.0 * degrees - D) * 60))
    S = abs((1.0 * degrees - D - (1.0 * M / 60)) * 3600)
    return D, M, S

def getGST(t):
    GST0 = 6 * 60**2 + 37 * 60 + 7.7912
    t0 = 2454100.5 * 86400
    dt = (t - t0)
    omega = (360.0 / 86164.09053) * (86400 / 360.0)
    return (GST0 + omega * dt) % 86400

def main():
    #Start from 1992/3/31 00:00:00, Julian Day is 2448712.5, time offset is 10
    #minutes, End with 1992/4/3 00:00:00
    ts = 2448712.5 * 86400
    tmpt = 2448712.5 * 86400
    offset = 10.0 * 60
    te = (2448715.5 * 86400) + offset
    
    if DEBUG:
        ts = 2454100.5 * 86400
        tmpt = 2454100.5 * 86400
        offset = 1440.0 * 60
        te = (2454146.5 * 86400) + offset
    
    
    T = []
    h = []
    m = []
    s = []
    D = []
    M = []
    S = []
    X = []
    Y = []
    Z = []
    GST_HMS = []
    GST_DMS = []
    index = 0
    while tmpt < te:
        ans = getGST(tmpt)
        hms = toDMS(ans / 3600)
        dms = toDMS((hms[0] * 60**2 + hms[1] * 60 + hms[2]) * (360.0 / 86400))
        GST_HMS.append(ans / 3600)
        GST_DMS.append((hms[0] * 60**2 + hms[1] * 60 + hms[2]) * (360.0 / 86400))
        T.append(int((tmpt - ts) / 60))
        h.append(hms[0])
        m.append(hms[1])
        s.append(hms[2])
        D.append(dms[0])
        M.append(dms[1])
        S.append(dms[2])
        print T[index], D[index], M[index], "%.4f" % S[index], h[index], m[index], "%.4f" % s[index]
        index += 1
        tmpt += offset
    
    #Generate an ECEF coordinates (The second point in lab2)
    p = radians(-50.0)
    l = radians(30.0)
    he = 0
    r = 6371000.0; #meter
    #Calculate ECEF coordinates
    x = (r + he) * cos(p) * cos(l)
    y = (r + he) * cos(p) * sin(l)
    z = (r + he) * sin(p)
    
    for i in range(0, 144):
        Rz = matrix([[cos(radians(-GST_DMS[i])), sin(radians(-GST_DMS[i])), 0], [-sin(radians(-GST_DMS[i])), cos(radians(-GST_DMS[i])), 0], [0, 0, 1]])
        XYZ = array(Rz * matrix([[x], [y], [z]]))
        X.append(XYZ[0][0])
        Y.append(XYZ[1][0])
        Z.append(XYZ[2][0])
        #print h[i], m[i], s[i], x, y, z, X[i], Y[i], Z[i]
    
    
    '''for 2d map'''"""
    fig, ax = plt.subplots()
    ax.plot(T, GST_DMS)
    ax.plot(T, GST_HMS)
    
    ax.annotate(r'GST(deg)', xy=(T[150], GST_DMS[150]), 
        xytext=(-50, 50), textcoords='offset points', va='center',
        size=15, 
        arrowprops=dict(arrowstyle='->'))
    
    ax.annotate(r'GST(hour)', xy=(T[200], GST_HMS[200]), 
        xytext=(-55, 100), textcoords='offset points', va='center',
        size=15, 
        arrowprops=dict(arrowstyle='->'))
    
    ax.annotate("Day1: " + str(datetime.datetime(1992, 3, 31, 0, 0, 0)), xy=(T[0], 0), 
        xytext=(10, 60), textcoords='offset points', va='center',
        size=13, 
        arrowprops=dict(arrowstyle='->'))
    
    ax.annotate("Day2: " + str(datetime.datetime(1992, 4, 1, 0, 0, 0)), xy=(T[144], 0), 
        xytext=(-90, 50), textcoords='offset points', va='center',
        size=13, 
        arrowprops=dict(arrowstyle='->'))
    
    ax.annotate("Day3: " + str(datetime.datetime(1992, 4, 2, 0, 0, 0)), xy=(T[288], 0), 
        xytext=(-55, 50), textcoords='offset points', va='center',
        size=13, 
        arrowprops=dict(arrowstyle='->'))
    
    plt.title("Greenwich Sideral Time", size=25)
    plt.xlabel("Time (min)")
    plt.ylabel("Greenwich Sideral Time (deg/hr)")
    plt.show()
    """
    
    
    
    
    '''for plot 3d scatter'''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[1:-1], Y[1:-1], Z[1:-1], c = 'b', marker = '*')
    ax.scatter(X[0], Y[0], Z[0], c = 'r', marker = '^')
    ax.scatter(X[-1], Y[-1], Z[-1], c = 'g', marker = 'v')
    ax.scatter(x, y, z, c = 'y', marker = 'o')
    
    
    labels = []
    """
    count = 0
    pt_t0 = datetime.datetime(1992, 3, 31, 0, 0,0)
    for i in range(0, 144, 22):
        x2, y2, _ = proj3d.proj_transform(X[i],Y[i],Z[i], ax.get_proj())
        labels.append((ax.annotate(
                    "%s\nX=%.4f\nY=%.4f\nZ=%.4f" % (str(pt_t0 + datetime.timedelta(0, T[i] * 60)), X[i], Y[i], Z[i]), 
                    xy = (x2, y2), xytext = (50, -100 * ((-1)**count)),
                    textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 1),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')), i))
        count += 1"""
    
    pt_t0 = datetime.datetime(1992, 3, 31, 0, 0,0)
    x2, y2, _ = proj3d.proj_transform(X[0],Y[0],Z[0], ax.get_proj())
    labels.append((ax.annotate(
                               "%s\nX=%.4f\nY=%.4f\nZ=%.4f" % (str(pt_t0 + datetime.timedelta(0, T[0] * 60)), X[0], Y[0], Z[0]), 
                               xy = (x2, y2), xytext = (0, 70),
                               textcoords = 'offset points', ha = 'right', va = 'bottom',
                               bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 1),
                               arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')), 0))
    
    x2, y2, _ = proj3d.proj_transform(X[143],Y[143],Z[143], ax.get_proj())
    labels.append((ax.annotate(
                               "%s\nX=%.4f\nY=%.4f\nZ=%.4f" % (str(pt_t0 + datetime.timedelta(0, T[143] * 60)), X[-1], Y[-1], Z[-1]), 
                               xy = (x2, y2), xytext = (0, -70),
                               textcoords = 'offset points', ha = 'right', va = 'bottom',
                               bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 1),
                               arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')), 143))
    
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    labels.append((ax.annotate(
                               "Original ECEF point\nx=%.4f\ny=%.4f\nz=%.4f" % (x, y, z), 
                               xy = (x2, y2), xytext = (0, 70),
                               textcoords = 'offset points', ha = 'right', va = 'bottom',
                               bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 1),
                               arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')), 144))
    X.append(x)
    Y.append(y)
    Z.append(z)
    
    def update_position(e):
        count = 0
        for label in labels:
            x2, y2, _ = proj3d.proj_transform(X[label[1]],Y[label[1]],Z[label[1]], ax.get_proj())
            label[0].xy = x2, y2
            label[0].xytext = (50, -100 * ((-1)**count))
            label[0].update_positions(fig.canvas.renderer)
            fig.canvas.draw()
            count += 1
    
    fig.canvas.mpl_connect('button_release_event', update_position)
    plt.title('Quasi-Inertial &ECEF Frames', size=25)
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    plt.show()
    
    

if __name__ == "__main__":
    main()

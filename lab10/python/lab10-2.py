'''
Created on 2014/06/09

@author: otakusaikou1
'''
from numpy import array, arange, append, sqrt, cos, sin, tan, matrix, arctan2, set_printoptions, zeros
from scipy import interpolate 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import bisect

#disable scientific notation
set_printoptions(suppress=True)

R = 6371000.0
c = 299792458.0
a = 6378137.0
f = 1.0 / 298.257222101 
b = a - a * f
e = sqrt((a**2 - b**2) / a**2)

def readSp3(filelist, SID):
    Coords = []
    for file in filelist:
        fin = open(file)
        data = fin.readlines()
        fin.close()
        for i in range(22, 3158, 33):
            Coords.append(data[i + int(SID[-2:])].split()[1:4])
            
    Coords = array(Coords).astype(float)
    return array(arange(-86400, 171901, 900)), Coords[:, 0] * 1000, Coords[:, 1] * 1000, Coords[:, 2] * 1000

def readClk(filelist, SID):
    dt = []
    for file in filelist:
        fin = open(file)
        data = fin.readlines()
        fin.close()
        
        i = 422
        while i < len(data):
            if data[i].startswith("AS " + SID):
                dt.append(data[i].split()[9])
            i += 1
            
    dt = array(dt).astype(float)
    return array(arange(-86400, 172771, 30)), dt

def readRINEX(filename, SID):
    fin = open(filename)
    data = fin.readlines()
    fin.close()
    t = []
    CA = []
    for i in range(len(data)):
        if data[i].startswith(" 14  5  4"):
            datestr = data[i][0:27]
            satstr = data[i][30:63].replace("\n", "")
            if len(satstr.split("G")) == 1:
                continue 
            
            if SID not in satstr.split("G")[1:]:
                continue
            t.append(int(datestr.split()[3]) * 3600 +  int(datestr.split()[4]) * 60 + float(datestr.split()[5]))
            CA.append(float(data[i + 1 + 3 * satstr.split("G")[1:].index(SID)][50:65]))
    return array(t), array(CA)
    

def getFunctions(T, X, Y, Z, T2, dt, t):
    Fx = interpolate.lagrange(T, X)
    Fy = interpolate.lagrange(T, Y)
    Fz = interpolate.lagrange(T, Z)
    Fdt = interpolate.lagrange(T2, dt)
    
    return Fx, Fy, Fz, Fdt

def getM(phi, a, e):
    return (a * (1 - e**2)) / sqrt((1 - e**2 * sin(phi)**2)**3)

def getN(phi, a, e):
    return a / sqrt(1 - e**2 * sin(phi)**2)

def xyz2lph(x, y, z, r):
    l = arctan2(y, x)
    p = arctan2(z, sqrt(x**2 + y**2))
    h = sqrt(x**2 + y**2 + z**2) - r
    return l, p, h

def getRecv(Xs, Ys, Zs, Sr, x0, y0, z0, r):
    lp, pp, hp = xyz2lph(x0, y0, z0, r)
    x1 = x0
    y1 = y0
    z1 = z0
    dt = 0
    while True:
        S = sqrt((Xs - x1)**2 + (Ys - y1)**2 + (Zs - z1)**2)
        L = matrix([Sr - S]).T
        A = matrix([(x1 - Xs) / S, (y1 - Ys) / S, (z1 - Zs) / S, zeros(len(Xs)) + c]).T
        
        X = (A.T * A).I * (A.T * L)
        x1 += X[0,0]
        y1 += X[1,0]
        z1 += X[2,0]
        dt += X[3,0]
        if abs(X[:3].sum()) < 10**-8:
            break
        print 111
    V = array(A * X - L)
    Sig = sqrt((V.T).dot(V)[0, 0] / (len(Xs) - 1))
    Qxx = array((A.T * A).I)
    
    J = matrix([[-sin(pp) * cos(lp), -sin(pp) * sin(lp), cos(pp)], [-sin(lp), cos(lp), 0], [cos(pp) * cos(lp), cos(pp) * sin(lp), sin(pp)]])
    Qenu = (J * Qxx[:3, :3] * J.T)

    trueError = sqrt((x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2)
    PDOP = sqrt(Qenu[0, 0] + Qenu[1, 1] + Qenu[2, 2])
    VDOP = sqrt(Qenu[2, 2])
    HDOP = sqrt(Qenu[0, 0] + Qenu[1, 1])
    TDOP = sqrt(Qxx[3, 3])

    #print x1, y1, z1, Sig, PDOP, VDOP, HDOP, trueError
    return x1, y1, z1, dt, Sig, PDOP, VDOP, HDOP, TDOP, trueError, Qxx
        
def main():
    ECEF = []
    T_all = []
    CA_all = []
    DT = []
    testx = []
    
    
    fig = plt.figure("C/A code range observation (m)")
    ax = fig.add_subplot(111)
    
    #test range
    offset = 3
    offset2 = 1
    
    #fout = open("result.txt", "w")
    #fout.write("Time\tC/A obs\t\tTime\tC/A obs\t\tTime\tC/A obs\t\tTime\tC/A obs\t\tTime\tC/A obs\t\tTime\tC/A obs\n")
    
    for i in range(1, 33):
        try:
            T, X, Y, Z = readSp3(["igs17906.sp3", "igs17910.sp3", "igs17911.sp3"], "PG%02d" % i)
            T2, dt = readClk(["igs17906.clk_30s", "igs17910.clk_30s", "igs17911.clk_30s"], "G%02d" % i)
            t, CA = readRINEX("arbt1240.14o", "%02d" % i)
            #for j in range(len(t) / 4):
                #fout.write("%d\t%.5f\t%d\t%.5f\t%d\t%.5f\t%d\t%.5f\t%d\t%.5f\t%d\t%.5f\n" % (t[j], CA[j], t[j + len(t) / 6], CA[j + len(t) / 6], t[j + 2 * len(t) / 6], CA[j + 2 * len(t) / 6], t[j + 3 * len(t) / 6], CA[j + 3 * len(t) / 6], t[j + 4 * len(t) / 6], CA[j + 4 * len(t) / 6], t[5 * len(t) / 6], CA[j + 5 * len(t) / 6]))
#            
            
            T_all.append(t)
            CA_all = append(CA_all, CA)
            preindex = bisect.bisect(T, t[0])
            preindex2 = bisect.bisect(T2, t[0])
            Fx, Fy, Fz, Fdt = getFunctions(T[preindex - offset:preindex + offset], X[preindex - offset:preindex + offset], Y[preindex - offset:preindex + offset], Z[preindex - offset:preindex + offset], T2[preindex2 - offset2:preindex2 + offset2], dt[preindex2 - offset2:preindex2 + offset2], t[0]) 
            for e in t:
                index = bisect.bisect(T, e)
                index2 = bisect.bisect(T2, e)
                if index != preindex:
                    preindex = index
                    Fx, Fy, Fz, Fdt = getFunctions(T[index - offset:index + offset], X[index - offset:index + offset], Y[index - offset:index + offset], Z[index - offset:index + offset], T2[index2 - offset2:index2 + offset2], dt[index2 - offset2:index2 + offset2], e)
                ECEF.append([Fx(e), Fy(e), Fz(e)])
                
                testx.append(Fdt(e))
                
                DT.append(Fdt(e))
            #start = 0
            #break lines if range of two point bigger than threshold
            #for i in range(len(t) - 1):
                #if sqrt((t[i] - t[i + 1])**2 + (CA[i] - CA[i + 1])**2) > 2000:
                    #ax.plot(t[start:i + 1], CA[start:i + 1])
                    #start = i + 1
            #ax.plot(t[start:], CA[start:])
            
            #interpolation test
            #ax.plot(T2, dt, 'r-', label = 'Value in clk_30s file')
            #ax.plot(t, testx, 'b*', label = 'Interpolated value')  
            #formatter = ScalarFormatter()
            #formatter.set_scientific(False)
            #ax.yaxis.set_major_formatter(formatter)   
            #plt.xlabel("Time (sec)", size = 20)
            #plt.ylabel("dt (m)", size = 20)
            #plt.title("Function of time (3rd order polynomial)", size = 20)
            #plt.legend(numpoints = 1, loc = 4)
            #plt.grid()
        except: 
            print i
    #fout.close()
    #plt.show()
            
            
    ECEF = array(ECEF)
    DT = array(DT)
    x0 = -147353.2870 
    y0 = -5182836.0270  
    z0 = 3702154.5080
    
    x, y, z, dt, Sig, PDOP, VDOP, HDOP, TDOP, trueError, Qxx = getRecv(ECEF[:, 0], ECEF[:, 1], ECEF[:, 2], CA_all + c * DT, x0, y0, z0, R)
    print x, y, z, dt, Sig, trueError
    print PDOP, VDOP, HDOP, TDOP
    print Sig * PDOP, Sig * VDOP, Sig * HDOP, Sig * TDOP
    print Qxx
    
    #ax.set_title("C/A code range observation", size = 20)
    #plt.xlabel("Time (sec)", size = 20)
    #plt.ylabel("C/A code range observation (m)", size = 20)
    #plt.grid()
    #plt.show()
    
if __name__ == "__main__":
    main()

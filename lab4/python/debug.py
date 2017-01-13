'''
Created on 2014/04/09

@author: otakusaikou1
'''
from numpy import sin, cos, arctan2, sqrt, radians, degrees, matrix, array, pi

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

def xyz2lph(x, y, z, a, e):
    l = arctan2(y, x)
    p0 = arctan2(z, (1 - e**2) * sqrt(x**2 + y**2))
    printAngle(p0)
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

def lph2xyz(l, p, he, a, e):
    N = getN(p, a, e)
    x = (N + he) * cos(p) * cos(l)
    y = (N + he) * cos(p) * sin(l)
    z = (N * (1 - e**2) + he) * sin(p)
    return x, y, z

def main():
    #define initial variable
    a = 6378137.0
    f = 1.0 / 298.257222101 
    b = a - a * f
    e = sqrt((a**2 - b**2) / a**2)
    
    l0 = -70
    p0 = 30
    
    x, y, z = lph2xyz(radians(l0), radians(p0), 0, a, e)
        
    x = 1894800.925945570700
    y = 1093963.824655427100        
    z = -5971040.007008514400
    
    #x = 12046.5808
    #y = -4649394.0826
    #z = 4353160.0634
    l, p, h = xyz2lph(x, y, z, a, e)
    print x, y, z
    print degrees(p)
    print degrees(l)
    print h
    

    
    
if __name__ == "__main__":
    main()
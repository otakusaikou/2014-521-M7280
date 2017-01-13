#!/usr/bin/python2.7

import math
import matplotlib.pyplot as plt
a = 6378137.0
f = 1.0 / 298.257222101
b = a - a * f
e = math.sqrt((a**2 - b**2) / a**2)

Lat = []
M_80 = []
N_80 = []
Ravg_80 = []
RG_80 = []

for i in range(-90, 91):
    Lat.append(i)
    M = a * (1 - e**2) / math.sqrt((1 - e**2 * (math.sin(math.radians(i)))**2)**3)
    M_80.append(M)
    N = a / math.sqrt(1 - e**2 * (math.sin(math.radians(i)))**2)
    N_80.append(N)
    Ravg_80.append(1.0 * (M + N) / 2)
    RG_80.append(math.sqrt(M * N))
    
a = 6378160.0;
f = 1.0 / 298.247167427;
b = a - a * f
e = math.sqrt((a**2 - b**2) / a**2)
M_67 = []
N_67 = []
Ravg_67 = []
RG_67 = []
dM = []
dN = []
dRavg = []
dRG = []


for i in range(-90, 91):
    M = a * (1 - e**2) / math.sqrt((1 - e**2 * (math.sin(math.radians(i)))**2)**3)
    M_67.append(M)
    N = a / math.sqrt(1 - e**2 * (math.sin(math.radians(i)))**2)
    N_67.append(N)
    Ravg_67.append(1.0 * (M + N) / 2)
    RG_67.append(math.sqrt(M * N))
    
for i in range(181):
    dM.append(M_67[i] - M_80[i])
    dN.append(N_67[i] - N_80[i])
    dRavg.append(Ravg_67[i] - Ravg_80[i])
    dRG.append(RG_67[i] - RG_80[i])
    
fig, ax = plt.subplots()

ax.plot(Lat, dM, label = "Radii of curvative on meridian plane")
ax.plot(Lat, dN, label = "Radii of curvative on prime vertical plane")
ax.plot(Lat, dRavg, label = "Average of curvative")
ax.plot(Lat, dRG, label = "Gaussian curvative")

#ax.plot(Lat, M_80, label = "Radii of curvative on meridian plane")
#ax.plot(Lat, N_80, label = "Radii of curvative on prime vertical plane")
#ax.plot(Lat, Ravg_80, label = "Average of curvative")
#ax.plot(Lat, RG_80, label = "Gaussian curvative")

ax.annotate(r'Radii of curvative on meridian plane', xy=(Lat[111], dM[111]), 
            xytext=(30, -80), textcoords='offset points', va='center',
            arrowprops=dict(arrowstyle='->'))
#
ax.annotate(r'Radii of curvative on prime vertical plane', xy=(Lat[130], dN[130]), 
            xytext=(-140, 80), textcoords='offset points', va='center',
            arrowprops=dict(arrowstyle='->'))
            
ax.annotate('Average of curvative\n               &\n Gaussian curvative', xy=(Lat[120], dRavg[120]), 
            xytext=(-140, 50), textcoords='offset points', va='center',
            arrowprops=dict(arrowstyle='->'))
            
#ax.annotate('Average of curvative, Ravg_80[0]=%.6f' % Ravg_80[0], xy=(-90, Ravg_80[0]), 
#            xytext=(-70, 80), textcoords='offset points', va='center',
#            arrowprops=dict(arrowstyle='->'))
#            
#ax.annotate('Gaussian curvative, RG_80[0]=%.6f' % RG_80[0], xy=(-90, RG_80[0]), 
#            xytext=(-70, -80), textcoords='offset points', va='center',
#            arrowprops=dict(arrowstyle='->'))


plt.xlabel("Latitude  (Unit: degree)")
plt.ylabel("Radii of curvature  (Unit: m)")
plt.show()

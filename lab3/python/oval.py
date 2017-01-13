from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

a_80 = 6378137.0
f_80 = 1.0 / 298.257222101
b_80 = a_80 - a_80 * f_80

a_67 = 6378160.0;
f_67 = 1.0 / 298.247167427;
b_67 = a_67 - a_67 * f_67

ellipse_80 = Ellipse(xy=(0, 0), width=2*a_80, height=2*b_80, 
                        edgecolor='b', fc='None')

ellipse_67 = Ellipse(xy=(0, 0), width=2*a_80, height=2*b_67, 
                        edgecolor='r', fc='None')
                        
fig.gca().add_artist(ellipse_80)
fig.gca().add_artist(ellipse_67)

plt.axis([0, a_67+100, 0, b_80+1000])
plt.show()
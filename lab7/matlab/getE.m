function E1 = getE(e0, toa, a, mt0, t)
%This function calculate eccentric argument of perigee
%Define constants
GM = 398600441800000.0;
     
%Get eccentric argument of perigee
n0 = sqrt(GM / a^3); %Mean motion of satellite
mt = mt0 + (t - toa) * n0; %Get mean anomaly at t second with given mean anomaly and mean motion of satellite 
    
E0 = mt;
E1 = E0 - ((E0 - e0 * sin(E0) - mt) / (1 - e0 * cos(E0)));
    
%Numerical solution
while abs(E0 - E1) > 10^-12
    E0 = E1;
    E1 = E0 - ((E0 - e0 * sin(E0) - mt) / (1 - e0 * cos(E0)));
end
E1 = mod(E1, (2 * pi));
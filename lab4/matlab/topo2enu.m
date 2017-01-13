function [e, n, u] = topo2enu(Az, El, Sr)
% Az (output) azimuth angle
% El (output) elevation angle
% Sr (output) range from origin to input point
% n (input) n value of cartesian reference frame
% e (input) e value of cartesian reference frame
% u (input) u value of cartesian reference frame
e = Sr * cos(El) * sin(Az);
n = Sr * cos(El) * cos(Az);
u = Sr * sin(El);


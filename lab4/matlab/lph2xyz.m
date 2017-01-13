function [x, y, z] = lph2xyz(l, p, h, a, e0)
% x (output) x value of input point in global elliposidal refrence frame
% y (output) y value of input point in global elliposidal refrence frame
% z (output) z value of input point in global elliposidal refrence frame
% a (input) length of semi-major axis of ellipsoid
% e0 (input) eccentricity of ellipsoid
% l (input) longitude
% p (input) latitude
% he (input) elliposidal height
N = a / sqrt(1 - e0^2 * sin(p)^2);
x = (N + h) * cos(p) * cos(l);
y = (N + h) * cos(p) * sin(l);
z = (N * (1 - e0^2) + h) * sin(p);
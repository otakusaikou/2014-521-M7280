function [x, y, z] = lph2xyz(l, p, h, r)
% x (output) x value of input point in global spherical refrence frame
% y (output) y value of input point in global spherical refrence frame
% z (output) z value of input point in global spherical refrence frame
% l (input) longitude
% p (input) latitude
% h (input) spherical height
% r (input) radius of sphere
x = (r + h) * cos(p) * cos(l);
y = (r + h) * cos(p) * sin(l);
z = (r + h) * sin(p);
function [l, p, h] = xyz2lph(x, y, z, r)
% l (output) longitude
% p (output) latitude
% h (output) spherical height
% x (input) x value of input point in global spherical refrence frame
% y (input) y value of input point in global spherical refrence frame
% z (input) z value of input point in global spherical refrence frame
% r (input) radius of sphere
l = atan2(y, x);
p = atan2(z, sqrt(x^2 + y^2));
h = sqrt(x^2 + y^2 + z^2) - r;
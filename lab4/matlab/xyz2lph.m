function [l, p, h] = xyz2lph(x, y, z, a, e0)
% l (output) longitude
% p (output) latitude
% he (output) elliposidal height
% x (input) x value of input point in global elliposidal refrence frame
% y (input) y value of input point in global elliposidal refrence frame
% z (input) z value of input point in global elliposidal refrence frame
% a (input) length of semi-major axis of ellipsoid
% e0 (input) eccentricity of ellipsoid

l = atan2(y, x);
p0 = atan2(z, (1 - e0^2) * sqrt(x^2 + y^2));
N0 = a / sqrt(1 - e0^2 * sin(p0)^2);
p = atan2((z + N0 * e0^2 * sin(p0)), sqrt(x^2 + y^2));
while (p - p0 > 10^-12)
    p0 = p;
    N0 = a / sqrt(1 - e0^2 * sin(p0)^2);
    p = atan2((z + N0 * e0^2 * sin(p0)), sqrt(x^2 + y^2));
end
N = a / sqrt(1 - e0^2 * sin(p)^2);
h = sqrt(x^2 + y^2 + (z + N * e0^2 * sin(p))^2)  - N;
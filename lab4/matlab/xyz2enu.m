function [e, n, u] = xyz2enu(x, y, z, xp, yp, zp, a, e0)
% n (output) n value of cartesian reference frame
% e (output) e value of cartesian reference frame
% u (output) u value of cartesian reference frame
% x (input) x value of input point in global elliposidal refrence frame
% y (input) y value of input point in global elliposidal refrence frame
% z (input) z value of input point in global elliposidal refrence frame
% xp (input) x value of local origin in global elliposidal refrence frame
% yp (input) y value of local origin in global elliposidal refrence frame
% zp (input) z value of local origin in global elliposidal refrence frame
% a (input) length of semi-major axis of ellipsoid
% e0 (input) eccentricity of ellipsoid

[lp, pp, hp] = xyz2lph(xp, yp, zp, a, e0);
Ry = [cos((pi / 2) - pp), 0, -sin((pi / 2) - pp); 0, 1, 0; sin((pi / 2) - pp), 0, cos((pi / 2) - pp)];
Rz = [cos(lp), sin(lp), 0; -sin(lp), cos(lp), 0; 0, 0, 1];
X = [x - xp; y - yp; z - zp];
Ans = Ry * Rz * X;
n = -Ans(1);
e = Ans(2);
u = Ans(3);
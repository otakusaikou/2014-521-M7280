function [x, y, z] = enu2xyz(e, n, u, xp, yp, zp, a, e0)
% x (output) x value of input point in global elliposidal refrence frame
% y (output) y value of input point in global elliposidal refrence frame
% z (output) z value of input point in global elliposidal refrence frame
% n (input) n value of cartesian reference frame
% e (input) e value of cartesian reference frame
% u (input) u value of cartesian reference frame
% xp (input) x value of local origin in global elliposidal refrence frame
% yp (input) y value of local origin in global elliposidal refrence frame
% zp (input) z value of local origin in global elliposidal refrence frame
% a (input) length of semi-major axis of ellipsoid
% e0 (input) eccentricity of ellipsoid

[lp, pp, hp] = xyz2lph(xp, yp, zp, a, e0);
Ry = [cos((pi / 2) - pp), 0, -sin((pi / 2) - pp); 0, 1, 0; sin((pi / 2) - pp), 0, cos((pi / 2) - pp)];
Rz = [cos(lp), sin(lp), 0; -sin(lp), cos(lp), 0; 0, 0, 1];
T = [xp; yp; zp];
X = [-n; e; u];
Ans = transpose(Rz) * transpose(Ry) * X + T;
x = Ans(1);
y = Ans(2);
z = Ans(3);
function [x, y, z] = enu2xyz(n, e, u, xp, yp, zp, r)
% x (output) x value of input point in global spherical refrence frame
% y (output) y value of input point in global spherical refrence frame
% z (output) z value of input point in global spherical refrence frame
% n (input) n value of cartesian reference frame
% e (input) e value of cartesian reference frame
% u (input) u value of cartesian reference frame
% xp (input) x value of local origin in global spherical refrence frame
% yp (input) y value of local origin in global spherical refrence frame
% zp (input) z value of local origin in global spherical refrence frame
% r (input) radius of sphere
[lp, pp, hp] = xyz2lph(xp, yp, zp, r);
Ry = [cos((pi / 2) - pp), 0, -sin((pi / 2) - pp); 0, 1, 0; sin((pi / 2) - pp), 0, cos((pi / 2) - pp)];
Rz = [cos(lp), sin(lp), 0; -sin(lp), cos(lp), 0; 0, 0, 1];
T = [xp; yp; zp];
X = [-n; e; u];
Ans = transpose(Rz) * transpose(Ry) * X + T;
x = Ans(1);
y = Ans(2);
z = Ans(3);
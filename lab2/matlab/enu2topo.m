function [Az, El, Sr] = enu2topo(n, e, u)
% Az (output) azimuth angle
% El (output) elevation angle
% Sr (output) range from origin to input point
% n (input) n value of cartesian reference frame
% e (input) e value of cartesian reference frame
% u (input) u value of cartesian reference frame
Az = atan2(e, n);
El = atan2(u, sqrt(e^2 + n^2));
Sr = sqrt(n^2 + e^2 + u^2);

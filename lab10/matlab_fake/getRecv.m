function [x1, y1, z1, dt, Sig, PDOP, VDOP, HDOP, TDOP, trueError, Qxx] = getRecv(Xs, Ys, Zs, Sr, x0, y0, z0, R)
lp = atan2(y0, x0);
pp = atan2(z0, sqrt(x0^2 + y0^2));
hp = sqrt(x0^2 + y0^2 + z0^2) - R;
c = 299792458.0;
x1 = x0;
y1 = y0;
z1 = z0;
dt = 0;
while true
    S = ((Xs - x1).^2 + (Ys - y1).^2 + (Zs - z1).^2).^0.5;
    L = transpose(Sr - S);
    A = transpose([(x1 - Xs) ./ S; (y1 - Ys) ./ S; (z1 - Zs) ./ S; zeros(1, length(Xs)) + c]);
    X = inv(transpose(A) * A) * (transpose(A) * L);
    x1 = x1 + X(1);
    y1 = y1 + X(2);
    z1 = z1 + X(3);
    dt = dt + X(4);
    if abs(sum(X(1:3))) < 10^-8
        break;
    end
end
V = (A * X) - L;
Sig= ((transpose(V) * V) / (length(Xs) - 1))^0.5;
Qxx = inv(transpose(A) * A);
J = [[-sin(pp) * cos(lp), -sin(pp) * sin(lp), cos(pp)]; [-sin(lp), cos(lp), 0]; [cos(pp) * cos(lp), cos(pp) * sin(lp), sin(pp)]];
Qenu = J * Qxx(1:3, 1:3) * transpose(J);
trueError = ((x1 - x0).^2 + (y1 - y0).^2 + (z1 - z0).^2).^0.5;
PDOP = sqrt(Qenu(1, 1) + Qenu(2, 2) + Qenu(3, 3));
VDOP = sqrt(Qenu(3, 3));
HDOP = sqrt(Qenu(1, 1) + Qenu(2, 2));
TDOP = sqrt(Qxx(4, 4));
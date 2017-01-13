function [x1, y1, z1, Sig, PDOP, VDOP, HDOP, trueError, Qxx] = getRecv(Xs, Ys, Zs, S, Sr, pp, lp, hp, R)
x0 = (R + hp) * cos(pp) * cos(lp);
y0 = (R + hp) * cos(pp) * sin(lp);
z0 = (R + hp) * sin(pp);
x1 = x0;
y1 = y0;
z1 = z0;

while true
    S = ((Xs - x1).^2 + (Ys - y1).^2 + (Zs - z1).^2).^0.5;
    L = Sr - S;
    A = [(x1 - Xs) ./ S, (y1 - Ys) ./ S, (z1 - Zs) ./ S];
    X = inv(transpose(A) * A) * (transpose(A) * L);
    x1 = x1 + X(1);
    y1 = y1 + X(2);
    z1 = z1 + X(3);
    if abs(sum(X)) < 10^-8
        break;
    end
end
V = (A * X) - L;
Sig= ((transpose(V) * V) / (length(Xs) - 1))^0.5;
Qxx = inv(transpose(A) * A);
J = [[-sin(pp) * cos(lp), -sin(pp) * sin(lp), cos(pp)]; [-sin(lp), cos(lp), 0]; [cos(pp) * cos(lp), cos(pp) * sin(lp), sin(pp)]];
Qenu = J * Qxx * transpose(J);
trueError = ((x1 - x0).^2 + (y1 - y0).^2 + (z1 - z0).^2).^0.5;
PDOP = sqrt(Qenu(1, 1) + Qenu(2, 2) + Qenu(3, 3));
VDOP = sqrt(Qenu(3, 3));
HDOP = sqrt(Qenu(1, 1) + Qenu(2, 2));
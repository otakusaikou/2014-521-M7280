clc;
format long g;
%Set constants
R = 6371000.0;
c = 299792458.0;

ECEF = [];
T_all = [];
CA_all = [];
DT = [];
testx = [];

Xs = [];
Ys = [];
Zs = [];
DT = [];
CA = [];

for i=1:32
    [t, ca] = readrinex('arbt1240.14o', sprintf('%02d', i));
    [T, X, Y, Z] = readsp3({'igs17906.sp3', 'igs17910.sp3', 'igs17911.sp3'}, sprintf('PG%02d', i));
    [T2, dt] = readclk({'igs17906.clk_30s', 'igs17910.clk_30s', 'igs17911.clk_30s'}, sprintf('AS G%02d', i));
    CA = [CA; ca];
    for j = 1:length(t)
        index = binarysearch(T, t(j));
        index2 = binarysearch(T2, t(j));
        offset = 3;
        offset2 = 1;
        xlist = T(index - offset:index + offset - 1);
        xlist2 = T2(index2 - offset2:index2 + offset2 - 1);
        Xs = [Xs, lagrange(xlist, X(index - offset:index + offset - 1), t(j))];
        Ys = [Ys, lagrange(xlist, Y(index - offset:index + offset - 1), t(j))];
        Zs = [Zs, lagrange(xlist, Z(index - offset:index + offset - 1), t(j))];
        DT = [DT, lagrange(xlist2, dt(index2 - offset2:index2 + offset2 - 1), t(j))];
    end
    disp(i);
end

x0 = -147353.2870;
y0 = -5182836.0270;
z0 = 3702154.5080;

[x, y, z, dt, Sig, PDOP, VDOP, HDOP, TDOP, trueError, Qxx] = getRecv(Xs, Ys, Zs, transpose(CA) + c * DT, x0, y0, z0, R);
disp([x, y, z, dt, Sig]);
disp([PDOP, VDOP, HDOP, TDOP, trueError]);
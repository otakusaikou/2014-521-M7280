function skyplot2(r)
fin = fopen('result.txt');
%scan satellite position file
c = textscan(fin, '%d%f%f%f%f%f%f', 'headerLines', 1);
[Xs, Ys, Zs] = c{1, 5:7};
T = c{1, 1};
fclose(fin);

%use tokyo for observr station
pp = (35 + 41.0 / 60 + 22.4 / 3600) * (pi / 180);
lp = (139 + 41.0 / 60 + 30.2 / 3600) * (pi / 180);
hp = 0.0;
xp = (r + hp) * cos(pp) * cos(lp);
yp = (r + hp) * cos(pp) * sin(lp);
zp = (r + hp) * sin(pp);

Ry = [cos((pi / 2) - pp), 0, -sin((pi / 2) - pp); 0, 1, 0; sin((pi / 2) - pp), 0, cos((pi / 2) - pp)];
Rz = [cos(lp), sin(lp), 0; -sin(lp), cos(lp), 0; 0, 0, 1];

N = [];
E = [];
U = [];
Az = [];
El = [];
T2 = [];
Zenith = [];
for i = 1:length(Xs)
    X = [Xs(i) - xp; Ys(i) - yp; Zs(i) - zp];
    Ans = Ry * Rz * X;
    N = [N, -Ans(1)];
    E = [E, Ans(2)];
    U = [U, Ans(3)];
    Az = [Az, atan2(E(i), N(i))];
    El = [El, atan2(U(i), sqrt(E(i)^2 + N(i)^2))];
    Zenith = [Zenith, ((pi / 2) - El(i)) / (pi / 180)];
end

x = [];
y = [];
S = [];
for i = 1:length(Zenith)
    if Zenith(i) >= 0 && Zenith(i) <= 80
        T2 = [T2, T(i)];
        x = [x, E(i)];
        y = [y, N(i)];
        S = [S, El(i)];
    end
end

for i = 1:length(x)
    plot(x(i), y(i), 'b^', 'Markersize', 5 + 20 * S(i) / (pi / 180) / 90, 'MarkerFaceColor','b');
end

for i = 1:length(T2)
    if (mod(T2(i), 3600) == 0)
        text(x(i), y(i), ['\leftarrow', num2str(10 + (T2(i) / 3600))], 'FontSize', 20);
    end
end
plot(0, 0, 'ro', 'Markersize', 5)
text(0, 0, '\rightarrowStation', 'FontSize', 20);
    



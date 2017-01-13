function [Xs, Ys, Zs, S, Sr] = getNewObs(X, Y, Z, pp, lp, hp, satfile, rngfile, R)
xp = (R + hp) * cos(pp) * cos(lp);
yp = (R + hp) * cos(pp) * sin(lp);
zp = (R + hp) * sin(pp);

%Read 1m random error for satellite
fin = fopen(satfile);
c = textscan(fin, '%f%f%f');
fclose(fin);
[Xer, Yer, Zer] = c{1, 1:3};

%Read 0.2m random error for range
fin = fopen(rngfile);
c = textscan(fin, '%f');
fclose(fin);
dS = c{1, 1};

%Xer = Xer - Xer;
%Yer = Yer - Yer;
%Zer = Zer - Zer;
%dS = dS - dS;

Xs = X + Xer;
Ys = Y + Yer;
Zs = Z + Zer;
S = ((X - xp).^2 + (Y - yp).^2 + (Z - zp).^2).^0.5;
Sr = S + dS;

%Write out data
%fout = fopen('result1.txt', 'w');
%fprintf(fout, 'Obs_ID\tS (m)\tSr (m)\tXs (m)\tYs (m)\tZs (m)\n');
%for i = 1:length(Xs)
%    fprintf(fout, 'OBS%02d\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n', i, S(i), Sr(i), Xs(i), Ys(i), Zs(i));
%end
%fclose(fout);
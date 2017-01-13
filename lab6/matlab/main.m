format long g;

%Read xp3 file
fin1 = fopen('igs17864.sp3');
tline = fgets(fin1);
%Define prn name
Prn = 'PG31';

%Define radius (km)
r = 6371.0;

%Define numbers of data
dataNum = 192;

fin = fopen('igs17864.sp3');
%Scan file1
c = textscan(fin, '%s%f%f%f%f%d', 'headerLines', 22);
coords = [c{1,2}(strcmp(Prn, c{1,1})), c{1,3}(strcmp(Prn, c{1,1})), c{1,4}(strcmp(Prn, c{1,1}))];
times = [c{1,2}(strcmp('*', c{1,1})), c{1,3}(strcmp('*', c{1,1})), c{1,4}(strcmp('*', c{1,1})), c{1,5}(strcmp('*', c{1,1})),c{1,6}(strcmp('*', c{1,1}))];
fclose(fin);

fin2 = fopen('igs17865.sp3');
%Scan file2
c = textscan(fin2, '%s%f%f%f%f%d', 'headerLines', 22);
coords = [coords; [c{1,2}(strcmp(Prn, c{1,1})), c{1,3}(strcmp(Prn, c{1,1})), c{1,4}(strcmp(Prn, c{1,1}))]];
times = [times; [c{1,2}(strcmp('*', c{1,1})), c{1,3}(strcmp('*', c{1,1})), c{1,4}(strcmp('*', c{1,1})), c{1,5}(strcmp('*', c{1,1})),c{1,6}(strcmp('*', c{1,1}))]];
fclose(fin2);

year = times(:,1);
mon = times(:,2);
day = times(:,3);
hour = times(:,4);
min = times(:,5);
x = coords(:,1);
y = coords(:,2);
z = coords(:,3);

%Calculate coordinates of inerital reference system in first day
%Start from 2014/04/3 00:00:00, Julian Day is 2456750.5, time offset is 15
%minutes, End with 2014/04/4 23:45:00
t = 2456750.5 * 86400;
offset = 15.0 * 60;

T = zeros(dataNum, 1); GST_DMS = zeros(dataNum, 1);
X = zeros(dataNum, 1); Y = zeros(dataNum, 1); Z = zeros(dataNum, 1);
count = 1;
for i = t:offset:t + offset * (dataNum - 1)
    hms = degrees2dms(getGst(i) / 3600);
    T(count) = i / 86400;
    GST_DMS(count) = (hms(1) * 60^2 + hms(2) * 60 + hms(3)) * (360.0 / 86400);
    Rz = [cosd(-GST_DMS(count)), sind(-GST_DMS(count)), 0; -sind(-GST_DMS(count)), cosd(-GST_DMS(count)), 0; 0, 0, 1];
    XYZ = Rz * [x(count); y(count); z(count)];
    X(count) = XYZ(1);
    Y(count) = XYZ(2);
    Z(count) = XYZ(3);
    count = count + 1;
end

%Write out data
fout = fopen('result.txt', 'w');
fprintf(fout, 'Time(YYYY-MM-DD HH:MM:SS)\tJD(day)\tPRN\tXin(km)\tYin(km)\tZin(km)\tx(km)\ty(km)\tz(km)\n');
for i = 1:dataNum
    fprintf(fout, '%04d-%02d-%02d %02d:%02d:00\t%.8f\t%s\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n', year(i), mon(i), day(i), hour(i), min(i), T(i), Prn, X(i), Y(i), Z(i), x(i), y(i), z(i))
end
fclose(fout);

l = zeros(dataNum, 3); p = zeros(dataNum, 3); h = zeros(dataNum, 3);
%ECEF coordinate frame to spherical refrence frame
for i = 1:dataNum
    l(i, :) = degrees2dms(rad2deg(atan2(y(i), x(i))));
    p(i, :) = degrees2dms(rad2deg(atan2(z(i), sqrt(x(i)^2 + y(i)^2))));
    h(i, :) = sqrt(x(i)^2 + y(i)^2 + z(i)^2) - r;
end

%Write out data
fout = fopen('result2.txt', 'w');
fprintf(fout, 'Time(YYYY-MM-DD HH:MM:SS)\tJD(day)\tlon(deg)\tlon(min)\tlon(sec)\tlat(deg)\tlat(min)\tlat(sec)\tH(km)\n');
for i = 1:dataNum
    fprintf(fout, '%04d-%02d-%02d %02d:%02d:00\t%.8f\t%d\t%d\t%.6f\t%d\t%d\t%.6f\t%.6f\n', year(i), mon(i), day(i), hour(i), min(i), T(i), l(i, 1), l(i, 2), l(i, 3), p(i, 1), p(i, 2), p(i, 3), h(i));
end
fclose(fout);

hold on;
plot3(x, y, z, 'bx');
plot3(X, Y, Z, 'rx');
hold off;


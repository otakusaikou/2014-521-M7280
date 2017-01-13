format long g;

%Start from 1992/3/31 00:00:00, Julian Day is 2456658.5, time offset is 10
%minutes, End with 1992/4/3 00:00:00
t = 2448712.5 * 86400;
offset = 10.0 * 60;

%For debug
%t = 2454100.5;
%offset = 1;

index = 1;
T = zeros(432, 1); h = zeros(432, 1); m = zeros(432, 1); s = zeros(432, 1);
D = zeros(432, 1); M = zeros(432, 1); S = zeros(432, 1);
GST_DMS = zeros(432, 1);GST_HMS = zeros(432, 1);
minute = 0;

for i = t:offset:t + (3 * 86400) + offset
    hms = DEGREES2DMS(getGst(i) / 3600);
    dms = DEGREES2DMS((hms(1) * 60^2 + hms(2) * 60 + hms(3)) * (360.0 / 86400));
    GST_HMS(index) = getGst(i) / 3600;
    GST_DMS(index) = (hms(1) * 60^2 + hms(2) * 60 + hms(3)) * (360.0 / 86400);
    T(index) = minute;
    h(index) = hms(1);
    m(index) = hms(2);    
    s(index) = hms(3);
    D(index) = dms(1);
    M(index) = dms(2);
    S(index) = dms(3);
    index = index + 1;
    minute = minute + 10;
end

output1 = [T, D, M, S, h, m, s];
%Write out data
fout = fopen('result1.txt', 'w');
fprintf(fout, 'time (min)\tGST (deg)\tGST (min)\tGST (sec)\tGST (hour)\tGST (min)\tGST (sec)\n');
for i = 1:433
    fprintf(fout, '%i\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n', T(i), D(i), M(i), S(i), h(i), m(i), s(i));
end
fclose(fout);
%hold on;
%fclose(fout);
%plot(T, GST_DMS, 'b');
%plot(T, GST_HMS, 'g');
%hold off;

%Generate an ECEF coordinates (The second point in lab2)
p = -50.0;
l = 30.0;
he = 0;
a = 6378137.0; %meter
f = 1.0/298.257222101;
b = a - a * f;
e0 = sqrt((a^2 - b^2) / a^2);
%Calculate ECEF coordinates
N = a / sqrt(1 - e0^2 * sind(p)^2);
x = (N + he) * cosd(p) * cosd(l);
y = (N + he) * cosd(p) * sind(l);
z = (N * (1 - e0^2) + he) * sind(p);

%Calculate coordinates of inerital reference system in first day
X = zeros(145, 1); Y = zeros(145, 1); Z = zeros(145, 1);
x2 = zeros(145, 1); y2 = zeros(145, 1); z2 = zeros(145, 1);

for i = 1:145
    %Rotate matrix
    Rz = [cosd(-GST_DMS(i)), sind(-GST_DMS(i)), 0; -sind(-GST_DMS(i)), cosd(-GST_DMS(i)), 0; 0, 0, 1];
    XYZ = Rz * [x; y; z];
    X(i) = XYZ(1);
    Y(i) = XYZ(2);
    Z(i) = XYZ(3);
    x2(i) = x;
    y2(i) = y;
    z2(i) = z;
end

output2 = [h(1:145), m(1:145), s(1:145), x2, y2, z2, X, Y, Z];
%Write out data
fout = fopen('result2.txt', 'w');
fprintf(fout, 'GST (hour)\tGST min)\tGST (sec)\tx (m)\ty (m)\tz (m)\tX (m)\tY (m)\tZ (m)\n');
for i = 1:145
    fprintf(fout, '%.4f\t%.4f\t%.4f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n', h(i), m(i), s(i), x2(i), y2(i), z2(i), X(i), Y(i), Z(i));
end
fclose(fout);
%plot3(X, Y, Z, 'bx');
    
    





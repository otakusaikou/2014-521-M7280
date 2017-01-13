clc;
format long g;

%Define prn name
Prn = 'PRN-31';

%Define constants
r = 6371000.0;
ST_SEC = 86164.09053;
dataNum = 577;
omegae = pi * 2 / ST_SEC; %Rotation rate of earth

%Read yuma file, referenced from http://www.navcen.uscg.gov/?pageName=gpsAlmanacs
%Week number 767 stand from weeks start from 22 Aug 1999 00:00:00 (Julian day is 2451412.5)  
text = fileread('current.alm');
lines = regexp(text, '\n', 'split');

for i=1:15:length(lines)
    header = regexp(lines(i), ' ', 'split');
    if strcmp(header{1, 1}(6), Prn)
       disp(header{1, 1}(6));
       data = regexp(lines(i+3:i+14), ' ', 'split');
       
       e0 = str2num(cell2mat(data{1,1}(length(data{1, 1})))); %Eccentricity of satellite orbit
       toa = str2num(cell2mat(data{1,2}(length(data{1, 2})))); %Time of Applicability (second start from gps week)
       I = str2num(cell2mat(data{1,3}(length(data{1, 3})))); %Obital Incilination
       omegadot = str2num(cell2mat(data{1,4}(length(data{1, 4})))); %Rate of right ascen
       a = (str2num(cell2mat(data{1,5}(length(data{1, 5})))))^2; %Length of major-axis of satellite orbit
       aw = str2num(cell2mat(data{1,6}(length(data{1, 6})))); %Right ascen at week (GASTweek - omegatoa)
       lomega = str2num(cell2mat(data{1,7}(length(data{1, 7})))); %Argument of perigee (little omega)
       mt0 = str2num(cell2mat(data{1,8}(length(data{1, 8})))); %Mean anomaly of toa
       break;
    end
end

x = zeros(dataNum, 1); y = zeros(dataNum, 1); z = zeros(dataNum, 1);
XIN = zeros(dataNum, 1); YIN = zeros(dataNum, 1); ZIN = zeros(dataNum, 1);
T = zeros(dataNum, 1); 

count = 1;
for t = 0:300:172801
    %Get current Geodetic longitude of satellite
    omega = aw + omegadot * (t - toa) - omegae * t;
    
    %Get eccentric argument of perigee
    E = getE(e0, toa, a, mt0, t);
    
    %Coordinates in 2D satellite-earth coordinate system
    Xw = a * cos(E) - a * e0;
    Yw = a * sqrt(1 - e0^2) * sin(E);
    Zw = 0;
    
    %Get GST at t second
    hms = degrees2dms(getGst(2451412.5 * 86400 + 767 * 7 * 86400 + t) / 3600);
    T(count) = t;
    GST = (hms(1) * 60^2 + hms(2) * 60 + hms(3)) * (360.0 / 86400);
    disp(GST);
    %Rotation matrix
    Rz = [cos(-lomega), sin(-lomega), 0; -sin(-lomega), cos(-lomega), 0; 0, 0, 1];
    Rx = [1, 0, 0; 0, cos(-I), sin(-I); 0, -sin(-I), cos(-I)];
    Rz2 = [cos(-omega), sin(-omega), 0; -sin(-omega), cos(-omega), 0; 0, 0, 1];
    Rz3 = [cosd(-GST), sind(-GST), 0; -sind(-GST), cosd(-GST), 0; 0, 0, 1];

    X = [Xw; Yw; Zw];
    ECEF = Rz2 * Rx * Rz * X;
    IN = Rz3 * ECEF;
    
    x(count) = ECEF(1);
    y(count) = ECEF(2);
    z(count) = ECEF(3);
    
    XIN(count) = IN(1);
    YIN(count) = IN(2);
    ZIN(count) = IN(3);
    
    count = count + 1;
end

%Write out data
fout = fopen('result.txt', 'w');
fprintf(fout, 'Time(sec)\tXin(m)\tYin(m)\tZin(m)\tx(m)\ty(m)\tz(m)\n');
for i = 1:dataNum
    fprintf(fout, '%d\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n', T(i), XIN(i), YIN(i), ZIN(i), x(i), y(i), z(i))
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
fprintf(fout, 'Time(sec)\tlon(deg)\tlon(min)\tlon(sec)\tlat(deg)\tlat(min)\tlat(sec)\tH(m)\n');
for i = 1:dataNum
    fprintf(fout, '%d\t%d\t%d\t%.6f\t%d\t%d\t%.6f\t%.6f\n', T(i), l(i, 1), l(i, 2), l(i, 3), p(i, 1), p(i, 2), p(i, 3), h(i));
end
fclose(fout);

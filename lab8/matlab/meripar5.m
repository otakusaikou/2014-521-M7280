function meripar5(method)
fin = fopen('MERIPAR5.dat');
%scan land file
c = textscan(fin, '%d%f%f');
[tag, lat, lon] = c{1, 1:3};
lat = lat / 100 / 0.6;
lon = lon / 100 / 0.6;
if strcmp(method, 'mercator') || strcmp(method, 'mercator2')
    for i = 1:length(lat)
        if lat(i) > 89.5
            lat(i) = 89.5;
        end
        if lat(i) < -89.5
            lat(i) = -89.5;
        end
        lat(i) = 180.0/pi*log(tan(pi/4.0+lat(i)*(pi/180.0)/2.0));
    end
end
fclose(fin);

threshold = 160;

start = 1;
for i = 1:length(lat) - 1
    if sqrt((lon(i) - lon(i + 1))^2 + (lat(i) - lat(i + 1))^2) > threshold
        plot(lon(start:i), lat(start:i), 'color', [0.5 0.5 0.5]);
        start = i + 1;
    end
end
if start == 1
    plot(lon, lat, 'color', [0.5 0.5 0.5]);
else
    plot(lon(start:length(lat)), lat(start:length(lat)), 'color', [0.5 0.5 0.5]);
end

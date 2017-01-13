function coast(method)
fin = fopen('COAST4.dat');
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

x = [];
y = [];
threshold = 50;
for i = 1:length(lat)
    if tag(i) == 3 && i ~= 1
        start = 1;
        for j = 1:length(x) - 1
            if sqrt((x(j) - x(j + 1))^2 + (y(j) - y(j + 1))^2) > threshold
                plot(x(start:j), y(start:j));
                start = j + 1;
            end
        end
        if (start == 1)
            plot(x, y);
        end
        x = [];
        y = [];
    end
    x = [x, lon(i)];
    y = [y, lat(i)];
end
start = 1;
for j = 1:length(x) - 1
    if sqrt((x(j) - x(j + 1))^2 + (y(j) - y(j + 1))^2) > threshold
        plot(x(start:j), y(start:j));
        start = j + 1;
    end
end
if (start == 1)
    plot(x, y);
end
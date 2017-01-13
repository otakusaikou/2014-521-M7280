function drawSat(method, T2)
fin = fopen('result.txt');
%scan satellite position file
c = textscan(fin, '%d%f%f%f%f%f%f', 'headerLines', 1);
[Xs, Ys, Zs] = c{1, 5:7};
T = c{1, 1};
fclose(fin);

lon = [];
lat = [];
for i = 1:length(Xs)
    lon = [lon, atan2(Ys(i), Xs(i)) / (pi / 180)];
    lat = [lat, atan2(Zs(i), sqrt(Ys(i)^2 + Xs(i)^2)) / (pi / 180)];
end

if strcmp(method, 'mercator')
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


if T2 ~= 0
	for i = 1:length(T)
        if any(T(i) == T2)
            plot(lon(i), lat(i), 'b*');
        else
            plot(lon(i), lat(i), 'r*');
        end
        
        if (mod(T(i), 3600) == 0)
            text(lon(i), lat(i), ['\leftarrow', num2str(10 + (T(i) / 3600))]);
        end
        
    end
    pp = (35 + 41.0 / 60 + 22.4 / 3600);
    lp = (139 + 41.0 / 60 + 30.2 / 3600);
    if strcmp(method, 'mercator')
        pp = 180.0/pi*log(tan(pi/4.0+pp*(pi/180.0)/2.0));
    end
    plot(lp, pp, 'ro', 'Markersize', 5)   
    text(lp, pp, '\rightarrowStation');
else
    for i = 1:length(T)
        if (mod(T(i), 3600) == 0)
            text(lon(i), lat(i), ['\leftarrow', num2str(10 + (T(i) / 3600))]);
        end
    end
    plot(lon, lat, 'r*');
end
function [xo, yo, zo, Pt_ID] = gendata(r)
xo = zeros(50, 1); yo = zeros(50, 1); zo = zeros(50, 1); Pt_ID = zeros(50, 1);
index = 1;
for i = 30:60:330
    for j = -70:20:70
        [xo(index), yo(index), zo(index)] = lph2xyz(i * (pi / 180), j * (pi / 180), 0, r);
        Pt_ID(index) = index;
        index = index + 1;
    end
end

Pt_ID(49) = 49;
Pt_ID(50) = 50;
[xo(49), yo(49), zo(49)] = lph2xyz(0 * (pi / 180), 90 * (pi / 180), 0, r);
[xo(50), yo(50), zo(50)] = lph2xyz(0 * (pi / 180), -90 * (pi / 180), 0, r);

%ECEF coordinate frame to spherical refrence frame
l = zeros(50, 1); p = zeros(50, 1); h = zeros(50, 1);
for i = 1:50
    [l(i), p(i), h(i)] = xyz2lph(xo(i), yo(i), zo(i), r);
end

%Write data
fout = fopen('resultOfPart1a.txt', 'w');
fprintf(fout, 'Pt_ID\tLatitude\tLongtitude\tHeight\n');
for i = 1:50
    fprintf(fout, '%i\t%.12f\t%.12f\t%.12f\n', Pt_ID(i), p(i), l(i), h(i));
end
fclose(fout)
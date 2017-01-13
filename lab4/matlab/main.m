%%%Part1%%%
%create ECEF points
a = 6378137.0;
f = 1.0/298.257222101;
b = a - a * f;
e0 = sqrt((a^2 - b^2) / a^2);
[xo, yo, zo, Pt_ID] = gendata(a, e0);

%plot3(xo, yo, zo, 'bx');

%%Part1a%%
%ECEF coordinate frame to elliposidal refrence frame
l = zeros(50, 1); p = zeros(50, 1); h = zeros(50, 1);
for i = 1:50
    [l(i), p(i), h(i)] = xyz2lph(xo(i), yo(i), zo(i), a, e0);
end

%%Part1b%%
%ECEF coordinate frame to cartesian reference frame
e = zeros(50, 1); n = zeros(50, 1); u = zeros(50, 1);
for i = 1:50
    [e(i), n(i), u(i)] = xyz2enu(xo(i), yo(i), zo(i), xo(1), yo(1), zo(1), a, e0);
end

%%Part1c%%
%cartesian reference frame to topocentric coordinate frame
Az = zeros(50, 1); El = zeros(50, 1); Sr = zeros(50, 1);
for i = 1:50
    [Az(i), El(i), Sr(i)] = enu2topo(e(i), n(i), u(i));
end

%cartesian reference frame to ECEF coordinates frame
%x_2 = zeros(50, 1); y_2 = zeros(50, 1); z_2 = zeros(50, 1);
%for i = 1:50
%    [x_2(i), y_2(i), z_2(i)] = enu2xyz(n(i), e(i), u(i), xo(1), yo(1), zo(1), r);
%end

%topocentric coordinate frame to topocentric coordinate frame
%e_2 = zeros(50, 1); n_2 = zeros(50, 1); u_2 = zeros(50, 1);
%for i = 1:50
%    [e_2(i), n_2(i), u_2(i)] = topo2enu(Az(i), El(i), Sr(i));
%end

format long g;
output = [Pt_ID, xo, yo, zo, p, l, h, e, n, u, Az, El, Sr];

%hold on;
%plot3(xo, yo, zo, 'bx');
%plot3(e, n, u, 'rx');
%xlabel('x');
%ylabel('y');
%zlabel('z');
%hold off;

%disp(output);

%%%Part1 END%%%
%%%Part2%%%

%read data
%[Pt_ID, p, l, h] = readdata;

%elliposidal refrence frame to ECEF coordinate frame
x = zeros(50, 1); y = zeros(50, 1); z = zeros(50, 1);
for i = 1:50
    [x(i), y(i), z(i)] = lph2xyz(l(i), p(i), h(i), a, e0);
end

output2 = [Pt_ID, xo, yo, zo, p, l, h, x, y, z];
%disp(output2)

test_p = (64 + 1.0 / 60 +  45.33240 / 3600) * (pi / 180);
test_l = (-(142 + 4.0 / 60 + 32.94873 / 3600)) * (pi / 180);
test_he = 745.09;
[outx, outy, outz] = lph2xyz(test_l, test_p, test_he, a, e0);


%%%Part2 END%%%

fout2 = fopen('13col.txt', 'w');
fout3 = fopen('10col.txt', 'w');
fprintf(fout2, 'Pt_ID\txo (m)\tyo (m)\tzo (m)\tlat (rad)\tlon (rad)\the (m)\te (m)\tn (m)\tu (m)\tAz (rad)\tEl (rad)\tSr (m)\n');
fprintf(fout3, 'Pt_ID\txo (m)\tyo (m)\tzo (m)\tlat (rad)\tlon (rad)\the (m)\tx (m)\ty (m)\tz (m)\n');
for i = 1:50
    fprintf(fout2, '%i\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t\n', Pt_ID(i), xo(i), yo(i), zo(i), p(i), l(i), h(i), e(i), n(i), u(i), Az(i), El(i), Sr(i));
    fprintf(fout3, '%i\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t\n', Pt_ID(i), xo(i), yo(i), zo(i), p(i), l(i), h(i), x(i), y(i), z(i));
end
fclose(fout2)
fclose(fout3)






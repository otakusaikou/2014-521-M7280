%%%Part1%%%
%create ECEF points
r = 6371.0;
[xo, yo, zo, Pt_ID] = gendata(r);

%plot3(xo, yo, zo, 'bx');

%%Part1a%%
%ECEF coordinate frame to spherical refrence frame
l = zeros(50, 1); p = zeros(50, 1); h = zeros(50, 1);
for i = 1:50
    [l(i), p(i), h(i)] = xyz2lph(xo(i), yo(i), zo(i), r);
end

%%Part1b%%
%ECEF coordinate frame to cartesian reference frame
e = zeros(50, 1); n = zeros(50, 1); u = zeros(50, 1);
for i = 1:50
    [n(i), e(i), u(i)] = xyz2enu(xo(i), yo(i), zo(i), xo(1), yo(1), zo(1), r);
end

%%Part1c%%
%cartesian reference frame to topocentric coordinate frame
Az = zeros(50, 1); El = zeros(50, 1); Sr = zeros(50, 1);
for i = 1:50
    [Az(i), El(i), Sr(i)] = enu2topo(n(i), e(i), u(i));
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
%hold off;

%disp(output);

%%%Part1 END%%%
%%%Part2%%%

%read data
%[Pt_ID, p, l, h] = readdata;

%spherical refrence frame to ECEF coordinate frame
x = zeros(50, 1); y = zeros(50, 1); z = zeros(50, 1);
for i = 1:50
    [x(i), y(i), z(i)] = lph2xyz(l(i), p(i), h(i), r);
end

output2 = [Pt_ID, xo, yo, zo, x, y, z];
%disp(output2)

%%%Part2 END%%%




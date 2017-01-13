%GRS67 ellipsodial parameter values
a_67 = 6378160.0;
f_67 = 1.0 / 298.247167427;
b_67 = a_67 - a_67 *f_67;
e_67 = sqrt((a_67^2 - b_67^2) / (a_67^2));

%GRS80 ellipsodial parameter values
a_80 = 6378137.0;
f_80 = 1.0 / 298.257222101;
b_80 = a_80 - a_80 *f_80;
e_80 = sqrt((a_80^2 - b_80^2) / (a_80^2));

Latitude = zeros(181, 1);
M_67 = zeros(181, 1); N_67 = zeros(181, 1); Ravg_67 = zeros(181, 1); RG_67 = zeros(181, 1);
M_80 = zeros(181, 1); N_80 = zeros(181, 1); Ravg_80 = zeros(181, 1); RG_80 = zeros(181, 1);
index = 1;
for i = -90:1:90
    Latitude(index, 1) = i;
    M_67(index, 1) = (a_67 * (1 - e_67^2)) / (1 - e_67^2 * (sin(i * (pi / 180)))^2)^(3.0 / 2.0);
    N_67(index, 1) = a_67 / sqrt(1 - e_67^2 * (sin(i * (pi / 180)))^2);
    Ravg_67(index, 1) = (M_67(index, 1) + N_67(index, 1)) / 2.0;
    RG_67(index, 1) = sqrt(M_67(index, 1) * N_67(index, 1));
    M_80(index, 1) = (a_80 * (1 - e_80^2)) / (1 - e_80^2 * (sin(i * (pi / 180)))^2)^(3.0 / 2.0);
    N_80(index, 1) = a_80 / sqrt(1 - e_80^2 * (sin(i * (pi / 180)))^2);
    Ravg_80(index, 1) = (M_80(index, 1) + N_80(index, 1)) / 2.0;
    RG_80(index, 1) = sqrt(M_80(index, 1) * N_80(index, 1));
    index = index + 1;
end

format long g
A = [Latitude, M_67, N_67, Ravg_67, RG_67, M_80, N_80, Ravg_80, RG_80];
disp(A);

%hold on;
%plot(Latitude, M_80);
%plot(Latitude, N_80);
%plot(Latitude, Ravg_80);
%plot(Latitude, RG_80);
%hold off;

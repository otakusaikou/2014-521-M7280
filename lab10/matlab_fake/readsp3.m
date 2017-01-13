function [T, X, Y, Z] = readsp3(filenames, SID)
X = [];
Y = [];
Z = [];
dt = [];
T = [];
for i = 1:3
fin = fopen(filenames{1, i});
c = textscan(fin, '%s%f%f%f%f%d', 'headerLines', 22);
coords = [c{1,2}(strcmp(SID, c{1,1})), c{1,3}(strcmp(SID, c{1,1})), c{1,4}(strcmp(SID, c{1,1}))];
X = [X; coords(:,1) * 1000];
Y = [Y; coords(:,2) * 1000];
Z = [Z; coords(:,3) * 1000];
T = [T; [c{1,5}(strcmp('*', c{1,1})) * 3600 + double(c{1,6}(strcmp('*', c{1,1})) * 60)] - 86400 * (2 - i)];
fclose(fin);
end

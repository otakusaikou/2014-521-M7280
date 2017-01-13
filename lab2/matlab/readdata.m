function [Pt_ID, p, l, h] = readdata
impt = importdata('resultOfPart1a.txt');
data = impt.data;
Pt_ID = transpose(data(1:50));
p = transpose(data(51:100));
l = transpose(data(101:150));
h = transpose(data(151:200));

disp(h);
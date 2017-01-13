format long g;
fin = fopen('result.txt');
%Scan file1
c = textscan(fin, '%d%f%f%f%f%f%f', 'headerLines', 1);
[Xs, Ys, Zs] = c{1, 5:7};
Xs = Xs / 1000;
fclose(fin);
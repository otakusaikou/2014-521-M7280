clc;
%set constant
R = 6371000.0;


%draw map 1, with Platte Carree Projection
figure;
axis equal;
axis([-190 190 -100 100]);
set(gca, 'xtick', -195:15:195);
set(gca, 'ytick', -90:15:90);
grid on;
hold on;
coast('platte');
meripar5('platte');
drawSat('platte', 0);
xlabel('x (deg)');
ylabel('y (deg)');
hold off;



%draw map 2, with Mercator Projection
figure;
axis equal;
axis([-190 190 -180 180]);
set(gca, 'xtick', -195:15:195);
set(gca, 'ytick', -180:15:180);
grid on;
hold on;
coast('mercator');
meripar5('mercator');
drawSat('mercator', 0);
xlabel('x (deg)');
ylabel('y (deg)');
hold off;



%draw skyplot
fHand = figure;
aHand = axes('parent', fHand);

%set the range start from 0 to 100
polar(0,100,'-k');
hold on;

%plot satellite
T2 = skyplot1(R);

%relabeling
pHand = polar(0, 100, 'parent', aHand);
delete(pHand);

hands = findall(fHand,'parent', aHand, 'Type', 'text');
hands = hands(strncmp('  ', get(hands,'String'), 2));
hands = sort(hands);

%relabel from inside out.
labels = {'80', '60', '40', '20'};
for i = 1:4
  set(hands(i),'String', labels{i})
end

view([90 -90]);
hold off;


%draw new skyplot
figure;
hold on
grid on;
skyplot2(R);
xlabel('E (m)');
ylabel('N (m)');
hold off;

%draw map 3, with Platte Carree Projection
figure;
axis equal;
axis([-190 190 -100 100]);
set(gca, 'xtick', -195:15:195);
set(gca, 'ytick', -90:15:90);
grid on;
hold on;
coast('platte');
meripar5('platte');
drawSat('platte', T2);
xlabel('x (deg)');
ylabel('y (deg)');
hold off;


%draw map 4, with Mercator Projection
figure;
axis equal;
axis([-190 190 -180 180]);
set(gca, 'xtick', -195:15:195);
set(gca, 'ytick', -180:15:180);
grid on;
hold on;
coast('mercator');
meripar5('mercator');
drawSat('mercator', T2);
xlabel('x (deg)');
ylabel('y (deg)');
hold off;







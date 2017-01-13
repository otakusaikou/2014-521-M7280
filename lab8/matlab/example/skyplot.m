function skyplot(latR,lonR,altR,cutoff);

% SKYPLOT	Produces satellite skyplot from sp3 file.
%           Input:
%             sp3file = an orbit file in sp3 format
%             sv = vector of PRN numbers
%             latR, lonR, altR = ground site position (WGS)
%             cutoff = elevation cutoff angle in degrees
%
%		Call: skyplot(sp3file, sv, latR, lonR, altR, cutoff)

polar(0,90);
hold on;

disp(['-------------']);
disp(['Producing sky plot...']);

  % read sp3 file for satellite sv
  %[Xs,Ys,Zs,dT,Ts] = read_sp3(sp3file,sv(i));

  % convert sp3 to meters
  %Xs = Xs.*1000;
  %Ys = Ys.*1000;
  %Zs = Zs.*1000;
  fin = fopen('result.txt');
  %Scan file1
  c = textscan(fin, '%d%f%f%f%f%f%f', 'headerLines', 1);
  [Xs, Ys, Zs] = c{1, 5:7};
  fclose(fin);

  % matrix of satellite positions (ECEF, meters)
  S = [Xs Ys Zs];

  % convert reference site to ECEF
  [XR,YR,ZR] = wgs2xyz(139 + 41.0 / 60 + 30.2 / 3600,35 + 41.0 / 60 + 22.4 / 3600,0);

  % compute elevation angle, range, and azimuth
  [azim,elev,hlen] = azelle(S,[XR,YR,ZR]);

  % convert elevation to zenith angle
  zen_ang = (pi/2) - elev;

  % cutoff observations below cutoff angle
  cutoff = 0;
  cutoff = cutoff * pi/180;
  I = find(zen_ang<((pi/2)-cutoff));

  % sky plot
  polar(azim(I),zen_ang(I).*180/pi,'*b');
  view([90 -90]);
  %h = mmpolar(azim(I),zen_ang(I).*180/pi,'*b','TZeroDirection','North','RLimit',[0 90]);



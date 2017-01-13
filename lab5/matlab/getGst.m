function GST = getGst(t)
%this function calculates the Greenwich Sidereal Time with difference of
%Julian Day
%t (input) is the input Julian Time (sec)

%The initial Greenwich Sidereal Time is on 2006/12/31 00:00:00, using GMST
GST0 = 6 * 60^2 + 37 * 60 + 7.7912;

%t0 is the Julian Day on 2006/12/31
t0 = 2454100.5 * 86400;

%omega is the rotation speed of earth (second (time)/ second (angle))
omega = (360.0 / 86164.09053) * (86400 / 360.0);

GST = mod((GST0 + omega * (t - t0)), 86400);
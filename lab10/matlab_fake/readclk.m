function [T2, dt] = readsp3(filenames, SID)
count = 1;
T2 = []; 
dt = [];
for i = 1:3
    fin = fopen(filenames{1, i});   
    line = fgets(fin);
    while line ~= -1
        %check epoch lines
        if (isempty(strfind(line,SID)) == 0)
            dt = [dt;str2num(line(41:60))];      
        end    
        count = count+1; 
        line = fgets(fin);
    end
end

for i=-86400:30:172769
    T2 = [T2, i];
end
fclose(fin);
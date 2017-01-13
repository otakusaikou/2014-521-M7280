function [t, CA] = readrinex(filename, SID)
fin = fopen(filename);

count = 1;
t = []; 
CA = [];
for i=1:27
    line = fgets(fin);
end
while line ~= -1
    %check epoch lines
    if (isempty(strfind(line,' 14  5  4')) + isempty(strfind(line, 'G')) == 0)
        sats = regexp(line(31:length(line) - 1),'G','split');
        sats = sats(2:length(sats));
        tarr = regexp(line(11:27), ' ','split');
        tarr = cellfun(@str2num, tarr(strcmp(tarr, '') ~= 1));
        %find satellite index in observations
		ind = find(ismember(sats, SID));
		if isempty(ind) ~= 1   
            %skip (ind - 1) * 2 + 1 lines
            for i=1:((ind - 1) * 3 + 1)
                line = fgets(fin);
            end
            CA = [CA;str2num(line(51:64))];
            t = [t, tarr(1) * 3600 + tarr(2) * 60 + tarr(3)];
        end
        
    end    
    count = count+1; 
    line = fgets(fin);
end
fclose(fin);

function avg = computeAvg(data, episodeNum)
    len = length(data);
    %episodeNum = 100;
    diff = data(2:len) - data(1:len-1);
    diff(len) = diff(len-1);
    
    for i = 1:len/episodeNum
       avg(i) = mean(diff(1 + (i-1)*episodeNum:i*episodeNum));
    end
end

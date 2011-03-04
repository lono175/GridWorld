function [ start sumT ] = winsum( q )
windowSize = 900
coarse = 50
alpha = 0.01

sumT = [];
sumQ = sum(q(1:windowSize));
prev = sumQ;
sumT(1) = sumQ;
start = [];
start(1) = q(1);
for i = 2:length(q) - windowSize +1
sumQ = sumQ - q(i-1) + q(i+windowSize-1);
sumT(i) = (1-alpha)*prev + alpha*sumQ;
start(i) = start(i-1) + q(i);
prev = sumQ;
end

start = start / 10 / 3600;
sumT = sumT / 10 / 900;


start = start(1:coarse:length(start)); 
sumT = sumT(1:coarse:length(sumT));


end


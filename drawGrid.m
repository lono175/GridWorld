%load no_transfer.csv
%load transfer.csv
data = load('RRLXtestX8X6_10X40000X2_1X1.csv');
%load 4vs3tran.csv

q = [data(:, 1) data(:, 3)];
[start sumT] = gridSum(q);
 plot(start, sumT)
 %hold on;
 
%data = X4vs3no;
%q = data(:, 4);
%[start sumT] = winsum(q);
 %plot(start, sumT, 'r.-')
%axis([0 18 8 15])
xlabel('Training Time (hours)')
ylabel('Episode Duration (seconds)')
legend('With transfer', 'without transfer')

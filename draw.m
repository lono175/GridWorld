%load no_transfer.csv
%load transfer.csv
load 4vs3no.csv
load 4vs3tran.csv

data = X4vs3tran;
q = data(:, 4);
[start sumT] = winsum(q);
 plot(start, sumT)
 hold on;
 
data = X4vs3no;
q = data(:, 4);
[start sumT] = winsum(q);
 plot(start, sumT, 'r.-')
axis([0 18 8 15])
xlabel('Training Time (hours)')
ylabel('Episode Duration (seconds)')
legend('With transfer', 'without transfer')

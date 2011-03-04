
fileList10 = {'RRL_test_0__0__1__2', 'RRL_test_200__0__1__2', 'RRL_test_400__0__1__2', 'RRL_test_600__0__1__2','RRL_test_800__0__1__2', 'RRL_test_1000__0__1__2', 'RRL_test_1200__0__1__2', 'RRL_test_1400__0__1__2'}
%fileList1 = {'RRL_test_0_(0, 1)_2', 'RRL_test_200_(0, 1)_2', 'RRL_test_400_(0, 1)_2', 'RRL_test_600_(0, 1)_2','RRL_test_800_(0, 1)_2', 'RRL_test_1000_(0, 1)_2', 'RRL_test_1200_(0, 1)_2', 'RRL_test_1400_(0, 1)_2'}
%fileList2 = {'SarsaComp0', 'SarsaComp400', 'SarsaComp800', 'SarsaComp1200', 'SarsaComp1600', 'SarsaComp2000', 'SarsaComp2400', 'SarsaComp2800'}

reward = [];
fileList = fileList1;
for i = 1:length(fileList)
    name = char(fileList(i))
    filename = [name '.csv']
    load(filename)
    name2 = char(fileList10(i))
    eval(['data = ' name2 ';'])
    reward(1, i) = data(length(data)-1)/100
end

fileList = fileList2;
for i = 1:length(fileList)
    name = char(fileList(i))
    filename = [name '.csv']
    load(filename)
    name2 = char(fileList(i))
    eval(['data = ' name2 ';'])
    reward(2, i) = data(length(data)-1)/100
end
x = [0:400:2800]
bar(x, reward')
xlabel('# of training episodes')
ylabel(['average reward per episodes'])
legend('PTL', 'SARSA')
range = [-400 3200 -30 20]
axis(range)

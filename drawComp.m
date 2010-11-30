%fileList = {'conV', 'RRL_conv0', 'RRL_conv50', 'RRL_conv100', 'RRL_conv150'}
fileList = {'RRL_test_10000__0_1__1', 'RRL_test_5000__0_2__2', 'RRL_test_3333__0_3__3', 'RRL_test_10000__1_0__1','RRL_test_10000__2_0__1', 'RRL_test_3333__1_1__3', 'RRL_test_2000__2_1__5', 'RRL_test_2000__1_2__5'}
%fileList = {'RRL_test_3333__1_1__3', 'RRL_test_2000__2_1__5', 'RRL_test_2000__1_2__5'}
plotSpec = {'r-', 'g-', 'b-', 'r.-', 'g.-', 'r-+', 'g-+', 'b-+'}
episodeNum = 500;

for i = 1:length(fileList)
    name = char(fileList(i))
    filename = [name '.csv']
    load(filename)
    eval(['data = ' name ';'])
    avg = computeAvg(data, episodeNum);
    X = [episodeNum:episodeNum:length(avg)*episodeNum];
    plot(X, avg, char(plotSpec(i)))
    hold on
end
%load('conv.csv')
%SARSA = conv;
%load('RRL_conv.csv')
%RRL = RRL_conv;
%avg = computeAvg(data, episodeNum);
%plot(X, avg)
%hold on
%avg = computeAvg(SARSA, episodeNum);
%plot(X, avg, ':')

xlabel('# of testing episodes')
ylabel(['average reward per '  num2str(episodeNum) ' episodes'])
legend('1st food', '2nd food', '3th food', '1st monster', '2nd monster', '1st food and 1st monster', '1st food and 2nd monster', '2nd food and 1st monster')
range = [episodeNum length(avg)*episodeNum -30 200];
axis(range)

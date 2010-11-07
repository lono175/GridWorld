%fileList = {'conV', 'RRL_conv0', 'RRL_conv50', 'RRL_conv100', 'RRL_conv150'}
fileList = {'conv', 'RRL_conv150'}
plotSpec = {'-x', '-'}
episodeNum = 100;

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
legend('SARSA', 'PTL')
range = [episodeNum length(avg)*episodeNum -30 30];
axis(range)


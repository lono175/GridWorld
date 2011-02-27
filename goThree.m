gamma = 0.9;
coinR = 20;
preC = coinR*[gamma^4 gamma^3 gamma^2 gamma^1 gamma^0 gamma^1 gamma^2 gamma^3 gamma^3 gamma^2 gamma^1 gamma^0 gamma^1 gamma^2 gamma^3 gamma^4 ];
preC = [0 preC];
n = size(three, 1);
R = three(:, 1);
fea = [three(:, 2:6) three(:, 8:11)];
fea = [fea fea(:, 2:9)];
for i = 1:n
    if fea(i, 1) == 1
        fea(i, 10:17) = 0;
    else
        fea(i, 2:9) = 0;
    end
end
%fea = [fea(:, 2:17)];
fea(:, 1) = 1;
In = eye(n);
P = circshift(In, -1);
P(n, :) = 0;
D = In - gamma*P;
A = fea'*D*fea;
b = fea'*R;
w = A \ b;

p1 = fea*preC';
p2 = fea*w;
p3 = max((fea.*repmat(preC, n, 1))');
p4t = fea.*repmat(preC, n, 1)
p4t(find(p4t==0)) = coinR;
p4 = min(p4t');

X = [p1 p3' p4'];


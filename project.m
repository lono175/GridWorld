maxIter = 2000;
tol = 1e-8;
A3 = obList'*D*obList;
A4 = A3 + speye(8190)*0.1;
b4 = ones(8190,1);
[x1,flag,relres,iter, resvec] = gmres(A4, b4, [], tol, maxIter);

A5 = chol(D)*obList;
A6 = [A5; sqrt(0.1)*speye(8190)];
b6 = [ones(9999, 1); zeros(8190, 1)];
[x2,flag,relres1,iter1,resvec1, lsvec1] = lsqr(A6,b6,tol,maxIter);

semilogy(resvec/norm(b4), '-')
hold on;
semilogy(lsvec1/norm(b6), '--')
legend('GMRES', 'LSQR')
xlabel('# of iterations')
ylabel('relative residual')
%[x2,flag,relres1,iter1,resvec1] = lsqr(A6,b6,tol,maxIter);

%[x,flag,relres2,iter2,resvec2,resveccg2] = minres(A4, ones(8190,1), tol, maxIter);



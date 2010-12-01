function [Res, indexList] = removeCol(Mat)
    indexList = [];
    Res = [];
    index = 1;
    len = size(Mat, 2);
    %make a matrix full column rank
    for i = 1:len
        if min(Mat(:, i)) ~= max(Mat(:, i))
            Res(:, index) = Mat(:, i);
            index = index + 1;
            indexList = [indexList; i];
        end
    end
end

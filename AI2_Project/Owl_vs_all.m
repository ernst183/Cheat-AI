A = csvread('owl_vs_all.txt');
 A(:,3)=A(:,3)./500;
 
 for i=1:200
    A(i,4)=A (i,4)/(A(i,4)+A(i,5));
end

plot(A(2:10:200,2),A(2:10:200,4), 'r', 'LineWidth', 2);
hold on;
plot(A(4:10:200,2),A(4:10:200,4), 'b', 'LineWidth', 2);
plot(A(6:10:200,2),A(6:10:200,4), 'm', 'LineWidth', 2);
plot(A(8:10:200,2),A(8:10:200,4), 'g', 'LineWidth', 2);
plot(A(10:10:200,2),A(10:10:200,4), 'k', 'LineWidth', 2);


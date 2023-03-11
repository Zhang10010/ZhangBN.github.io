clc
clear

% Heart coordinates from MATLAB cubic spline tutorials
x = pi*linspace(0,2,11); 
y = [0 0 8 12 14 6 0 -6 -14 -12 -8 0 0; 
     5 5 7 10 14 16 14 16 14 10 7 5 5];
pp = spline(x,y);
yy = ppval(pp, linspace(0,2*pi,50));
plot(yy(1,:),yy(2,:),'-b',y(1,2:11),y(2,2:11),'or')
axis equal


% Putting all x and y together
x = yy(1,:);
y = yy(2,:);

L1=10;
L2=10;

% IK loop
% IK loop
for i = 1:length(x)
    
    % IK
    L3=sqrt(x(i)^2+y(i)^2);
    b1 = (-(L2^2-L1^2-L3^2)/(2*L1*L3));
    a1 = atan2(sqrt(1-b1^2),b1);
    theta1(i) = (atan2(y(i),x(i))-a1)*(180/pi);
    b2 = (-(L3^2-L1^2-L2^2)/(2*L1*L2));
    a2 = atan2(sqrt(1-b2^2),b2);
    theta2(i) = (pi-a2)*(180/pi);

    % Angles for motor movement
    if i > 1
        theta11(i) = theta1(i)-theta1(i-1);
        theta22(i) = theta2(i)-theta2(i-1);
    end
    theta11(1) = theta1(1);
    theta22(1) = theta2(1);

    % Animation
    clf
    X = [0 L1*cos(theta1(i)*(pi/180)) x(i)];
    Y = [0 L1*sin(theta1(i)*(pi/180)) y(i)];
    xlim([-16 16])
    ylim([-16 16])
    hold on
    plot(X,Y)

    % Debugging stuff
    L1_1 = sqrt((L1*cos(theta1(i)*(pi/180)))^2+(L1*sin(theta1(i)*(pi/180)))^2);
    L2_1 = sqrt((x(i)-L1*cos(theta1(i)*(pi/180)))^2+(y(i)-L1*sin(theta1(i)*(pi/180)))^2);
    fprintf('Theta1 %5.2f\n', theta1(i))
    fprintf('Theta2 %5.2f\n', theta2(i))
    fprintf('L1 %3.2f\n', L1_1)
    fprintf('L2 %3.2f\n', L2_1)
    fprintf('--------------------\n')

    pause(0.1)
end
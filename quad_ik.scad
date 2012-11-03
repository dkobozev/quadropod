include <quad_params.scad>;

// IK CALCULATION
x = 190.8;
y = 25;
z = -30;


theta1_ik1 = atan2(-x, y) + atan2(sqrt(x*x + y*y - pow(d3 + d2, 2)), d3 + d2);
theta1_ik2 = atan2(-x, y) - atan2(sqrt(x*x + y*y - pow(d3 + d2, 2)), d3 + d2);
theta1_ik = round(theta1_ik1*10) / 10;

ik_a = -4*a2*x*cos(theta1_ik) - 4*a2*y*sin(theta1_ik) + x*x*cos(2*theta1_ik) + 2*x*y*sin(2*theta1_ik) - y*y*cos(2*theta1_ik) + 2*pow(z - d1, 2) + 2*a2*a2 + x*x + y*y;
ik_b1 = (ik_a/2 - a3*a3 - a4*a4) / (2*a3*a4);
ik_b = round(ik_b1*1000000) / 1000000; // round to six places
theta3_ik1 = atan2(sqrt(1 - ik_b*ik_b), ik_b);
theta3_ik2 = atan2(-sqrt(1 - ik_b*ik_b), ik_b);
theta3_ik = round(theta3_ik1*10) / 10;

ik_c = a2 - (x*cos(theta1_ik) + y*sin(theta1_ik));
ik_d = -z + d1;
ik_e = a4*sin(theta3_ik);
theta2_ik1 = atan2(ik_c, ik_d) + atan2(sqrt(ik_c*ik_c + ik_d*ik_d - ik_e*ik_e), ik_e);
theta2_ik2 = atan2(ik_c, ik_d) - atan2(sqrt(ik_c*ik_c + ik_d*ik_d - ik_e*ik_e), ik_e);
theta2_ik = round(theta2_ik1*10) / 10;


echo("theta1, solution 1", theta1_ik1 - 360);
echo("theta1, solution 2", theta1_ik2 - 360);

echo("theta2, solution 1", theta2_ik1 - 360);
echo("theta2, solution 2", theta2_ik2 - 360);

echo("theta3, solution 1", theta3_ik1);
echo("theta3, solution 2", theta3_ik2);

echo();


// RENDER THE MANIPULATOR

theta1 = theta1_ik;
theta2 = theta2_ik;
theta3 = theta3_ik;
theta4 = 0;

include <quad_manipulator.scad>;

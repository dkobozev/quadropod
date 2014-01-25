// Rendering of a quadropod leg using Denavit-Hartenberg parameters.
//
// A notable point here is that the length a of link i has to be rendered with
// link i-1.

include <quad_params.scad>;

//theta1 = -120; // from 0 to -180
//theta2 = -45; // from -90 to 90
//theta3 = 160; // from 0 to 180
//theta4 = 0; // 0

//theta1 = 0; // from 0 to -180
//theta2 = 53; // from -90 to 90
//theta3 = 60; // from 0 to 180
//theta4 = 0; // 0

theta1 = 0; // from 0 to -180
theta2 = 53; // from -90 to 90
theta3 = 60; // from 0 to 180
theta4 = 0; // 0


// FORWARD KINEMATICS {{{

// complete matrix:
//    [
//     cos(theta1)*cos(theta2 + theta3),
//     -sin(theta1),
//     cos(theta1)*sin(theta2 + theta3),
//     a4*cos(theta1)*cos(theta2 + theta3) + a3*cos(theta1)*cos(theta2) - d3*sin(theta1) + a2*cos(theta1) - d2*sin(theta1)
//    ],
//    [
//     sin(theta1) * cos(theta2 + theta3),
//     cos(theta1),
//     sin(theta1)*sin(theta2 + theta3),
//     a4*sin(theta1)*cos(theta2 + theta3) + a3*sin(theta1)*cos(theta2) + d3*cos(theta1) + a2*sin(theta1) + d2*cos(theta1)
//    ],
//    [
//     -sin(theta2 + theta3),
//     0,
//     -cos(theta2 + theta3),
//     -a4*sin(theta2 + theta3) - a3*sin(theta2) + d1
//    ],
//    [ 0, 0, 0, 1]
px = a4*cos(theta1)*cos(theta2 + theta3) + a3*cos(theta1)*cos(theta2) - d3*sin(theta1) + a2*cos(theta1) - d2*sin(theta1);
py = a4*sin(theta1)*cos(theta2 + theta3) + a3*sin(theta1)*cos(theta2) + d3*cos(theta1) + a2*sin(theta1) + d2*cos(theta1);
pz = -a4*sin(theta2 + theta3) - a3*sin(theta2) + d1;

multmatrix(m = [
    [1, 0, 0, px],
    [0, 1, 0, py],
    [0, 0, 1, pz],
    [0, 0, 0, 1]
])
    color ([1.0, 0.0, 0.0]) sphere (r = 8, $fn = resolution);

// verify forward kinematic with openscad transforms - transform a green cube to the end effector position
rotate([alpha1, 0, 0]) translate([a1, 0, 0]) rotate([0, 0, theta1]) translate([0, 0, d1])
rotate([alpha2, 0, 0]) translate([a2, 0, 0]) rotate([0, 0, theta2]) translate([0, 0, d2])
rotate([alpha3, 0, 0]) translate([a3, 0, 0]) rotate([0, 0, theta3]) translate([0, 0, d3])
rotate([alpha4, 0, 0]) translate([a4, 0, 0]) rotate([0, 0, theta4]) translate([0, 0, d4])
    color ([0.0, 1.0, 0.0]) cube ([12, 12, 12], center=true);

echo();
echo("X", px);
echo("Y", py);
echo("Z", pz);
echo();

// }}} fk

// INVERSE MATRICES TEST {{{

// undo manipulator transformations to put a green cube at the origin
translate([0, 0, -d4]) rotate([0, 0, -theta4]) translate([-a4, 0, 0]) rotate([-alpha4, 0, 0])
translate([0, 0, -d3]) rotate([0, 0, -theta3]) translate([-a3, 0, 0]) rotate([-alpha3, 0, 0])
translate([0, 0, -d2]) rotate([0, 0, -theta2]) translate([-a2, 0, 0]) rotate([-alpha2, 0, 0])
translate([0, 0, -d1]) rotate([0, 0, -theta1]) translate([-a1, 0, 0]) rotate([-alpha1, 0, 0])
rotate([alpha1, 0, 0]) translate([a1, 0, 0]) rotate([0, 0, theta1]) translate([0, 0, d1])
rotate([alpha2, 0, 0]) translate([a2, 0, 0]) rotate([0, 0, theta2]) translate([0, 0, d2])
rotate([alpha3, 0, 0]) translate([a3, 0, 0]) rotate([0, 0, theta3]) translate([0, 0, d3])
rotate([alpha4, 0, 0]) translate([a4, 0, 0]) rotate([0, 0, theta4]) translate([0, 0, d4])
    color ([0.0, 1.0, 0.0]) cube ([12, 12, 12], center=true);


// product of inverse of first transform and final matrix
multmatrix(m = [
    [1, 0, 0, px*cos(theta1) + py*sin(theta1)],
    [0, 1, 0, -px*sin(theta1) + py*cos(theta1)],
    [0, 0, 1, pz - d1],
    [0, 0, 0, 1]
])
    crosshair();

// product of second, third and fourth transforms
multmatrix(m = [
    [1, 0, 0, a4*cos(theta2 + theta3) + a3*cos(theta2) + a2],
    [0, 1, 0, d3 + d2],
    [0, 0, 1, -a4*sin(theta2 + theta3) - a3*sin(theta2)],
    [0, 0, 0, 1]
])
    color ([1.0, 0.0, 0.0]) sphere (r = 8, $fn = resolution);

// verify with openscad transforms and green cube
translate([0, 0, -d1]) rotate([0, 0, -theta1]) translate([-a1, 0, 0]) rotate([-alpha1, 0, 0])
rotate([alpha1, 0, 0]) translate([a1, 0, 0]) rotate([0, 0, theta1]) translate([0, 0, d1])
rotate([alpha2, 0, 0]) translate([a2, 0, 0]) rotate([0, 0, theta2]) translate([0, 0, d2])
rotate([alpha3, 0, 0]) translate([a3, 0, 0]) rotate([0, 0, theta3]) translate([0, 0, d3])
rotate([alpha4, 0, 0]) translate([a4, 0, 0]) rotate([0, 0, theta4]) translate([0, 0, d4])
    color ([0.0, 1.0, 0.0]) cube ([12, 12, 12], center=true, $fn=resolution);


// product of inverse of first and second transforms and final matrix
multmatrix(m = [
    [1, 0, 0, cos(theta2)*(px*cos(theta1) + py*sin(theta1)) - sin(theta2)*(pz - d1) - a2*cos(theta2)],
    [0, 1, 0, -sin(theta2)*(px*cos(theta1) + py*sin(theta1)) - cos(theta2)*(pz - d1) + a2*sin(theta2)],
    [0, 0, 1, -px*sin(theta1) + py*cos(theta1) - d2],
    [0, 0, 0, 1]
])
    crosshair();

// product of third and fourth transforms
multmatrix(m = [
    [1, 0, 0, a4*cos(theta3) + a3],
    [0, 1, 0, a4*sin(theta3)],
    [0, 0, 1, d3],
    [0, 0, 0, 1]
])
    color ([1.0, 0.0, 0.0]) sphere (r = 8, $fn = resolution);

// verify with openscad transforms and green cube
translate([0, 0, -d2]) rotate([0, 0, -theta2]) translate([-a2, 0, 0]) rotate([-alpha2, 0, 0])
translate([0, 0, -d1]) rotate([0, 0, -theta1]) translate([-a1, 0, 0]) rotate([-alpha1, 0, 0])
rotate([alpha1, 0, 0]) translate([a1, 0, 0]) rotate([0, 0, theta1]) translate([0, 0, d1])
rotate([alpha2, 0, 0]) translate([a2, 0, 0]) rotate([0, 0, theta2]) translate([0, 0, d2])
rotate([alpha3, 0, 0]) translate([a3, 0, 0]) rotate([0, 0, theta3]) translate([0, 0, d3])
rotate([alpha4, 0, 0]) translate([a4, 0, 0]) rotate([0, 0, theta4]) translate([0, 0, d4])
    color ([0.0, 1.0, 0.0]) cube ([12, 12, 12], center=true, $fn=resolution);

module crosshair() {
    color ([0.0, 0.0, 1.0]) cylinder (r=0.5, h=30, center=true, $fn=resolution);
    color ([0.0, 0.0, 1.0]) rotate ([0, 90, 0]) cylinder (r=0.5, h=30, center=true, $fn=resolution);
    color ([0.0, 0.0, 1.0]) rotate ([90, 0, 0]) cylinder (r=0.5, h=30, center=true, $fn=resolution);
}

// }}} inverse matrices test

// ACTUAL IK CALCULATION
x = px;
y = py;
z = pz;

// theta1
theta1_ik1 = atan2(-x, y) + atan2(sqrt(x*x + y*y - pow(d3 + d2, 2)), d3 + d2);
theta1_ik2 = atan2(-x, y) - atan2(sqrt(x*x + y*y - pow(d3 + d2, 2)), d3 + d2);

theta1_ik1r = round(theta1_ik1*10) / 10 - 360;
theta1_ik2r = (round(theta1_ik2*10) / 10 - 360) % 360;
theta1_ik = theta1_ik1r;

// theta3
ik_a = -4*a2*x*cos(theta1_ik) - 4*a2*y*sin(theta1_ik) + x*x*cos(2*theta1_ik) + 2*x*y*sin(2*theta1_ik) - y*y*cos(2*theta1_ik) + 2*pow(z - d1, 2) + 2*a2*a2 + x*x + y*y;
ik_b1 = (ik_a/2 - a3*a3 - a4*a4) / (2*a3*a4);
ik_b = round(ik_b1*1000000) / 1000000; // round to six places
theta3_ik1 = atan2(sqrt(1 - ik_b*ik_b), ik_b);
theta3_ik2 = atan2(-sqrt(1 - ik_b*ik_b), ik_b);

theta3_ik1r = round(theta3_ik1*10) / 10;
theta3_ik2r = round(theta3_ik2*10) / 10;
theta3_ik = theta3_ik1r;

// theta2
ik_c = a2 - (x*cos(theta1_ik) + y*sin(theta1_ik));
ik_d = -z + d1;
ik_e = a4*sin(theta3_ik);
ik_f = ik_c*ik_c + ik_d*ik_d - ik_e*ik_e;
theta2_ik1 = atan2(ik_c, ik_d) + atan2(sqrt(ik_f), ik_e);
theta2_ik2 = atan2(ik_c, ik_d) - atan2(sqrt(ik_f), ik_e);

theta2_ik1r = round(theta2_ik1*10) / 10;
theta2_ik2r = (round(theta2_ik2*10) / 10);
theta2_ik = theta2_ik1r;

// print results
echo("theta1", theta1_ik1r, theta1_ik2r);
echo("theta2", theta2_ik1r, theta2_ik2r);
echo("theta3", theta3_ik1r, theta3_ik2r);
echo();


// RENDER THE MANIPULATOR

include <quad_manipulator.scad>;

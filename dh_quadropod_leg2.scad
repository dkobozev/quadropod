// Rendering of a quadropod leg using Denavit-Hartenberg parameters.
//
// A notable point here is that the length a of link i has to be rendered with
// link i-1.

resolution = 30;

jr = 9;
jh = 15;
ow = 2;

alpha1 = 0;
a1     = 0;
theta1 = 90;
d1     = -30;

alpha2 = -90;
a2     = 27.5;
theta2 = -5;
d2     = 43;

alpha3 = 0;
a3     = 57.3;
theta3 = 26;
d3     = -18;

alpha4 = 90;
a4     = 106;
theta4 = 0;
d4     = 0;

// FORWARD KINEMATICS

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


// INVERSE KINEMATICS
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

theta1_ik1 = atan2(-px, py) + atan2(sqrt(px*px + py*py - pow(d3 + d2, 2)), d3 + d2);
theta1_ik2 = atan2(-px, py) - atan2(sqrt(px*px + py*py - pow(d3 + d2, 2)), d3 + d2);
theta1_ik = theta1_ik1;

ik_a = -4*a2*px*cos(theta1) - 4*a2*py*sin(theta1) + px*px*cos(2*theta1) + 2*px*py*sin(2*theta1) - py*py*cos(2*theta1) + 2*pow(pz - d1, 2) + 2*a2*a2 + px*px + py*py;
ik_b = (ik_a/2 - a3*a3 - a4*a4) / (2*a3*a4);
theta3_ik1 = atan2(sqrt(1 - ik_b*ik_b), ik_b);
theta3_ik2 = atan2(-sqrt(1 - ik_b*ik_b), ik_b);
theta3_ik = theta3_ik1;

ik_c = a2 - (px*cos(theta1_ik) + py*sin(theta1_ik));
ik_d = -pz + d1;
ik_e = a4*sin(theta3_ik);
theta2_ik1 = atan2(ik_c, ik_d) + atan2(sqrt(ik_c*ik_c + ik_d*ik_d - ik_e*ik_e), ik_e);
theta2_ik2 = atan2(ik_c, ik_d) - atan2(sqrt(ik_c*ik_c + ik_d*ik_d - ik_e*ik_e), ik_e);


echo("theta1, solution 1", theta1_ik1 - 360);
echo("theta1, solution 2", theta1_ik2 - 360);

echo("theta2, solution 1", theta2_ik1 - 360);
echo("theta2, solution 2", theta2_ik2 - 360);

echo("theta3, solution 1", theta3_ik1);
echo("theta3, solution 2", theta3_ik2);

echo();

// RENDER MANIPULATOR

dh_cone(alpha1, a1, theta1, d1);

module dh_cone(alpha=0, a=0, theta=0, d=0) {
    rotate([alpha, 0, 0])
    translate([a, 0, 0])
    rotate([0, 0, theta])
    translate([0, 0, d]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d/2]) cube ([ow, ow, abs(d)], center=true); // offset

        rotate ([0, 90, 0]) cylinder (r = 2, h = a2, $fn = resolution); // link

        dh_cone2(alpha2, a2, theta2, d2);
    }
}
module dh_cone2(alpha=0, a=0, theta=0, d=0) {
    rotate([alpha, 0, 0])
    translate([a, 0, 0])
    rotate([0, 0, theta])
    translate([0, 0, d]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d/2]) cube ([ow, ow, abs(d)], center=true); // offset

        rotate ([0, 90, 0]) cylinder (r = 2, h = a3, $fn = resolution); // link

        dh_cone3(alpha3, a3, theta3, d3);
    }
}
module dh_cone3(alpha=0, a=0, theta=0, d=0) {
    rotate([alpha, 0, 0])
    translate([a, 0, 0])
    rotate([0, 0, theta])
    translate([0, 0, d]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d/2]) cube ([ow, ow, abs(d)], center=true); // offset

        rotate ([0, 90, 0]) cylinder (r = 2, h = a4, $fn = resolution); // link

        dh_cone4(alpha4, a4, theta4, d4);
    }
}
module dh_cone4(alpha=0, a=0, theta=0, d=0) {
    rotate([alpha, 0, 0])
    translate([a, 0, 0])
    rotate([0, 0, theta])
    translate([0, 0, d]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d/2]) cube ([ow, ow, abs(d)], center=true); // offset
    }
}

module crosshair() {
    color ([0.0, 0.0, 1.0]) cylinder (r=0.5, h=30, center=true, $fn=resolution);
    color ([0.0, 0.0, 1.0]) rotate ([0, 90, 0]) cylinder (r=0.5, h=30, center=true, $fn=resolution);
    color ([0.0, 0.0, 1.0]) rotate ([90, 0, 0]) cylinder (r=0.5, h=30, center=true, $fn=resolution);
}

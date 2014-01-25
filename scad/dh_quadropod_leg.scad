resolution = 30;

jr = 9;
jh = 15;
ow = 2;

alpha1 = 0;
a1     = 0;
theta1 = 0;
d1     = -30;

alpha2 = -90;
a2     = 27.5;
theta2 = -15;
d2     = 43;

alpha3 = 0;
a3     = 57.3;
theta3 = 30;
d3     = -18;

alpha4 = 90;
a4     = 106;
theta4 = 0;
d4     = 0;


dh_cone(alpha1, a1, theta1, d1);

module dh_cone(alpha=0, a=0, theta=0, d=0) {
    rotate([alpha, 0, 0])
    translate([a, 0, 0])
    rotate([0, 0, theta])
    translate([0, 0, d]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        rotate ([0, -90, 0]) cylinder (r = 2, h = a, $fn = resolution); // link
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d/2]) cube ([ow, ow, abs(d)], center=true); // offset

        dh_cone2(alpha2, a2, theta2, d2);
    }
}
module dh_cone2(alpha=0, a=0, theta=0, d=0) {
    rotate([alpha, 0, 0])
    translate([a, 0, 0])
    rotate([0, 0, theta])
    translate([0, 0, d]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        rotate ([0, -90, 0]) cylinder (r = 2, h = a, $fn = resolution); // link
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d/2]) cube ([ow, ow, abs(d)], center=true); // offset

        dh_cone3(alpha3, a3, theta3, d3);
    }
}
module dh_cone3(alpha=0, a=0, theta=0, d=0) {
    rotate([alpha, 0, 0])
    translate([a, 0, 0])
    rotate([0, 0, theta])
    translate([0, 0, d]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        rotate ([0, -90, 0]) cylinder (r = 2, h = a, $fn = resolution); // link
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d/2]) cube ([ow, ow, abs(d)], center=true); // offset

        dh_cone4(alpha4, a4, theta4, d4);
    }
}
module dh_cone4(alpha=0, a=0, theta=0, d=0) {
    rotate([alpha, 0, 0])
    translate([a, 0, 0])
    rotate([0, 0, theta])
    translate([0, 0, d]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        rotate ([0, -90, 0]) cylinder (r = 2, h = a, $fn = resolution); // link
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d/2]) cube ([ow, ow, abs(d)], center=true); // offset
    }
}


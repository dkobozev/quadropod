dh_cone1();

module dh_cone1() {
    rotate([alpha1, 0, 0])
    translate([a1, 0, 0])
    rotate([0, 0, theta1])
    translate([0, 0, d1]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d1/2]) cube ([ow, ow, abs(d1)], center=true); // offset
        rotate ([0, 90, 0]) cylinder (r=2, h=a2, $fn = resolution); // link

        dh_cone2();
    }
}
module dh_cone2() {
    rotate([alpha2, 0, 0])
    translate([a2, 0, 0])
    rotate([0, 0, theta2])
    translate([0, 0, d2]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d2/2]) cube ([ow, ow, abs(d2)], center=true); // offset
        rotate ([0, 90, 0]) cylinder (r=2, h=a3, $fn = resolution); // link

        dh_cone3();
    }
}
module dh_cone3() {
    rotate([alpha3, 0, 0])
    translate([a3, 0, 0])
    rotate([0, 0, theta3])
    translate([0, 0, d3]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d3/2]) cube ([ow, ow, abs(d3)], center=true); // offset
        rotate ([0, 90, 0]) cylinder (r=2, h=a4, $fn = resolution); // link

        dh_cone4();
    }
}
module dh_cone4() {
    rotate([alpha4, 0, 0])
    translate([a4, 0, 0])
    rotate([0, 0, theta4])
    translate([0, 0, d4]) {
        color([231/255, 88/255, 88/255]) cylinder(r1=jr, r2=0, h=jh, center=true, $fn=resolution); // joint
        color ([70/255, 70/255, 70/255]) translate([0, 0, -d4/2]) cube ([ow, ow, abs(d4)], center=true); // offset
    }
}

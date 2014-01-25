#include <Arduino.h>
#include "leg.h"

#include <math.h>

#define DEG_PER_RAD (180.0 / M_PI)
#define DEG2RAD(x) (x) / DEG_PER_RAD
#define RAD2DEG(x) (x) * DEG_PER_RAD

#define ALPHA1   0
#define A1       0
#define D1     -30

#define ALPHA2 -90
#define A2      27.5
#define D2      43

#define ALPHA3   0
#define A3      57.3
#define D3     -18

#define ALPHA4  90
#define A4     106
#define D4       0

#define IK_TOLERANCE 4


void print_solutions(float *solutions, int n)
{
    for (int i = 0; i < n; i++) {
        Serial.print("(");
        Serial.print(solutions[3*i]);
        Serial.print(", ");
        Serial.print(solutions[3*i+1]);
        Serial.print(", ");
        Serial.print(solutions[3*i+2]);
        Serial.println(")");
    }
}

void print_xyz(float x, float y, float z)
{
    Serial.print("(");
    Serial.print(x);
    Serial.print(", ");
    Serial.print(y);
    Serial.print(", ");
    Serial.print(z);
    Serial.println(")");
}

int fk(float a1, float a2, float a3, float a4,
       float theta1, float theta2, float theta3,
       float d1, float d2, float d3,
       float *x, float *y, float *z)
{
    double c1, c2, c23, s1, s2, s23;

    theta1 = DEG2RAD(theta1);
    theta2 = DEG2RAD(theta2);
    theta3 = DEG2RAD(theta3);

    c1 = cos(theta1);
    c2 = cos(theta2);
    c23 = cos(theta2 + theta3);

    s1 = sin(theta1);
    s2 = sin(theta2);
    s23 = sin(theta2 + theta3);

    *x = a4*c1*c23 + a3*c1*c2 - d3*s1 + a2*c1 - d2*s1;
    *y = a4*s1*c23 + a3*s1*c2 + d3*c1 + a2*s1 + d2*c1;
    *z = -a4*s23 - a3*s2 + d1;

    return 1;
}

float convert_angle(float a)
{
    a = RAD2DEG(a);
    if (a >= 180.0) {
        a = fmod(a, 180.0) - 180.0;
    } else if (a < -180.0) {
        a = 180.0 - fmod(fabs(a), 180.0);
    }

    if (a == -180.0) {
        a = 180.0;
    }

    return a;
}

int ik_theta1(float x, float y, float d2, float d3, float *solution1, float *solution2)
{
    double d, m, xyd, n;

    d = d2 + d3;
    m = atan2(-x, y);
    xyd = fabs(x*x + y*y - d*d);

    if (xyd >= 0) {
        n = atan2(sqrt(xyd), d);
    } else {
        // no solutions
        //Serial.println("no solutions for theta1");
        return 0;
    }

    *solution1 = convert_angle(m + n);
    *solution2 = convert_angle(m - n);

    if (*solution1 > 0) {
        *solution1 = -*solution1;
    }
    if (*solution2 > 0) {
        *solution2 = -*solution2;
    }

    return 1;
}

int ik_theta3(float x, float y, float z,
              float theta1, float a2, float a3, float a4, float d1,
              float *solution1, float *solution2)
{
    double th1, m, n, n2, o;

    th1 = DEG2RAD(theta1);
    m = (-4*a2*x*cos(th1) - 4*a2*y*sin(th1) + x*x*cos(2*th1) + 2*x*y*sin(2*th1) -
         y*y*cos(2*th1) + 2*(z - d1)*(z - d1) + 2*a2*a2 + x*x + y*y);
    n = (m/2 - a3*a3 - a4*a4) / (2*a3*a4);
    n2 = n*n;

    if (n2 > 1) {
        if (fabs(n2 - 1) > 0.01) {
            // no solutions
            //Serial.println("no solutions for theta3");
            return 0;
        } else {
            n2 = 1;
        }
    }

    o = sqrt(1 - n2);
    *solution1 = convert_angle(atan2(o, n));
    *solution2 = convert_angle(atan2(-o, n));

    return 1;
}

int ik_theta2(float x, float y, float z,
              float theta1, float theta3, float a2, float a4, float d1,
              float *solution1, float *solution2)
{
    double m, n, o, p, q, r;

    theta1 = DEG2RAD(theta1);
    theta3 = DEG2RAD(theta3);
    m = a2 - (x*cos(theta1) + y*sin(theta1));
    n = -z + d1;
    o = a4*sin(theta3);
    p = m*m + n*n - o*o;

    if (p < 0) {
        // no solutions
        //Serial.println("no solutions for theta2");
        return 0;
    }

    q = atan2(m, n);
    r = atan2(sqrt(p), o);

    *solution1 = convert_angle(q + r);
    *solution2 = convert_angle(q - r);

    return 1;
}

int ik(float x, float y, float z,
       float a1, float a2, float a3, float a4, float d1, float d2, float d3,
       float *solutions)
{
    float th1[2], th2[2], th3[2];
    int i, j, k;
    int n = 0;

    // find solutions for theta1
    if (ik_theta1(x, y, d2, d3, &th1[0], &th1[1])) {
        for (i = 0; i < 2; i++) {
            // find solutions for theta3
            if (ik_theta3(x, y, z, th1[i], a2, a3, a4, d1, &th3[0], &th3[1])) {
                for (j = 0; j < 2; j++) {
                    // find solutions for theta2
                    if (ik_theta2(x, y, z, th1[i], th3[j], a2, a4, d1, &th2[0], &th2[1])) {
                        for (k = 0; k < 2; k++) {
                            if (th2[k] < -90) {
                                continue;
                            }
                            solutions[3*n] = th1[i];
                            solutions[3*n+1] = th2[k];
                            solutions[3*n+2] = th3[j];
                            n++;
                        }
                    }
                }
            }
        }
    }

    return n;
}

int iksearch_fk(float x, float y, float z,
                float a1, float a2, float a3, float a4, float d1, float d2, float d3,
                float *iksolutions)
{
    float solutions[24];
    int i;
    int n;
    float px, py, pz;
    int valid[8];
    int n_valid = 0;

    //Serial.println("target:");
    //print_xyz(x, y, z);

    n = ik(x, y, z, A1, A2, A3, A4, D1, D2, D3, solutions);

    //Serial.println("Possible solutions:");
    //print_solutions(solutions, n);

    // test for valid solutions
    for (i = 0; i < n; i++) {
        fk(A1, A2, A3, A4, solutions[3*i], solutions[3*i+1], solutions[3*i+2],
           D1, D2, D3, &px, &py, &pz);

        //Serial.println("FK:");
        //print_xyz(px, py, pz);

        if (    fabs(px - x) < IK_TOLERANCE &&
                fabs(py - y) < IK_TOLERANCE &&
                fabs(pz - z) < IK_TOLERANCE) {
            valid[n_valid] = i;
            n_valid++;
        }
    }

    for (i = 0; i < n_valid; i++) {
        iksolutions[3*i] = solutions[3*valid[i]];
        iksolutions[3*i+1] = solutions[3*valid[i]+1];
        iksolutions[3*i+2] = solutions[3*valid[i]+2];
    }

    //Serial.println("Valid solutions:");
    //print_solutions(iksolutions, n_valid);

    // return the number of valid solutions
    return n_valid;
}

joint_t joints[NUM_JOINTS];

int joint_pins[] = {
    11, 12, 13, // hind right: hip, knee, ankle
    8,  9,  10, // fore right
     7,  6,  5, // fore left
     4,  3,  2, // hind left
};

// direction, adjustment angle, min pulse adjustment, max pulse adjustment
int joint_settings[] = {
    // HIND RIGHT
    -1, -7, 0, 0,
     1, 86, 0, 0,
    -1, 160, 0, 0,

    // FORE RIGHT
     1, 182, 0, 0,
    -1, 88, 0, 0,
     1, 20, 0, 0,

    // FORE LEFT
    -1, 2, 0, 0,
     1, 98, 0, 0,
    -1, 155, 0, 0,

    // HIND LEFT
     1, 184, 0, 0,
    -1, 92, 0, 0,
     1, 20, 0, 0,
};

void leg_set_position(int leg, float x, float y, float z)
{
    int n;
    float solutions[24];

    if (n = iksearch_fk(x, y, z, A1, A2, A3, A4, D1, D2, D3, solutions)) {
        joint_rotate(&joints[3*leg], solutions[0]);
        joint_rotate(&joints[3*leg+1], solutions[1]);
        joint_rotate(&joints[3*leg+2], solutions[2]);
    }
    else {
        Serial.print("No solution for leg: ");
        Serial.println(leg);
        print_xyz(x, y, z);
    }
}


int joint_start_angles[] = {
    -72.61,  -16.09, 103.44,
    -72.61,  -16.09, 103.44,
    -72.61,  -16.09, 103.44,
    -72.61,  -16.09, 103.44,
};

int t = 0;

float hrx = 50;
float hry = -76;
float hrz = -120;

float frx = 50;
float fry = -76;
float frz = -120;

float flx = 50;
float fly = -76;
float flz = -120;

float hlx = 50;
float hly = -76;
float hlz = -120;

void setup()
{
    int dir, start, min, max;
    float dt, dz;
    int cycle;

    // workaround for delay() bug
    Serial.begin(9600);

    for (int i = 0; i < NUM_JOINTS; i++) {
        dir   = joint_settings[i*4];
        start = joint_settings[i*4+1];
        min   = joint_settings[i*4+2];
        max   = joint_settings[i*4+3];

        joint_init(&joints[i], joint_pins[i], start, dir, min, max);
        joint_rotate(&joints[i], joint_start_angles[i]);
    }

    delay(2000);

    Serial.println("Leg positions:");
    print_xyz(hrx, hry, hrz);
    print_xyz(frx, fry, frz);
    print_xyz(flx, fly, flz);
    print_xyz(hlx, hly, hlz);
    Serial.println("Setup finished");

    for (cycle = 0; cycle < 6; cycle++) {
        // shift body left
        for (t = 0; t <= 90; t++) {
            dt = t/3.0;
            leg_set_position(0, hrx + dt, hry - dt, hrz);
            leg_set_position(1, frx - dt, fry - dt, frz);
            leg_set_position(2, flx - dt, fly + dt, flz);
            leg_set_position(3, hlx + dt, hly + dt, hlz);
        }
        hrx += 30;
        hry -= 30;
        frx -= 30;
        fry -= 30;
        flx -= 30;
        fly += 30;
        hlx += 30;
        hly += 30;

        // raise hr
        for (t = 0; t <= 90; t++) {
            dt = t/2.0;
            dz = sin(M_PI/2 * t/90) * 30;
            leg_set_position(0, hrx - dt, hry, hrz + dz);
        }
        hrx -= 45;
        hrz += 30;

        // lower hr
        for (t = 0; t <= 90; t++) {
            dt = t/2.0;
            dz = (sin(M_PI/2 + M_PI/2 * t/90) - 1) * 30;
            leg_set_position(0, hrx - dt, hry, hrz + dz);
            //leg_set_position(2, flx + dt, fly, flz + dz);
            //leg_set_position(3, hlx - dt, hly, hlz + dz);
        }
        hrx -= 45;
        hrz -= 30;

        // raise fr
        for (t = 0; t <= 90; t++) {
            dt = t/2.0;
            dz = sin(M_PI/2 * t/90) * 30;
            leg_set_position(1, frx + dt, hry, frz + dz);
        }
        frx += 45;
        frz += 30;

        // lower fr
        for (t = 0; t <= 90; t++) {
            dt = t/2.0;
            dz = (sin(M_PI/2 + M_PI/2 * t/90) - 1) * 30;
            leg_set_position(1, frx + dt, hry, frz + dz);
        }
        frx += 45;
        frz -= 30;

        // shift body right
        for (t = 0; t <= 90; t++) {
            dt = t/3.0;
            leg_set_position(0, hrx + dt, hry + dt*2, hrz);
            leg_set_position(1, frx - dt, fry + dt*2, frz);
            leg_set_position(2, flx - dt, fly - dt*2, flz);
            leg_set_position(3, hlx + dt, hly - dt*2, hlz);
        }
        hrx += 30;
        hry += 60;
        frx -= 30;
        fry += 60;
        flx -= 30;
        fly -= 60;
        hlx += 30;
        hly -= 60;

        // raise hl
        for (t = 0; t <= 90; t++) {
            dt = t/2.0;
            dz = sin(M_PI/2 * t/90) * 30;
            leg_set_position(3, hlx - dt, hly, hlz + dz);
        }
        hlx -= 45;
        hlz += 30;

        // lower hl
        for (t = 0; t <= 90; t++) {
            dt = t/2.0;
            dz = (sin(M_PI/2 + M_PI/2 * t/90) - 1) * 30;
            leg_set_position(3, hlx - dt, hly, hlz + dz);
        }
        hlx -= 45;
        hlz -= 30;

        // raise fl
        for (t = 0; t <= 90; t++) {
            dt = t/2.0;
            dz = sin(M_PI/2 * t/90) * 30;
            leg_set_position(2, flx + dt, fly, flz + dz);
        }
        flx += 45;
        flz += 30;

        // lower fl
        for (t = 0; t <= 90; t++) {
            dt = t/2.0;
            dz = (sin(M_PI/2 + M_PI/2 * t/90) - 1) * 30;
            leg_set_position(2, flx + dt, fly, flz + dz);
        }
        flx += 45;
        flz -= 30;

        // center body
        for (t = 0; t <= 90; t++) {
            dt = t/3.0;
            leg_set_position(0, hrx + dt, hry - dt, hrz);
            leg_set_position(1, frx - dt, fry - dt, frz);
            leg_set_position(2, flx - dt, fly + dt, flz);
            leg_set_position(3, hlx + dt, hly + dt, hlz);
        }
        hrx += 30;
        hry -= 30;
        frx -= 30;
        fry -= 30;
        flx -= 30;
        fly += 30;
        hlx += 30;
        hly += 30;

        Serial.print("End of cycle "); Serial.println(cycle);
    }

    Serial.println("Leg positions:");
    print_xyz(hrx, hry, hrz);
    print_xyz(frx, fry, frz);
    print_xyz(flx, fly, flz);
    print_xyz(hlx, hly, hlz);

    Serial.println("Done");
}

void loop()
{
    //int n;
    //float solutions[24];

    //if (i > 30) {
    //    i = 0;
    //}
    //i = 23;

    //Serial.println(i);

    //if (n = iksearch_fk(hrx + i, hry - i, hrz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
    //    //Serial.print("Found solution for hr:");
    //    //print_solutions(solutions, 1);

    //    joint_rotate(&joints[0], solutions[0]);
    //    joint_rotate(&joints[1], solutions[1]);
    //    joint_rotate(&joints[2], solutions[2]);
    //}
    //else {
    //    Serial.println("No solution for hr");
    //}

    //if (n = iksearch_fk(frx - i, fry - i, frz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
    //    joint_rotate(&joints[3], solutions[0]);
    //    joint_rotate(&joints[4], solutions[1]);
    //    joint_rotate(&joints[5], solutions[2]);
    //}
    //else {
    //    Serial.println("No solution for fr:");
    //}

    //if (n = iksearch_fk(flx - i, fly + i, flz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
    //    joint_rotate(&joints[6], solutions[0]);
    //    joint_rotate(&joints[7], solutions[1]);
    //    joint_rotate(&joints[8], solutions[2]);
    //}
    //else {
    //    Serial.println("No solution for fl:");
    //}

    //if (n = iksearch_fk(hlx + i, hly + i, hlz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
    //    joint_rotate(&joints[9], solutions[0]);
    //    joint_rotate(&joints[10], solutions[1]);
    //    joint_rotate(&joints[11], solutions[2]);
    //}
    //else {
    //    Serial.println("No solution for hl:");
    //}

    //i++;
    //delay(100);
}

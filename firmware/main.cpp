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

#define LEG_HR 0
#define LEG_FR 3
#define LEG_FL 6
#define LEG_HL 9


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
                            break; // stop after 1 solution
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

float joint_start_angles[] = {
    -72.61,  -16.09, 103.44,
    -72.61,  -16.09, 103.44,
    -72.61,  -16.09, 103.44,
    -72.61,  -16.09, 103.44,
};

// last leg coordinates for all legs
float lcs[] = {
    70, -80, -130,
    70, -80, -130,
    70, -80, -130,
    70, -80, -130,
};
#define LEN_LEG_COORDS 12

// current leg coordinates
float nlcs[LEN_LEG_COORDS];


void update_leg_coords()
{
    int i;

    for (i = 0; i < LEN_LEG_COORDS; i++) {
        lcs[i] = nlcs[i];
    }
}

void leg_set_position(int leg, float x, float y, float z)
{
    float solutions[24];

    if (iksearch_fk(x, y, z, A1, A2, A3, A4, D1, D2, D3, solutions)) {
        joint_rotate(&joints[leg], solutions[0]);
        joint_rotate(&joints[leg+1], solutions[1]);
        joint_rotate(&joints[leg+2], solutions[2]);

        nlcs[leg]   = x;
        nlcs[leg+1] = y;
        nlcs[leg+2] = z;
    }
    else {
        Serial.print("No solution for leg: ");
        Serial.println(leg);
        print_xyz(x, y, z);
    }
}

// turn left or right depending on the order of legs:
// fl, hl, hr, fr to turn left
// fr, hr, hl, fl to turn right
void turn(int leg_front1, int leg_hind1, int leg_hind2, int leg_front2)
{
    float angle, raise_h, steps, dt, rdz, solutions[24], theta1;
    int t, step_delay;

    raise_h = 42;
    angle = 30;
    steps = 10;
    step_delay = 30;

    if (iksearch_fk(lcs[LEG_HR], lcs[LEG_HR+1], lcs[LEG_HR+2], A1, A2, A3, A4, D1, D2, D3, solutions)) {
        theta1 = solutions[0];

        // turn body
        for (t = 0; t <= (int) steps; t++) {
            dt = angle * t/steps;

            joint_rotate(&joints[leg_front1], theta1+dt);
            joint_rotate(&joints[leg_hind1], theta1-dt*1.5);
            joint_rotate(&joints[leg_hind2], theta1+dt);
            joint_rotate(&joints[leg_front2], theta1-dt*0.5);

            delay(step_delay);
        }

        // readjust front leg 1
        for (t = 0; t <= (int) steps; t++) {
            dt = angle * t/steps;
            rdz = raise_h * sin(M_PI * t/steps);

            if (iksearch_fk(lcs[LEG_HR], lcs[LEG_HR+1], lcs[LEG_HR+2]+rdz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
                joint_rotate(&joints[leg_front1],   solutions[0]+angle-dt);
                joint_rotate(&joints[leg_front1+1], solutions[1]);
                joint_rotate(&joints[leg_front1+2], solutions[2]);
            }

            delay(step_delay);
        }

        // readjust hind leg 1
        for (t = 0; t <= (int) steps; t++) {
            dt = angle * t/steps;
            rdz = raise_h * sin(M_PI * t/steps);

            if (iksearch_fk(lcs[LEG_HR], lcs[LEG_HR+1], lcs[LEG_HR+2]+rdz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
                joint_rotate(&joints[leg_hind1],   solutions[0]-angle*1.5+dt*2.0);
                joint_rotate(&joints[leg_hind1+1], solutions[1]);
                joint_rotate(&joints[leg_hind1+2], solutions[2]);
            }

            delay(step_delay);
        }

        // readjust hind leg 2
        for (t = 0; t <= (int) steps; t++) {
            dt = angle * t/steps;
            rdz = raise_h * sin(M_PI * t/steps);

            if (iksearch_fk(lcs[LEG_HR], lcs[LEG_HR+1], lcs[LEG_HR+2]+rdz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
                joint_rotate(&joints[leg_hind2],   solutions[0]+angle-dt*2);
                joint_rotate(&joints[leg_hind2+1], solutions[1]);
                joint_rotate(&joints[leg_hind2+2], solutions[2]);
            }

            delay(step_delay);
        }

        // readjust front leg 2
        for (t = 0; t <= (int) steps; t++) {
            dt = angle * t/steps;
            rdz = raise_h * sin(M_PI * t/steps);

            if (iksearch_fk(lcs[LEG_HR], lcs[LEG_HR+1], lcs[LEG_HR+2]+rdz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
                joint_rotate(&joints[leg_front2],   solutions[0]-angle*0.5+dt);
                joint_rotate(&joints[leg_front2+1], solutions[1]);
                joint_rotate(&joints[leg_front2+2], solutions[2]);
            }

            delay(step_delay);
        }

        // turn body in the opposite direction to even out
        for (t = 0; t <= (int) steps; t++) {
            dt = angle * t/steps;

            joint_rotate(&joints[leg_hind1], theta1+angle-dt);
            joint_rotate(&joints[leg_hind2], theta1-angle*0.5+dt*0.5);
            joint_rotate(&joints[leg_front2], theta1+angle*0.5-dt*0.5);

            delay(step_delay);
        }
    }
} // turn

void turn_left()
{
    turn(LEG_FL, LEG_HL, LEG_HR, LEG_FR);
}

void turn_right()
{
    turn(LEG_FR, LEG_HR, LEG_HL, LEG_FL);
}

// strafe left or right depending on the order of legs:
// fr, hr, hl, fl to strafe left
// fl, hl, hr, fr to strafe right
void strafe(int leg_front1, int leg_hind1, int leg_hind2, int leg_front2, int direction)
{
    float strafe_d, raise_h, sdy, dy, rdz, steps;
    int t, step_delay;

    strafe_d = 50;
    raise_h = 38;
    steps = 10;
    step_delay = 30;

    // shift body in the direction we want to strafe
    for (t = 0; t <= (int) steps; t++) {
        sdy = direction * strafe_d * t/steps;

        leg_set_position(LEG_HR, lcs[LEG_HR], lcs[LEG_HR+1]+sdy, lcs[LEG_HR+2]);
        leg_set_position(LEG_FR, lcs[LEG_FR], lcs[LEG_FR+1]+sdy, lcs[LEG_FR+2]);
        leg_set_position(LEG_FL, lcs[LEG_FL], lcs[LEG_FL+1]-sdy, lcs[LEG_FL+2]);
        leg_set_position(LEG_HL, lcs[LEG_HL], lcs[LEG_HL+1]-sdy, lcs[LEG_HL+2]);

        delay(step_delay);
    }

    update_leg_coords();

    // readjust hind leg 1
    for (t = 0; t <= (int) steps; t++) {
        dy = strafe_d * t/steps;
        rdz = raise_h * sin(M_PI * t/steps);

        leg_set_position(leg_hind1, lcs[leg_hind1], lcs[leg_hind1+1]+dy, lcs[leg_hind1+2]+rdz);

        delay(step_delay);
    }

    update_leg_coords();

    // readjust front leg 1
    for (t = 0; t <= (int) steps; t++) {
        dy = strafe_d * t/steps;
        rdz = raise_h * sin(M_PI * t/steps);

        leg_set_position(leg_front1, lcs[leg_front1], lcs[leg_front1+1]+dy, lcs[leg_front1+2]+rdz);

        delay(step_delay);
    }

    update_leg_coords();

    // shift body in the opposite direction for stability
    for (t = 0; t <= (int) steps; t++) {
        sdy = direction * strafe_d * t/steps;

        leg_set_position(LEG_HR, lcs[LEG_HR], lcs[LEG_HR+1]-sdy*0.75, lcs[LEG_HR+2]);
        leg_set_position(LEG_FR, lcs[LEG_FR], lcs[LEG_FR+1]-sdy*0.75, lcs[LEG_FR+2]);
        leg_set_position(LEG_FL, lcs[LEG_FL], lcs[LEG_FL+1]+sdy*0.75, lcs[LEG_FL+2]);
        leg_set_position(LEG_HL, lcs[LEG_HL], lcs[LEG_HL+1]+sdy*0.75, lcs[LEG_HL+2]);

        delay(step_delay);
    }

    update_leg_coords();

    // readjust hind leg 2
    for (t = 0; t <= (int) steps; t++) {
        dy = strafe_d * t/steps;
        rdz = raise_h * sin(M_PI * t/steps);

        leg_set_position(leg_hind2, lcs[leg_hind2], lcs[leg_hind2+1]-dy, lcs[leg_hind2+2]+rdz);

        delay(step_delay);
    }

    update_leg_coords();

    // readjust front leg 2
    for (t = 0; t <= (int) steps; t++) {
        dy = strafe_d * t/steps;
        rdz = raise_h * sin(M_PI * t/steps);

        leg_set_position(leg_front2, lcs[leg_front2], lcs[leg_front2+1]-dy, lcs[leg_front2+2]+rdz);

        delay(step_delay);
    }

    update_leg_coords();

    // shift body in the strafe direction again
    for (t = 0; t <= (int) steps; t++) {
        sdy = direction * strafe_d * t/steps;

        leg_set_position(LEG_HR, lcs[LEG_HR], lcs[LEG_HR+1]+sdy*0.75, lcs[LEG_HR+2]);
        leg_set_position(LEG_FR, lcs[LEG_FR], lcs[LEG_FR+1]+sdy*0.75, lcs[LEG_FR+2]);
        leg_set_position(LEG_FL, lcs[LEG_FL], lcs[LEG_FL+1]-sdy*0.75, lcs[LEG_FL+2]);
        leg_set_position(LEG_HL, lcs[LEG_HL], lcs[LEG_HL+1]-sdy*0.75, lcs[LEG_HL+2]);

        delay(step_delay);
    }

    update_leg_coords();
} // strafe

void strafe_left()
{
    strafe(LEG_FR, LEG_HR, LEG_HL, LEG_FL, -1);
}

void strafe_right()
{
    strafe(LEG_FL, LEG_HL, LEG_HR, LEG_FR, 1);
}

void walk(int leg_front1, int leg_hind1, int leg_hind2, int leg_front2)
{
    float sdx, sdy, rdt, rdz, steps, shift_dx, shift_dy, raise_h, raise_d;
    int t;

    shift_dx = 13.75;
    shift_dy = 15;

    raise_d = 55;
    raise_h = 34;

    steps = 10.0;

    // shift body left, raise hind leg 1
    for (t = 0; t <= (int) steps; t++) {
        sdx = shift_dx * t/steps;
        sdy = shift_dy * t/steps;
        rdt = raise_d * t/steps;
        rdz = raise_h * sin(M_PI/2 * t/steps);

        leg_set_position(leg_hind1,  lcs[leg_hind1]+sdx-rdt, lcs[leg_hind1+1]-sdy,  lcs[leg_hind1+2]+rdz);
        leg_set_position(leg_front1, lcs[leg_front1]-sdx,    lcs[leg_front1+1]-sdy, lcs[leg_front1+2]);
        leg_set_position(leg_front2, lcs[leg_front2]-sdx,    lcs[leg_front2+1]+sdy, lcs[leg_front2+2]);
        leg_set_position(leg_hind2,  lcs[leg_hind2]+sdx,     lcs[leg_hind2+1]+sdy,  lcs[leg_hind2+2]);
    }

    update_leg_coords();

    // shift body left, lower hind leg 1
    for (t = 0; t <= (int) steps; t++) {
        sdx = shift_dx * t/steps;
        sdy = shift_dy * t/steps;
        rdt = raise_d * t/steps;
        rdz = raise_h * (sin(M_PI/2 + M_PI/2 * t/steps) - 1);

        leg_set_position(leg_hind1,  lcs[leg_hind1]+sdx-rdt, lcs[leg_hind1+1]-sdy,  lcs[leg_hind1+2]+rdz);
        leg_set_position(leg_front1, lcs[leg_front1]-sdx,    lcs[leg_front1+1]-sdy, lcs[leg_front1+2]);
        leg_set_position(leg_front2, lcs[leg_front2]-sdx,    lcs[leg_front2+1]+sdy, lcs[leg_front2+2]);
        leg_set_position(leg_hind2,  lcs[leg_hind2]+sdx,     lcs[leg_hind2+1]+sdy,  lcs[leg_hind2+2]);
    }

    update_leg_coords();

    // shift body right, raise fr
    for (t = 0; t <= (int) steps; t++) {
        sdx = shift_dx * t/steps;
        sdy = shift_dy * t/steps;
        rdt = raise_d * t/steps;
        rdz = raise_h * sin(M_PI/2 * t/steps);

        leg_set_position(leg_hind1,  lcs[leg_hind1]+sdx,      lcs[leg_hind1+1]+sdy,  lcs[leg_hind1+2]);
        leg_set_position(leg_front1, lcs[leg_front1]-sdx+rdt, lcs[leg_front1+1]+sdy, lcs[leg_front1+2]+rdz);
        leg_set_position(leg_front2, lcs[leg_front2]-sdx,     lcs[leg_front2+1]-sdy, lcs[leg_front2+2]);
        leg_set_position(leg_hind2,  lcs[leg_hind2]+sdx,      lcs[leg_hind2+1]-sdy,  lcs[leg_hind2+2]);
    }

    update_leg_coords();

    // shift body right, lower fr
    for (t = 0; t <= (int) steps; t++) {
        sdx = shift_dx * t/steps;
        sdy = shift_dy * t/steps;
        rdt = raise_d * t/steps;
        rdz = raise_h * (sin(M_PI/2 + M_PI/2 * t/steps) - 1);

        leg_set_position(leg_hind1,  lcs[leg_hind1]+sdx,      lcs[leg_hind1+1]+sdy,  lcs[leg_hind1+2]);
        leg_set_position(leg_front1, lcs[leg_front1]-sdx+rdt, lcs[leg_front1+1]+sdy, lcs[leg_front1+2]+rdz);
        leg_set_position(leg_front2, lcs[leg_front2]-sdx,     lcs[leg_front2+1]-sdy, lcs[leg_front2+2]);
        leg_set_position(leg_hind2,  lcs[leg_hind2]+sdx,      lcs[leg_hind2+1]-sdy,  lcs[leg_hind2+2]);
    }

    update_leg_coords();

    // shift body right, raise hl
    for (t = 0; t <= (int) steps; t++) {
        sdx = shift_dx * t/steps;
        sdy = shift_dy * t/steps;
        rdt = raise_d * t/steps;
        rdz = raise_h * sin(M_PI/2 * t/steps);

        leg_set_position(leg_hind1,  lcs[leg_hind1]+sdx,      lcs[leg_hind1+1]+sdy,  lcs[leg_hind1+2]);
        leg_set_position(leg_front1, lcs[leg_front1]-sdx,     lcs[leg_front1+1]+sdy, lcs[leg_front1+2]);
        leg_set_position(leg_front2, lcs[leg_front2]-sdx,     lcs[leg_front2+1]-sdy, lcs[leg_front2+2]);
        leg_set_position(leg_hind2,  lcs[leg_hind2]+sdx-rdt,  lcs[leg_hind2+1]-sdy,  lcs[leg_hind2+2]+rdz);
    }

    update_leg_coords();

    // shift body right, lower hl
    for (t = 0; t <= (int) steps; t++) {
        sdx = shift_dx * t/steps;
        sdy = shift_dy * t/steps;
        rdt = raise_d * t/steps;
        rdz = raise_h * (sin(M_PI/2 + M_PI/2 * t/steps) - 1);

        leg_set_position(leg_hind1,  lcs[leg_hind1]+sdx,     lcs[leg_hind1+1]+sdy,  lcs[leg_hind1+2]);
        leg_set_position(leg_front1, lcs[leg_front1]-sdx,    lcs[leg_front1+1]+sdy, lcs[leg_front1+2]);
        leg_set_position(leg_front2, lcs[leg_front2]-sdx,    lcs[leg_front2+1]-sdy, lcs[leg_front2+2]);
        leg_set_position(leg_hind2,  lcs[leg_hind2]+sdx-rdt, lcs[leg_hind2+1]-sdy,  lcs[leg_hind2+2]+rdz);
    }

    update_leg_coords();

    // shift body left, raise fl
    for (t = 0; t <= (int) steps; t++) {
        sdx = shift_dx * t/steps;
        sdy = shift_dy * t/steps;
        rdt = raise_d * t/steps;
        rdz = raise_h * sin(M_PI/2 * t/steps);

        leg_set_position(leg_hind1,  lcs[leg_hind1]+sdx,      lcs[leg_hind1+1]-sdy,  lcs[leg_hind1+2]);
        leg_set_position(leg_front1, lcs[leg_front1]-sdx,     lcs[leg_front1+1]-sdy, lcs[leg_front1+2]);
        leg_set_position(leg_front2, lcs[leg_front2]-sdx+rdt, lcs[leg_front2+1]+sdy, lcs[leg_front2+2]+rdz);
        leg_set_position(leg_hind2,  lcs[leg_hind2]+sdx,      lcs[leg_hind2+1]+sdy,  lcs[leg_hind2+2]);
    }

    update_leg_coords();

    // shift body left, lower fl
    for (t = 0; t <= (int) steps; t++) {
        sdx = shift_dx * t/steps;
        sdy = shift_dy * t/steps;
        rdt = raise_d * t/steps;
        rdz = raise_h * (sin(M_PI/2 + M_PI/2 * t/steps) - 1);

        leg_set_position(leg_hind1,  lcs[leg_hind1]+sdx,      lcs[leg_hind1+1]-sdy,  lcs[leg_hind1+2]);
        leg_set_position(leg_front1, lcs[leg_front1]-sdx,     lcs[leg_front1+1]-sdy, lcs[leg_front1+2]);
        leg_set_position(leg_front2, lcs[leg_front2]-sdx+rdt, lcs[leg_front2+1]+sdy, lcs[leg_front2+2]+rdz);
        leg_set_position(leg_hind2,  lcs[leg_hind2]+sdx,      lcs[leg_hind2+1]+sdy,  lcs[leg_hind2+2]);
    }

    update_leg_coords();
} // walk

void walk_forward()
{
    walk(LEG_FR, LEG_HR, LEG_HL, LEG_FL);
}

void setup()
{
    int i, dir, start, min, max;

    Serial.begin(9600); // workaround for delay() bug

    for (i = 0; i < NUM_JOINTS; i++) {
        dir   = joint_settings[i*4];
        start = joint_settings[i*4+1];
        min   = joint_settings[i*4+2];
        max   = joint_settings[i*4+3];

        joint_init(&joints[i], joint_pins[i], start, dir, min, max);
        joint_rotate(&joints[i], joint_start_angles[i]);
    }

    delay(2000);

    Serial.println("Starting walking...");

    walk_forward();
    walk_forward();

    strafe_left();
    strafe_right();

    walk_forward();

    turn_left();
    turn_right();

    walk_forward();

    Serial.println("Leg positions:");
    print_xyz(lcs[LEG_HR], lcs[LEG_HR+1], lcs[LEG_HR+2]);
    print_xyz(lcs[LEG_FR], lcs[LEG_FR+1], lcs[LEG_FR+2]);
    print_xyz(lcs[LEG_FL], lcs[LEG_FL+1], lcs[LEG_FL+2]);
    print_xyz(lcs[LEG_HL], lcs[LEG_HL+1], lcs[LEG_HL+2]);

    Serial.println("Done");
}

void loop()
{
}

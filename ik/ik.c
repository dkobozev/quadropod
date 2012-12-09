#include <stdio.h>
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

#define IK_TOLERANCE 1

//#define DEBUG 1

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

    return round(a * 100) / 100;
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
        if (fabs(n2 - 1) > 0.001) {
            // no solutions
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
       float *iksolutions)
{
    float th1[2], th2[2], th3[2];
    float solutions[24];
    int i, j, k;
    int n = 0;
    float px, py, pz;
    int valid[8];
    int n_valid = 0;

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
#ifdef DEBUG
                                printf("theta2 out of range: %f\n", th2[i]);
#endif
                                continue;
                            }
                            solutions[3*n] = th1[i];
                            solutions[3*n+1] = th2[k];
                            solutions[3*n+2] = th3[j];
                            n++;
                        }
                    }
#ifdef DEBUG
                    else {
                        printf("No solutions for theta2\n");
                    }
#endif
                }
            }
#ifdef DEBUG
            else {
                printf("No solutions for theta3\n");
            }
#endif
        }
    }
#ifdef DEBUG
    else {
        printf("No solutions for theta1\n");
    }
#endif

#ifdef DEBUG
    printf("Found %d possible solutions:\n", n);
    for (i = 0; i < n; i++) {
        printf("(%f, %f, %f)\n", solutions[3*i], solutions[3*i+1], solutions[3*i+2]);
    }
#endif

    // test for valid solutions
    for (i = 0; i < n; i++) {
        fk(A1, A2, A3, A4, solutions[3*i], solutions[3*i+1], solutions[3*i+2],
           D1, D2, D3, &px, &py, &pz);
        if (    fabs(px - x) < IK_TOLERANCE &&
                fabs(py - y) < IK_TOLERANCE &&
                fabs(pz - z) < IK_TOLERANCE) {
            valid[n_valid] = i;
            n_valid++;
        }
    }

#ifdef DEBUG
    printf("Found %d valid solutions:\n", n_valid);
    for (i = 0; i < n_valid; i++) {
        printf("(%f, %f, %f)\n", solutions[3*valid[i]],
                                 solutions[3*valid[i]+1],
                                 solutions[3*valid[i]+2]);
    }
#endif

    for (i = 0; i < n_valid; i++) {
        iksolutions[3*i] = solutions[3*valid[i]];
        iksolutions[3*i+1] = solutions[3*valid[i]+1];
        iksolutions[3*i+2] = solutions[3*valid[i]+2];
    }

    // return the number of valid solutions
    return n_valid;
}

int main(int argc, char *argv[])
{
    float x, y, z;
    float fx, fy, fz;
    float theta1, theta2, theta3;
    float solutions[24];
    float th1ik, th2ik, th3ik;
    int i, n, found;

    int testall = 1;

    if (!testall) {
        theta1 = 0;
        theta2 = -57;
        theta3 = 162;
        fk(A1, A2, A3, A4, theta1, theta2, theta3, D1, D2, D3, &fx, &fy, &fz);
        printf("FK for angles (%f, %f, %f): (%f, %f, %f)\n", theta1, theta2, theta3, fx, fy, fz);

        if (n = ik(fx, fy, fz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
            printf("Solutions:\n");
            for (i = 0; i < n; i++) {
                printf("(%f, %f, %f)\n", solutions[3*i],
                                         solutions[3*i+1],
                                         solutions[3*i+2]);
            }
        }
    } else {
        for (theta1 = 0; theta1 >= -180; theta1--) {
            for (theta2 = -90; theta2 <= 90; theta2++) {
                for (theta3 = 0; theta3 <= 180; theta3++) {
                    fk(A1, A2, A3, A4, theta1, theta2, theta3, D1, D2, D3, &fx, &fy, &fz);

                    if (n = ik(fx, fy, fz, A1, A2, A3, A4, D1, D2, D3, solutions)) {
                        found = 0;
                        for (i = 0; i < n; i++) {
                            th1ik = round(solutions[3*i]);
                            th2ik = round(solutions[3*i+1]);
                            th3ik = round(solutions[3*i+2]);
                            if (th1ik == theta1 && th2ik == theta2 && th3ik == theta3) {
                                found = 1;
                            }
                        }
                        if (!found) {
                            printf("No valid solutions found for (%f, %f, %f):\n",
                                   theta1, theta2, theta3);
                            for (i = 0; i < n; i++) {
                                printf("(%f, %f, %f)\n", solutions[3*i],
                                                         solutions[3*i+1],
                                                         solutions[3*i+2]);
                            }
                        }
                    } else {
                        printf("No solutions for (%f, %f, %f)\n", theta1, theta2, theta3);
                    }
                }
            }
            printf("Percent done: %.2f\n", theta1 / -180.0 * 100);
        }
    }

    return 0;
}

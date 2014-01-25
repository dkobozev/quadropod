#include "leg.h"


void joint_init(joint_t *joint, int pin, int start, int dir, int pulse_min, int pulse_max)
{
    pinMode(pin, OUTPUT);

    Servo *servo = new Servo;
    servo->attach(pin, SERVO_MIN + pulse_min, SERVO_MAX + pulse_max);

    joint->servo = servo;
    joint->start = start;
    joint->dir   = dir;
}

void joint_rotate(joint_t *joint, int angle)
{
    int actual = (joint->start + joint->dir * angle) % 360;
    joint->servo->write(actual);
    joint->angle = angle;
}

void move_execute(joint_t *joints, int *move)
{
    int steps = move[0];
    int from, to, next, angle, alpha, beta;

    double increments[NUM_JOINTS];
    double counters[NUM_JOINTS];


    // init increments and counters
    for (int joint = 0; joint < NUM_JOINTS; joint++) {
        from = joints[joint].angle;
        to = move[joint + 1];

        alpha = (360 + to - from) % 360;
        beta  = (360 + from - to) % 360;
        angle = (alpha < beta) ? alpha : beta;

        if (from > to)
            angle = -angle;

        increments[joint] = angle / (double) steps;
        counters[joint] = 360 + from;
    }

    for (int step = 1; step <= steps; step++) {
        for (int joint = 0; joint < NUM_JOINTS; joint++) {
            counters[joint] += increments[joint];
            next = ((int) (counters[joint] + 0.5)) % 360;

            // take care of any rounding errors
            to = move[joint + 1];
            if ( (increments[joint] > 0 && next > to) ||
                 (increments[joint] < 0 && next < to) ) {
                next = to;
            }

            joint_rotate(&joints[joint], next);
        }
        delay(20);
    }
}

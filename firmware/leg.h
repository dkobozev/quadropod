#ifndef __LEG_H__
#define __LEG_H__

#include <Arduino.h>
#include <Servo/Servo.h>

#define NUM_JOINTS 12
#define LEN_MOVE   NUM_JOINTS + 1

#define SERVO_MIN 544
#define SERVO_MAX 2400

typedef struct joint {
    Servo *servo;
    int angle; // current joint angle
    int start; // starting angle; joint range is start .. start + 180
    int dir;   // direction
} joint_t;

void joint_init(joint_t *joint, int pin, int start, int dir, int pulse_min, int pulse_max);
void joint_rotate(joint_t *joint, int angle);
void move_execute(joint_t *joints, int *move);

#endif

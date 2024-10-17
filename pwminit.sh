#!/bin/bash

# Check if the directory exists
if [ ! -d "/sys/class/pwm/pwmchip0/pwm0" ]; then
    # Export the PWM0 if it does not exist
    echo 0 > /sys/class/pwm/pwmchip0/export
fi

# Set PWM parameters
echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/period
echo 500000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
echo "normal" > /sys/class/pwm/pwmchip0/pwm0/polarity
echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable

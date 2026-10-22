# Freenove hardware evidence for Omega1

Local source found on the workstation: `Desktop/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi`.
Upstream: https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi
Inspected checkout commit: `a49db4b9dfa9b7a82d172354cb3b4e0ed64985e5`.

## Documented kit facts

- Ordinary-wheel tutorial, printed page 3 (PDF page 7): four DC speed reduction motors, four driven wheels, two servo packages. Visual inspection shows yellow plastic gearmotor housings matching the user's description.
- Printed page 4 (PDF page 8): camera, line-tracking module, HC-SR04 ultrasonic module, and connection-board V1.0/V2.0 alternatives.
- Printed page 51: connection board joins Raspberry Pi and smart-car board.
- Printed page 52: two 18650 batteries; two servos connect to Servo0/Servo1.
- `Code/Server/motor.py`: four separately controlled motor positions; PCA9685 address 0x40, PWM initialization at 50 Hz, signed duty range -4095..4095. These are software settings, NOT motor RPM, torque, gear ratio, or speed calibration.
- The ordinary-wheel program turns with opposing left/right commands. This establishes a four-wheel skid-steer reference architecture, not a two-wheel/caster architecture.
- Both ordinary- and mecanum-wheel tutorials exist. Local `car.py` imports `Ordinary_Car`, which indicates the provided code path, not proof of wheels fitted to Omega1.
- `parameter.py` distinguishes Connect_Version from Pcb_Version. These must be recorded separately. Defaults do not establish installed hardware revisions.
- `adc.py` uses address 0x48 with version-dependent scaling. ADS7830, PCF8591 and PCA9685 datasheets are bundled; presence of a datasheet alone does not establish the fitted ADC.

## Implications and remaining unknowns

The user's reference to this kit makes it the candidate hardware family for Omega1. Kit parts remain unconfirmed installed components until matched to the physical assembly. Existing confirmed Raspberry Pi 4 inventory remains unchanged.

Ordinary wheels require a four-wheel skid-steer generator; mecanum wheels require a different controller and wheel/contact model. The current two-wheel reference generator must not be used as Omega1's model.

No reliable chassis dimensions, wheel diameter, wheelbase, track width, assembled mass, gear ratio or motor torque/RPM specification was identified in the reviewed parts/assembly material and code. Keep those unknown. Measure front-rear axle spacing as well as left-right wheel centre spacing.

## Source handling

The upstream README identifies its materials as CC BY-NC-SA 3.0. RobotForge records original factual summaries, commit references and file hashes here; no vendor PDF, image or implementation is copied into this repository.

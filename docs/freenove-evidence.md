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

## Online listing and image cross-check (2026-10-21)

- [Official FNK0043 listing](https://store.freenove.com/products/fnk0043) identifies Raspberry Pi compatibility and two required 3.7 V 18650 batteries, with Pi and batteries excluded from the kit.
- [Official assembled-car image](https://store.freenove.com/cdn/shop/files/FNK0043.MAIN_fac56ef0-085d-46b0-8743-ab12d50d9efe.jpg?v=1790071965&width=416) visually shows four ordinary yellow-hub tires, a board chassis, Raspberry Pi, and front camera/ultrasonic assembly. This is a vendor reference, not a photo of Omega1.
- [Official size-and-packaging image](https://store.freenove.com/cdn/shop/files/FNK0043.PT06_16e483ca-2688-4e9f-aea4-dbc5e3068d79.jpg?v=1790071965&width=416) explicitly labels the assembled ordinary-wheel car as **21 cm long, 15 cm wide, 12.5 cm high**. It separately labels the box as 26.7 × 13.6 × 7.2 cm. The car values are nominal outer envelope dimensions, NOT chassis-only dimensions, wheel track or wheelbase. They cannot directly populate `chassis_dimensions_m`.
- [Amazon candidate B07YD2LT9D](https://www.amazon.com/dp/B07YD2LT9D) was identified via external listing indexes. Direct browser access reached a shopping interstitial and then redirected to the homepage; the web extraction did not expose reliable product specifications. ASIN-to-variant association is provisional.
- External mirrors disagree about mass and dimensions, and some explicitly report package dimensions. These are not accepted as simulation inputs. No assembled mass or wheel dimensions are asserted.

Images are linked as visual references, not redistributed in the project. No perspective-derived measurements are promoted to physical specifications. Next useful measurements remain tire diameter/width, wheel centre track, front-rear wheelbase, individual masses and installed board variants.

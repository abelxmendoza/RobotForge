# Omega1 hardware evidence

The user identified Omega1 as a Raspberry Pi 4 rover. The board revision and rover geometry are unknown. A Jetson Orin Nano and Intel RealSense camera are available, but their installation on Omega1 has not been confirmed; they are not declared installed components.

Before generating a physically meaningful model, collect:

- Chassis length, width, height, total mass, center of mass, and measured or CAD-derived inertia.
- Wheel count, radius, width, positions, axle separation, and drive/steering arrangement.
- Motor and gearbox model numbers, gear ratios, torque/speed ratings, and controller documentation.
- Battery and power distribution details.
- Sensor exact models, mounting transforms, calibration, and intended update rates.
- CAD and datasheet sources, permissions, revisions, units, and checksums.

Unknown values stay null. Do not substitute plausible dimensions for measurements. Any future illustrative simulation must be explicitly identified as a synthetic fixture.

## Measurement worksheet

| Field | Omega1 value | How to obtain |
| --- | --- | --- |
| Drive arrangement / wheel count | unknown | photo of underside and drivetrain |
| Chassis length × width × height (m) | unknown | tape measure, excluding wheels |
| Chassis-only mass (kg) | unknown | scale, excluding wheels/caster |
| Wheel radius / width (m) | unknown | measure unloaded tire |
| Left-right wheel centre separation (m) | unknown | axle measurement |
| Mass per wheel (kg) | unknown | scale or datasheet |
| Caster radius / mass | unknown | measure if present |
| Motor, gearbox, controller model | unknown | labels / datasheets |

For each measurement, record date, method, uncertainty and source photo/document. Do not copy the reference fixture's values into Omega1.

## Located vendor documentation

See [Freenove evidence](freenove-evidence.md) for the identified local kit repository. Four driven wheels and four geared motors are documented kit facts. Ordinary-wheel skid steer versus mecanum configuration and installed board revisions still require confirmation. The two-wheel/caster fixture is not an Omega1 drivetrain model.

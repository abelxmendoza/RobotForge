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

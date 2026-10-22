# Multi-robot compatibility experiment

The shared `RobotDescription` interface accepts existing hardware manifests,
URDF, expanded Xacro and single-model SDF. Its version 1 JSON interchange format
contains a source, format, authoritative `description_xml`, and derived indexes
of links, joints, sensors, actuators and controller extensions. Link XML retains
geometry, collision, inertial and frame information; joint XML retains limits,
axes, dynamics and mimic relationships. Unknown extensions remain in the XML.
The JSON output can be imported again. It is separate from the existing version 1
hardware inventory manifest, distinguished by `description_xml`.

This is a conservative first schema implementation. Validation checks names,
references and URDF tree connectivity. It does **not** certify inertias, joint
limits, controller compatibility, asset availability or physical correctness.
`gz sdf -k` adds native SDFormat validation. SDF closed loops remain supported;
URDF requires a tree. Multi-model worlds require splitting before import.
Cross-format export currently supports URDF to SDF through libsdformat; SDF to
URDF fails explicitly. Conversion may reduce fixed joints according to
libsdformat semantics. Exact XML preservation applies to same-format exports.

## Start on Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,importers]'
pytest -q
robotforge import-model robots/omega1/prototype.json --output /tmp/omega1.json
robotforge export-model /tmp/omega1.json --format sdf --output /tmp/omega1.sdf
```

Gazebo Harmonic (`gz sim`, `gz sdf`) is an external runtime dependency. Xacro is
optional (`importers` extra). Xacro processing executes its normal include and
substitution machinery: use trusted robot packages. Package lookup via ROS
requires sourcing the corresponding installed ROS workspace. The Burger test
only needs the local description package and Xacro.

## Official TurtleBot3 fixture

The initial experiment uses the official ROBOTIS Humble description at commit
`90a68bd2e3c61c12966779da89d8eeaec82730e9`. Source meshes stay in that external
checkout; they are not copied into RobotForge.

```bash
mkdir -p work
git clone --branch humble https://github.com/ROBOTIS-GIT/turtlebot3.git work/turtlebot3
git -C work/turtlebot3 checkout 90a68bd2e3c61c12966779da89d8eeaec82730e9
python scripts/compatibility.py \
  --turtlebot3-description work/turtlebot3/turtlebot3_description \
  --output work/compatibility --motion
```

The runner imports both robots through the same interface, writes their shared
JSON descriptions, converts them with libsdformat, supplies explicit differential
drive capabilities, resolves TurtleBot3 package meshes, and validates the worlds.
With `--motion`, it launches each model in its own headless Gazebo world and tests
forward movement and rotation. Its `report.json` records passed, failed or
not-run checks and measured wheel odometry. A failed check produces a nonzero
exit code. Without `--motion`, overall status is `partial`, never motion passed.
Generated SDF includes absolute local mesh paths and must be regenerated on a
new machine. Robot descriptions without mesh assets can still be imported.

Burger wheel radius is 0.033 m and centre separation is 0.160 m, taken from its
URDF wheel collision geometry and wheel joint origins. Omega1 uses the existing
four-wheel prototype's explicit assumptions. Drive capability configuration is
supplied separately from topology: other robot classes can retain their standard
XML but need their own simulation/control adapter.

Motion evidence is wheel-derived odometry, not independent world displacement.
Passing it does not verify wheel slip, sensors, ROS 2 integration or calibration.
Measured Omega1 remains blocked by the incomplete `robots/omega1/robot.json`.
The AI assistant, PX4, MuJoCo and Isaac Sim remain subsequent stages.

## Initial local result

On the initial Ubuntu run, all 55 Python tests passed. Both models passed native
SDF validation and forward/turn smoke checks. Omega1 prototype reported 1.258 m
forward odometry and 1.880 rad rotation; TurtleBot3 Burger reported 1.280 m and
1.571 rad. These are separate bounded runs and wheel-derived measurements.
The committed runner regenerates the report; generated files remain under the
ignored `work/` directory.

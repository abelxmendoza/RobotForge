# Reproducible simulation milestone

## Verified now

The synthetic reference rover is generated from a versioned hardware manifest, validated with libsdformat, and driven in headless Gazebo Harmonic. It is NOT a measured Omega1 model. It uses uniform primitive solids for inertia and a frictionless spherical caster approximation. Odometry is wheel-derived; this acceptance test does not establish traction accuracy or independent ground-truth displacement.

```bash
source .venv/bin/activate
robotforge generate-sdf robots/reference/robot.json --output /tmp/reference.sdf
gz sdf -k /tmp/reference.sdf
python scripts/smoke_gazebo.py
```

The test isolates Gazebo Transport with a unique partition, waits for odometry, commands 0.2 m/s, requires at least 0.1 m odometry displacement, and terminates its server. No remote model downloads or GUI are needed. Run it on a host permitting local Gazebo networking.

For interactive inspection: `gz sim -r /tmp/reference.sdf`.

URDF export: `robotforge generate-urdf robots/reference/robot.json --output /tmp/reference.urdf`. This exports primitive geometry, inertias, and joints. SDF is the current executable simulation artifact; URDF does not yet embed the Gazebo drive plugin. Xacro is deferred until parameter reuse is needed.

## ROS 2 Humble + Harmonic

Official matrix: https://gazebosim.org/docs/harmonic/ros_installation/

Humble normally pairs with Fortress; Humble/Harmonic is a non-default pairing marked use with caution. The official OSRF repository provides `ros-humble-ros-gzharmonic`. Do not blindly install default `ros-humble-ros-gz`, which targets Fortress. Review the official repository setup and package conflicts before modifying an existing ROS installation.

This host has Humble and Gazebo 8.15.0, but no ros_gz_bridge executable. ROS bridge acceptance is therefore NOT yet verified. After the matching bridge is available, run the generated world and bridge these topics:

```bash
source /opt/ros/humble/setup.bash
ros2 run ros_gz_bridge parameter_bridge \
  '/model/reference_rover/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist' \
  '/model/reference_rover/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry'
ros2 topic pub --once /model/reference_rover/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.2}}'
ros2 topic echo /model/reference_rover/odometry
```

Bridge syntax reference: https://github.com/gazebosim/ros_gz/tree/humble/ros_gz_bridge

These ROS commands are documented setup steps, not a claim of successful ROS verification.

## Omega1 gate

`robotforge generate-sdf robots/omega1/robot.json` fails until required geometry, masses, drive arrangement, and source evidence are supplied. See hardware.md. Only two-wheel differential drive plus a caster is implemented; a different Omega1 drivetrain requires a corresponding generator implementation.

Manifest geometry is SI: metres, kilograms, radians. `chassis_mass_kg` excludes wheels and caster. `wheel_separation_m` is wheel centre-to-centre. Source evidence is mandatory. `measured` is a user assertion, not independent certification. Primitive inertia assumes uniform solids; it is a documented approximation rather than measured inertia.

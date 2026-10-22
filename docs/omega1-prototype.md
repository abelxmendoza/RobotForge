# Omega1 development prototype

This is a runnable approximation based on the Freenove FNK0043 ordinary-wheel architecture. It is not a measured digital twin. The ordinary-wheel choice is provisional; it does not model mecanum wheels. The measured manifest `robots/omega1/robot.json` remains incomplete and separate.

## Run

```bash
source .venv/bin/activate
robotforge generate-sdf robots/omega1/prototype.json --output /tmp/omega1.sdf
gz sdf -k /tmp/omega1.sdf
gz sim -r /tmp/omega1.sdf
```

In another terminal, drive or turn:

```bash
gz topic -t /model/omega1_prototype/cmd_vel -m gz.msgs.Twist -p 'linear: {x: 0.2}'
gz topic -t /model/omega1_prototype/cmd_vel -m gz.msgs.Twist -p 'angular: {z: 0.3}'
gz topic -t /model/omega1_prototype/cmd_vel -m gz.msgs.Twist -p 'linear: {x: 0}, angular: {z: 0}'
```

The commands persist until replaced. These are simulation topics, not commands to physical motors.

Automated headless checks (each starts/stops its own isolated world):

```bash
python scripts/smoke_gazebo.py robots/omega1/prototype.json
python scripts/smoke_gazebo.py robots/omega1/prototype.json --turn
```

URDF export:

```bash
robotforge generate-urdf robots/omega1/prototype.json --output /tmp/omega1.urdf
```

## Explicit assumptions

| Parameter | Prototype value | Evidence / status |
| --- | --- | --- |
| Four driven wheels | 4 | Vendor ordinary-wheel kit architecture |
| Vendor overall reference envelope | 0.21 × 0.15 × 0.125 m | Official size image; not chassis-only dimensions |
| Primitive chassis box | 0.21 × 0.09 × 0.02 m | Assumption; includes lumped body, not CAD |
| Wheel radius | 0.0325 m | Assumption, not identified manufacturer specification |
| Wheel width | 0.025 m | Assumption |
| Wheel centre track | 0.125 m | Assumption; yields nominal 0.15 m outside width |
| Front/rear wheelbase | 0.13 m | Assumption |
| Lumped chassis mass | 0.5 kg | Assumption, includes omitted equipment |
| Each wheel mass | 0.035 kg | Assumption |
| Inertia | Uniform box/cylinder formula | Approximation |

The box and wheel layout is not a reconstruction of the vendor's exact 21 cm envelope. Camera, pan/tilt, batteries, sensors and Pi are currently lumped into the body, without separate geometry or sensor plugins. Gazebo's default contact settings and ideal joint controller are not calibrated motor/traction models. No motor RPM, torque, gear ratio, battery capacity or sensor calibration is asserted.

Acceptance checks wheel-derived odometry, not independent ground-truth pose. Passing movement tests demonstrates the generated drive chain works, not accurate tire slip or real-world turning radius. ROS bridge verification remains a separate task.

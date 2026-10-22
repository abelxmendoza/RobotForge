# RobotForge

An open-source foundation for documenting hardware and generating reproducible robot models.

## Status

v0.1 provides a versioned JSON hardware manifest, validation CLI, Omega1 inventory, and automated tests. Primitive URDF/SDF generation and headless Gazebo prototype motion are available; a 3D assembler and physically calibrated Omega1 simulation are not yet implemented. JSON keeps this initial scaffold dependency-free and is also valid YAML 1.2.

## Ubuntu development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
robotforge validate robots/omega1/robot.json
pytest -q
robotforge simulation-gaps robots/omega1/robot.json
```

The final command deliberately exits 1 until missing simulation inputs are supplied; validation success only establishes manifest structure, not physical correctness.

Target workstation: Ubuntu 22.04 bare-metal, Intel Core Ultra 9 275HX, RTX 5070 Laptop GPU (8 GB), 64 GB RAM. ROS 2 Humble and Gazebo Harmonic are intended integration targets; this scaffold installs neither. Their bridge compatibility must be verified before pinning integration dependencies.

See [roadmap](docs/roadmap.md) and [hardware measurements](docs/hardware.md).

## Generated simulation prototype

A clearly labeled synthetic two-wheel rover now exercises manifest → SDF → Gazebo → velocity command → odometry. Primitive URDF export is also available. See [simulation setup and acceptance test](docs/simulation.md). Omega1 remains blocked on real measurements; the ROS bridge is not yet verified.

## Omega1 four-wheel prototype

A provisional ordinary-wheel Freenove model can now drive and turn in Gazebo. Geometry and masses that lack evidence are explicitly labeled prototype assumptions. See [run commands and parameter provenance](docs/omega1-prototype.md). The measured Omega1 manifest remains incomplete.

```bash
robotforge generate-sdf robots/omega1/prototype.json --output /tmp/omega1.sdf
gz sim -r /tmp/omega1.sdf
```

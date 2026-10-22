# RobotForge

An open-source foundation for documenting hardware and generating reproducible robot models.

## Status

v0.1 provides a versioned JSON hardware manifest, validation CLI, Omega1 inventory, and automated tests. There is no 3D assembler, URDF generator, or working Gazebo simulation yet. JSON keeps this initial scaffold dependency-free and is also valid YAML 1.2.

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

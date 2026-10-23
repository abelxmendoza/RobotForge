# RobotForge

An open-source foundation for documenting hardware and generating reproducible robot models.

**By Abel Mendoza.**

RobotForge turns robot descriptions — a plain-English idea, a parts list, or a published open-robot design — into validated, simulation-tested robot models. A structured hardware registry (parts with compatibility rules, sources, and licenses) is the single source of truth; deterministic generators render URDF/SDF from it; validators check structure, physics, and drivetrain kinematics; and a headless Gazebo acceptance run — spawn, settle, drive, turn, compare odometry — decides whether the robot actually works.

Pre-existing open-source foundation begun October 2026. The registry-first architecture is the point: language models fill in the schema; they never hand-write robot XML.

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

## Universal description interface (in progress)

URDF, Xacro and single-model SDF now share a loss-preserving description interface.
Existing rover manifests enter the same pipeline. The Gazebo adapter accepts
explicit wheel assignments and dimensions, and the compatibility runner writes
machine-readable import, export and optional motion evidence for the provisional
Omega1 and official TurtleBot3 Burger. See [setup and scope](docs/multi-robot.md).
This does not complete the measured Omega1 acceptance gate.

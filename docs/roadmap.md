# Roadmap

1. Expand registry v1 with relationship validation, component revisions, provenance, and migration policy.
2. Add local CAD/datasheet assets with hashes, units, and source metadata.
3. Evaluate FreeCAD/RobotCAD import/export against documented sample files.
4. Generate URDF/Xacro with link-tree, units, joint, and inertia checks.
5. Verify ROS 2 Humble / Gazebo Harmonic bridge support in a reproducible environment; generate Omega1 from measured data, spawn it, command motion, and assert odometry displacement.
6. Add FastAPI, React, and Three.js workspace after simulation acceptance.
7. Expand sensors, actuators, revisions, and assembly relationships.
8. Expose validated engineering operations through MCP.

First simulation acceptance: a clean environment can generate the model, spawn Omega1, send a velocity command, and observe displacement with documented commands and tests.

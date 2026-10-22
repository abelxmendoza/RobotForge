# Initial verification

- Clean Python 3.10 virtual environment: editable installation with dev dependencies succeeded.
- `env -u PYTHONPATH .venv/bin/pytest -q`: 16 passed.
- `.venv/bin/robotforge validate robots/omega1/robot.json`: passed.
- Simulation inputs remain incomplete; no Gazebo motion verification is claimed.

On a shell with ROS sourced, the inherited PYTHONPATH can expose ROS pytest plugins outside the virtual environment. In this environment plain pytest attempted to import launch_testing and failed due to missing PyYAML. Run the foundation tests with `env -u PYTHONPATH pytest -q` to isolate them from the ROS installation.

# RobotForge market research and hackathon hold (pre-event notes)

**Recorded:** 2026-10-23. **Status:** Research and planning only. **No hackathon implementation authorized.**

## Important competition boundary

The hackathon is expected to start **Monday, 2026-10-26**, but official rules, eligible tracks, permitted starter code, and exact build window **have not been released or verified**. Do not implement, generate project-specific code, create demo assets, preassemble a submission, or present existing RobotForge work as work completed during the event. Stop at research until the organizers publish the rules and the official start time arrives. Research notes are not a claim of hackathon eligibility. If the rules prohibit pre-event documentation or using this existing repository, follow the rules and keep this repository separate from the submission. Seek organizer clarification where needed.

At kickoff: read official rules, confirm whether prior work and open-source frameworks are permitted, record the baseline commit, identify pre-existing versus event-created work, and only then choose a scoped hackathon deliverable. Preserve commit history and provenance. **No automatic build at kickoff.** The team decides after reviewing the rules.

## Problem and market thesis (hypotheses, not validated customer demand)

Robot model conversion and simulation are already addressed by established tools; the more interesting potential gap is **repeatable verification of robot behavior and field failures** across models, simulators, and software revisions.

Potential customers/users: robotics test engineers, autonomy developers, field reliability teams, researchers, and ROS 2 maintainers. We have **not** established willingness to pay, product-market fit, market share, or a novel defensible advantage. Validate by interviewing 5–10 robotics engineers after the event as appropriate.

## Existing ecosystem to evaluate (do not implement yet)

- Gazebo / SDFormat / ros_gz: simulator, structural checks, ground-truth pose, ROS 2 integration — https://gazebosim.org/
- robot_descriptions.py: reusable open robot descriptions and regression fixtures — https://github.com/robot-descriptions/robot_descriptions.py
- yourdfpy: independent URDF parsing/validation — https://github.com/clemense/yourdfpy
- Onshape-to-Robot: CAD-to-robot-model conversion — https://github.com/Rhoban/onshape-to-robot
- MuJoCo: possible future cross-simulator validation — https://github.com/google-deepmind/mujoco
- ROS 2 MCP: inspect ROS graph and telemetry, preferably read-only first — https://github.com/wise-vision/ros2_mcp
- Gazebo MCP: evaluate real-runtime support and safety before trusting tool outputs — https://github.com/kvgork/gazebo-mcp
- Gazebo Fuel public models — https://app.gazebosim.org/
- GitHub REST API: repository/model discovery and provenance — https://docs.github.com/en/rest
- Onshape API: account/plan/usage rights must be verified — https://cad.onshape.com/glassworks/explorer/

Check each dependency's license, compatibility, maintenance, and reproducibility before adoption. Do not assume all APIs are unlimited or free for commercial use.

## Candidate directions (not committed hackathon scope)

1. **Robot simulation acceptance gate:** independently compare Gazebo world displacement with wheel odometry, enforce tolerances, and produce evidence with exact versions/revisions.
2. **Fault-injection regression suite:** ROS 2 sensor dropout, stale odometry, communications interruption, and expected safe responses.
3. **Field incident to replayable test:** import recorded telemetry/ROS bags, label reconstruction uncertainty, reproduce a failure when possible, and prevent regression.
4. **Multi-robot safety verification:** separation, task reassignment, deadlock, and recovery checks; potentially reuse lessons from PX4 work only where event rules allow.

Most pragmatic *post-approval* candidate: a narrow, reproducible mobile-robot regression demo using Gazebo and ROS 2. This is a **proposal**, not a decision to build or a claim of novelty.

## RobotForge pre-event baseline and open questions

Existing RobotForge code already includes hardware registry, URDF/SDF generation, Gazebo motion tooling, and compatibility tests. Current documented motion evidence is wheel-derived odometry, not independent world-ground-truth verification. Real Omega1 geometry/masses remain unmeasured; ROS 2 bridge behavior remains unverified. These capabilities predate the event and must never be represented as newly built during it.

Questions to resolve after rules release:
- Is a pre-existing project/repository allowed, or must the hackathon submission be new?
- Are research notes, designs, templates, and AI assistance allowed?
- Can external libraries, existing code, and simulation models be used, and with what attribution?
- When precisely does the official build window begin/end, and what deliverables are required?
- Does the team agree on a scope and ownership boundaries?

## Success criteria after authorization

An independently repeatable test that fails when the robot behaves incorrectly, passes when it behaves correctly, and reports exact inputs, source revision, simulator version, and evidence. Avoid claiming physical fidelity or sim-to-real calibration without measurements.

**Freeze instruction:** No code, tests, infrastructure, integration, or demo work for the hackathon until official rules are checked and the event's build window opens.

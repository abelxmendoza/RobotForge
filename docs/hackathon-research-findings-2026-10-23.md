# RobotForge pre-event hackathon research findings (2026-10-23)

**Status:** Research and planning only. **No implementation authorized.** Official Meta Global AI Developer Hackathon rules have not been verified. This document records findings from an architecture audit, competitive scan, and feasibility review. It does not claim eligibility or represent work completed during the event.

## Architecture audit summary

**CONFIRMED existing capabilities:**
- Versioned JSON hardware manifests (schema v1) with structural validation CLI and `simulation-gaps` checker.
- Deterministic primitive SDF/URDF generation for differential 2-wheel + caster and skid-steer 4-wheel rovers.
- Shared `RobotDescription` interface for import/export (URDF, expanded Xacro, single-model SDF, manifests) with structural checks.
- Gazebo adapter that injects DiffDrive plugin with explicit joint assignments.
- Headless Gazebo motion smoke tests (isolated via `GZ_PARTITION`) that check wheel-derived odometry displacement or yaw after a velocity command.
- Multi-robot compatibility runner covering Omega1 prototype + official TurtleBot3 Burger with motion evidence.
- Explicit labeling of assumptions; measured Omega1 remains blocked; ROS bridge unverified.

**Limits (not claimed as complete):**
- Verification is wheel-odometry only; no independent world-pose comparison or traction validation.
- No physical calibration of Omega1.
- Roadmap items (full CAD import, MCP, workspace UI) are not implemented.

## Competitive gap

No single mature open-source project provides a lightweight, registry-driven, provenance-explicit acceptance gate that compares DiffDrive wheel odometry against simulator world ground truth for mobile bases. Closest pieces:
- `robot_descriptions.py`, `onshape-to-robot` (conversion/catalogs).
- Scenario Execution for Robotics (multi-backend scenarios + fault injection).
- ROS-RVFT guidelines and various ROS fault-injection toolkits.
- Gazebo Fuel / official DiffDrive examples (baseline models and odometry topics).

The gap is real for a narrow mobile-base fixture but the building blocks exist.

## Feasibility of independent ground-truth acceptance gate

**CONFIRMED:**
- DiffDrive publishes wheel odometry on `/model/<name>/odometry`.
- Gazebo Harmonic provides `gz-sim-pose-publisher-system` (PosePublisher) for model/world poses. Parameters include `publish_model_pose`, `publish_nested_model_pose`, `update_frequency`, and custom `topic`.
- Existing isolation and smoke infrastructure can be extended.

**Requires validation on target host (Harmonic 8.15):**
- Exact topic names and message fields.
- Behavior of `publish_model_pose` vs `publish_nested_model_pose`.
- Timing between publishers and meaningfulness of divergence under current frictionless/ideal-joint models.

## Recommended 10-day concept (if rules permit)

Narrow extension of existing capability: generate SDF, run headless Gazebo, command a fixed velocity profile, capture both wheel odometry and independent world model pose (via PosePublisher), assert absolute motion and relative divergence within documented tolerances, and emit a machine-readable evidence report with versions, SHA, inputs, and explicit limitations (sim-truth only).

Optional light Meta model use (Muse Spark / Muse Code) for scenario wording or report summarization only; core assertion remains deterministic.

## Risks and constraints

- Official rules are the controlling constraint (prior work, AI assistance, submission format still UNKNOWN).
- ROS 2 + Harmonic bridge remains unverified and non-default.
- Scope creep into fault injection, bag replay, multi-robot, or measured Omega1 exceeds the window.
- Provenance: any adapted pre-event code must be disclosed. New-repository timestamp does not prove originality of content.

## Proposed scope (if rules allow after kickoff review)

If the official rules permit prior work and the build window opens, the eligible deliverable is a single, reproducible acceptance gate for one or two primitive mobile bases (reference rover and/or Omega1 prototype or TurtleBot3 Burger). The gate compares wheel-derived odometry against PosePublisher world pose, fails on divergence beyond documented tolerances, and produces an auditable JSON report. No measured geometry, no full ROS bridge, and no broader fault-injection or multi-robot features are included in this scope.

**Freeze remains in effect until rules are checked and the official start time arrives.**

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

## Confirmed event details and approval (2026-10-23 email review)

- **Event:** Meta Global AI Developer Hackathon, hosted via Cerebral Valley: https://cerebralvalley.ai/e/meta-ai-developer-hackathon
- **Acceptance:** Participant received an **APPROVED** status email dated 2026-10-22. This confirms acceptance, not the eligibility of a particular project or repository.
- **Format:** Remote; scheduled **October 26 through November 4, 2026** (10 days). The event calendar invite indicates an October 26 start at 12:00 Eastern / 09:00 Pacific and November 4 end at 21:00 Eastern / 18:00 Pacific; **verify official build-window times and submission deadline against the organizer's published rules** rather than treating the calendar as authorization to code.
- **Promotional terms:** $1M aggregate prize pool; selected participants advertised $150 Meta Model API credits and access to Muse Code, subject to terms and actual credit allocation.
- **Theme alignment to investigate:** Robotics/physical systems under the event's frontier-oriented themes may fit a verification-focused entry, but thematic fit does not prove eligibility or competitiveness.
- **Rules status:** No separate official rules announcement was found in the relevant Gmail searches on 2026-10-23. The event page should be checked again at kickoff; this document is not a substitute for the final rules.

## Proposed two-repository approach (decision pending rules)

**Existing `RobotForge` repository:** Retain as the **pre-event brainstorming, research, architecture, and prototype baseline**. It contains genuine pre-event code (registry, URDF/SDF generation, Gazebo tooling, tests), not merely empty scaffolding. The initial prototype was developed with Meta Muse before the competition. Preserve its actual history and source attribution. Do not relabel existing implementation as event-created work.

**Potential new `RobotForge-Hackathon` repository:** **Do not create before the event.** If rules permit, create a distinct repository *after the official start* and rules review for the eligible event implementation, verification evidence, demo, and submission. The repository creation timestamp proves when the repository was created **but does not prove that copied code was written then**. Explicitly identify any imported or adapted pre-event code and third-party dependencies. If pre-existing code is prohibited, start implementation from scratch within the allowed window; do not copy old code and disguise its origin.

**At the authorized kickoff:**
1. Read and save official rules/terms; verify build start/end, tracks, team size, permitted prior work, AI assistance, open-source licensing, judging, and submission format. Request organizer clarification for ambiguity.
2. Record the existing RobotForge baseline commit SHA and a dated inventory of pre-event source and documentation.
3. Agree with teammates on the submission scope and how to disclose prior work; decide whether a fresh repository is eligible.
4. Only then create the submission repository and begin eligible implementation, keeping truthful commit history and clear provenance.
5. Maintain an event-work log of new commits, tests, demonstrations, dependencies, and measurable results.

**Current user direction:** Brainstorming and competitor/problem research may continue before kickoff; no hackathon implementation, new submission repository, tests, demos, or integration before the rules and official build window. No automatic action is scheduled for Monday.

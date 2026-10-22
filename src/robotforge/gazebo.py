"""Gazebo adapter with explicit capabilities rather than robot-name dispatch."""
from dataclasses import dataclass
from pathlib import Path
import math
import xml.etree.ElementTree as ET

from .description import RobotDescription
from .model import add
from .registry import ValidationError


@dataclass(frozen=True)
class DifferentialDrive:
    left_joints: tuple
    right_joints: tuple
    wheel_radius: float
    wheel_separation: float

    def validate(self, model):
        known = {joint.get("name") for joint in model.findall("joint")}
        assigned = self.left_joints + self.right_joints
        if not self.left_joints or not self.right_joints or len(set(assigned)) != len(assigned):
            raise ValidationError("Drive needs distinct left and right wheel joints")
        if not set(assigned) <= known:
            raise ValidationError("Drive references unknown wheel joints")
        for value in (self.wheel_radius, self.wheel_separation):
            if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
                raise ValidationError("Drive dimensions must be finite positive SI values")


def simulation_world(description, drive, package_paths=None, spawn_height=0.01):
    """Preserve converted SDF, resolve local mesh assets and add drive/world systems.

    Does not infer a drive type from topology. Callers supply robot-specific wheel
    dimensions and joint assignments. Package assets must exist before simulation.
    """
    if type(spawn_height) not in (int, float) or not math.isfinite(spawn_height):
        raise ValidationError("Spawn height must be finite")
    converted = RobotDescription("sdf", description.export("sdf"), description.source)
    _, model = converted.root_and_model()
    drive.validate(model)
    for uri in model.findall(".//uri"):
        if (uri.text or "").startswith(("package://", "model://")):
            package, separator, relative = uri.text.split("://", 1)[1].partition("/")
            if not separator or package not in (package_paths or {}):
                raise ValidationError(f"Missing package path for {uri.text}")
            base = Path(package_paths[package]).resolve()
            asset = (base / relative).resolve()
            if not asset.is_relative_to(base) or not asset.is_file():
                raise ValidationError(f"Missing or invalid mesh asset: {uri.text}")
            uri.text = asset.as_uri()
    for plugin in model.findall("plugin"):
        if "DiffDrive" in plugin.get("name", ""):
            raise ValidationError("Model already has a drive plugin; remove it or use its native world")
    pose = model.find("pose")
    if pose is None:
        pose = add(model, "pose", "0 0 0 0 0 0")
    if pose.get("relative_to"):
        raise ValidationError("Spawn pose with relative_to needs explicit frame resolution")
    values = (pose.text or "0 0 0 0 0 0").split()
    if len(values) != 6:
        raise ValidationError("Spawn pose must use six Euler components")
    values[2] = str(float(values[2]) + spawn_height)
    pose.text = " ".join(values)
    plugin = add(model, "plugin", filename="gz-sim-diff-drive-system", name="gz::sim::systems::DiffDrive")
    for side, names in (("left", drive.left_joints), ("right", drive.right_joints)):
        for name in names:
            add(plugin, side + "_joint", name)
    for key, value in {"wheel_radius": drive.wheel_radius, "wheel_separation": drive.wheel_separation,
                       "topic": f"/model/{model.get('name')}/cmd_vel", "odom_topic": f"/model/{model.get('name')}/odometry",
                       "odom_publish_frequency": 30}.items():
        add(plugin, key, value)
    root = ET.Element("sdf", version="1.9")
    world = add(root, "world", name="robotforge")
    physics = add(world, "physics", name="default", type="ignored")
    add(physics, "max_step_size", 0.001)
    for system, name in (("physics", "Physics"), ("user-commands", "UserCommands"), ("scene-broadcaster", "SceneBroadcaster")):
        add(world, "plugin", filename=f"gz-sim-{system}-system", name=f"gz::sim::systems::{name}")
    ground = add(world, "model", name="ground")
    add(ground, "static", "true")
    link = add(ground, "link", name="ground_link")
    for kind in ("visual", "collision"):
        plane = add(add(add(link, kind, name=kind), "geometry"), "plane")
        add(plane, "normal", "0 0 1")
        add(plane, "size", "100 100")
    world.append(model)
    ET.indent(root)
    return ET.tostring(root, encoding="unicode") + "\n"

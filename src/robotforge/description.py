"""Shared robot description interface; original standard XML remains authoritative.

Schema v1 indexes links, joints and capability XML without flattening away frames,
plugins, transmissions, ros2_control or simulator-specific physical properties.
Structural validation is deliberately distinct from simulation verification.
"""
from dataclasses import dataclass
from pathlib import Path
import json
import shutil
import subprocess
import xml.etree.ElementTree as ET

from .registry import ValidationError


@dataclass(frozen=True)
class RobotDescription:
    format: str
    xml: str
    source: str

    def root_and_model(self):
        try:
            root = ET.fromstring(self.xml)
        except ET.ParseError as error:
            raise ValidationError(f"Invalid XML: {error}") from error
        if self.format == "urdf" and root.tag == "robot":
            return root, root
        if self.format == "sdf" and root.tag == "sdf":
            models = root.findall("model") + root.findall("world/model")
            if len(models) == 1:
                return root, models[0]
            raise ValidationError("Import requires exactly one SDF model; split multi-model worlds first")
        raise ValidationError("Expected a URDF robot or SDF model")

    def validate(self):
        _, model = self.root_and_model()
        if not model.get("name", "").strip():
            raise ValidationError("Robot name is required")
        if any(item.tag.startswith("{http://ros.org/wiki/xacro}") for item in model.iter()) or "${" in ET.tostring(model, encoding="unicode") or "$(" in ET.tostring(model, encoding="unicode"):
            raise ValidationError("Unexpanded Xacro; import with --format xacro")
        groups = {}
        for kind in ("link", "joint"):
            names = [item.get("name", "") for item in model.findall(kind)]
            if any(not name.strip() for name in names) or len(set(names)) != len(names):
                raise ValidationError(f"Missing or duplicate {kind} name")
            groups[kind] = set(names)
        if not groups["link"]:
            raise ValidationError("At least one link is required")
        parents = {}
        for joint in model.findall("joint"):
            refs = []
            for role in ("parent", "child"):
                element = joint.find(role)
                name = (element.get("link") if self.format == "urdf" else element.text) if element is not None else None
                if name not in groups["link"] and not (self.format == "sdf" and role == "parent" and name == "world"):
                    raise ValidationError(f"Joint {joint.get('name')} has unknown {role}: {name}")
                refs.append(name)
            if self.format == "urdf":
                parent, child = refs
                if child in parents:
                    raise ValidationError(f"Multiple parent joints for {child}")
                parents[child] = parent
        if self.format == "urdf":
            if len(groups["link"] - parents.keys()) != 1:
                raise ValidationError("URDF must have exactly one root link")
            for link in groups["link"]:
                visited = set()
                while link in parents:
                    if link in visited:
                        raise ValidationError("URDF joint graph contains a cycle")
                    visited.add(link)
                    link = parents[link]
        return self

    def manifest(self):
        self.validate()
        _, model = self.root_and_model()
        def encoded(elements):
            return [dict(name=item.get("name"), type=item.get("type"), xml=ET.tostring(item, encoding="unicode")) for item in elements]
        return {
            "schema_version": 1, "name": model.get("name"),
            "source": self.source, "format": self.format,
            "links": encoded(model.findall("link")),
            "joints": encoded(model.findall("joint")),
            "sensors": encoded(model.findall(".//sensor")),
            "actuators": encoded(model.findall(".//actuator")),
            "controllers": encoded(model.findall("plugin") + model.findall("ros2_control") + model.findall("gazebo/plugin")),
            "description_xml": self.xml,
        }

    def export(self, format):
        self.validate()
        if format == self.format:
            return self.xml
        if self.format == "urdf" and format == "sdf":
            import tempfile
            with tempfile.TemporaryDirectory(prefix="robotforge-") as directory:
                path = Path(directory) / "robot.urdf"
                path.write_text(self.xml, encoding="utf-8")
                result = run_tool(["gz", "sdf", "-p", str(path)])
                converted = RobotDescription("sdf", result, self.source).validate()
                return converted.xml
        raise ValidationError(f"Unsupported conversion: {self.format} to {format}")


def run_tool(command):
    if not shutil.which(command[0]):
        raise ValidationError(f"Required tool not installed: {command[0]}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired as error:
        raise ValidationError(f"{command[0]} timed out") from error
    if result.returncode:
        raise ValidationError(f"{command[0]} failed: {result.stderr.strip()}")
    return result.stdout


def import_description(path, format=None):
    path = Path(path).resolve()
    format = format or path.suffix.lstrip(".")
    if format == "json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "description_xml" in data:
            if data.get("schema_version") != 1 or not isinstance(data["description_xml"], str):
                raise ValidationError("Unsupported robot description schema")
            return RobotDescription(data.get("format"), data["description_xml"], data.get("source", str(path))).validate()
        from .registry import validate
        from .model import urdf
        return RobotDescription("urdf", urdf(validate(data)), str(path)).validate()
    if format == "xacro":
        xml = run_tool(["xacro", str(path)])
        format = "urdf"
    elif format in ("urdf", "sdf"):
        xml = path.read_text(encoding="utf-8")
    else:
        raise ValidationError("Supported inputs: manifest JSON, URDF, Xacro, SDF")
    return RobotDescription(format, xml, str(path)).validate()

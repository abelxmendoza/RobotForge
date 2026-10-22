"""Validate version 1 hardware manifests without inventing missing specifications."""
import json
from pathlib import Path

class ValidationError(ValueError):
    pass

def validate(data):
    errors = []
    if not isinstance(data, dict):
        raise ValidationError("manifest must be an object")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        errors.append("schema_version must be 1")
    for key in ("id", "name", "revision"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key} must be a nonempty string")
    components = data.get("components")
    if not isinstance(components, list):
        errors.append("components must be an array")
        components = []
    ids = set()
    for i, component in enumerate(components):
        prefix = f"components[{i}]"
        if not isinstance(component, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("id", "name", "revision", "kind"):
            value = component.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{key} must be a nonempty string")
        identifier = component.get("id")
        if isinstance(identifier, str):
            if identifier in ids:
                errors.append(f"duplicate component id: {identifier}")
            ids.add(identifier)
        if component.get("status") not in ("confirmed", "unconfirmed"):
            errors.append(f"{prefix}.status must be confirmed or unconfirmed")
        if not isinstance(component.get("specifications"), dict):
            errors.append(f"{prefix}.specifications must be an object")
    if errors:
        raise ValidationError("; ".join(errors))
    return data

def load(path):
    return validate(json.loads(Path(path).read_text(encoding="utf-8")))

def simulation_gaps(data):
    """No physical model is ready until geometry and drive data are documented."""
    validate(data)
    required = ("mass_kg", "chassis_dimensions_m", "wheel_radius_m", "wheel_separation_m", "inertia_kg_m2", "drive_configuration")
    specs = data.get("simulation", {})
    if not isinstance(specs, dict):
        return ["simulation must be an object"]
    return [key for key in required if specs.get(key) is None]

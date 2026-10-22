"""Generate primitive two-wheel and four-wheel differential rover models."""
import math
import re
import xml.etree.ElementTree as E
from .registry import validate, ValidationError

FIELDS = ("chassis_mass_kg", "chassis_dimensions_m", "wheel_radius_m", "wheel_width_m", "wheel_separation_m", "wheel_mass_kg", "caster_radius_m")

def ready(data):
    validate(data)
    s = data.get("simulation")
    if not isinstance(s, dict):
        raise ValidationError("simulation must be an object")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", data["id"]):
        raise ValidationError("model id must use lowercase letters, digits and underscores")
    if s.get("drive_configuration") not in ("differential_2wheel", "skid_steer_4wheel"):
        raise ValidationError("unsupported drive configuration; mecanum requires a separate model")
    if s.get("provenance") not in ("synthetic_fixture", "measured"):
        raise ValidationError("simulation.provenance must be synthetic_fixture or measured")
    if not isinstance(s.get("source"), str) or not s["source"].strip():
        raise ValidationError("simulation.source must document measurements or fixture origin")
    four = s["drive_configuration"] == "skid_steer_4wheel"
    fields = FIELDS[:-1] + ("wheelbase_m",) if four else FIELDS + ("caster_mass_kg",)
    for key in fields:
        values = s.get(key)
        if key == "chassis_dimensions_m":
            if not isinstance(values, list) or len(values) != 3:
                raise ValidationError(f"{key} requires [length, width, height] in metres")
        else:
            values = [values]
        if any(type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in values):
            raise ValidationError(f"{key} requires finite positive SI values")
    length, width, height = s["chassis_dimensions_m"]
    if s["wheel_separation_m"] <= width + s["wheel_width_m"]:
        raise ValidationError("wheel separation must clear the chassis")
    if s["wheel_radius_m"] <= height / 2:
        raise ValidationError("wheel radius must provide chassis ground clearance")
    if four and s["wheelbase_m"] <= 2 * s["wheel_radius_m"]:
        raise ValidationError("wheelbase must prevent front/rear wheel overlap")
    if not four and s["caster_radius_m"] >= s["wheel_radius_m"]:
        raise ValidationError("caster must be smaller than drive wheels")
    return s

def add(parent, tag, text=None, **attrs):
    child = E.SubElement(parent, tag, attrs)
    if text is not None:
        child.text = str(text)
    return child

def world(data):
    s = ready(data)
    root = E.Element("sdf", version="1.9")
    w = add(root, "world", name="robotforge")
    physics = add(w, "physics", name="default", type="ignored")
    add(physics, "max_step_size", 0.001)
    add(physics, "real_time_factor", 1)
    for filename, name in (("physics", "Physics"), ("user-commands", "UserCommands"), ("scene-broadcaster", "SceneBroadcaster")):
        add(w, "plugin", filename=f"gz-sim-{filename}-system", name=f"gz::sim::systems::{name}")
    ground = add(w, "model", name="ground")
    add(ground, "static", "true")
    gl = add(ground, "link", name="ground_link")
    for kind in ("collision", "visual"):
        plane = add(add(add(gl, kind, name=kind), "geometry"), "plane")
        add(plane, "normal", "0 0 1")
        add(plane, "size", "100 100")
    model = add(w, "model", name=data["id"])
    radius = s["wheel_radius_m"]
    add(model, "pose", f"0 0 {radius + 0.01} 0 0 0")
    length, width, height = s["chassis_dimensions_m"]
    def link(name, mass, shape, dims, pose, inertia):
        el = add(model, "link", name=name)
        add(el, "pose", pose)
        inertial = add(el, "inertial")
        add(inertial, "mass", mass)
        tensor = add(inertial, "inertia")
        for key, value in zip(("ixx", "iyy", "izz"), inertia):
            add(tensor, key, value)
        for key in ("ixy", "ixz", "iyz"):
            add(tensor, key, 0)
        for kind in ("collision", "visual"):
            item = add(el, kind, name=kind)
            geometry = add(add(item, "geometry"), shape)
            for key, value in dims.items():
                add(geometry, key, value)
            if name == "caster" and kind == "collision":
                ode = add(add(add(item, "surface"), "friction"), "ode")
                add(ode, "mu", 0)
                add(ode, "mu2", 0)
        return el
    mass = s["chassis_mass_kg"]
    link("base_link", mass, "box", {"size": f"{length} {width} {height}"}, "0 0 0 0 0 0", (mass*(width**2+height**2)/12, mass*(length**2+height**2)/12, mass*(length**2+width**2)/12))
    wm, ww = s["wheel_mass_kg"], s["wheel_width_m"]
    four = s["drive_configuration"] == "skid_steer_4wheel"
    wheel_joints = {"left": [], "right": []}
    stations = (("front", s["wheelbase_m"]/2), ("rear", -s["wheelbase_m"]/2)) if four else (("", 0),)
    for side, sign in (("left", 1), ("right", -1)):
        for station, x in stations:
            stem = side + ("_" + station if station else "")
            wheel = link(stem+"_wheel", wm, "cylinder", {"radius":radius,"length":ww}, f"{x} {sign*s['wheel_separation_m']/2} 0 {math.pi/2} 0 0", (wm*(3*radius**2+ww**2)/12, wm*(3*radius**2+ww**2)/12, wm*radius**2/2))
            joint = add(model, "joint", name=stem+"_joint", type="revolute")
            add(joint, "parent", "base_link")
            add(joint, "child", stem+"_wheel")
            axis = add(joint, "axis")
            add(axis, "xyz", "0 1 0", expressed_in="__model__")
            wheel_joints[side].append(stem+"_joint")
    if not four:
        cr = s["caster_radius_m"]
        # Caster mass is explicit in the fixture/model specification.
        cm = s.get("caster_mass_kg")
        if type(cm) not in (int,float) or not math.isfinite(cm) or cm <= 0:
            raise ValidationError("caster_mass_kg requires a finite positive value")
        link("caster", cm, "sphere", {"radius":cr}, f"{-length/2} 0 {cr-radius} 0 0 0", (2*cm*cr**2/5,)*3)
        joint = add(model, "joint", name="caster_joint", type="fixed")
        add(joint, "parent", "base_link")
        add(joint, "child", "caster")
    plugin = add(model, "plugin", filename="gz-sim-diff-drive-system", name="gz::sim::systems::DiffDrive")
    for side, joints in wheel_joints.items():
        for name in joints:
            add(plugin, side+"_joint", name)
    for key, value in {"wheel_separation":s["wheel_separation_m"], "wheel_radius":radius,"topic":f"/model/{data['id']}/cmd_vel","odom_topic":f"/model/{data['id']}/odometry", "odom_publish_frequency":30}.items():
        add(plugin, key, value)
    E.indent(root)
    return E.tostring(root, encoding="unicode") + "\n"

def urdf(data):
    """Export the same primitive links as a URDF tree (no simulator plugins)."""
    model = E.fromstring(world(data)).find('world/model[@name="' + data['id'] + '"]')
    robot = E.Element('robot', name=data['id'])
    poses = {}
    for source in model.findall('link'):
        name = source.get('name')
        poses[name] = source.findtext('pose').split()
        target = add(robot, 'link', name=name)
        inertial = add(target, 'inertial')
        add(inertial, 'mass', value=source.findtext('inertial/mass'))
        tensor = source.find('inertial/inertia')
        add(inertial, 'inertia', **{child.tag:child.text for child in tensor})
        for kind in ('collision', 'visual'):
            item = add(target, kind)
            geometry = add(item, 'geometry')
            primitive = source.find(kind+'/geometry')[0]
            add(geometry, primitive.tag, **{child.tag:child.text for child in primitive})
    for source in model.findall('joint'):
        child = source.findtext('child')
        joint = add(robot, 'joint', name=source.get('name'), type='continuous' if source.get('type') == 'revolute' else 'fixed')
        add(joint, 'parent', link=source.findtext('parent'))
        add(joint, 'child', link=child)
        pose = poses[child]
        add(joint, 'origin', xyz=' '.join(pose[:3]), rpy=' '.join(pose[3:]))
        if source.get('type') == 'revolute':
            add(joint, 'axis', xyz='0 0 -1')
    E.indent(robot)
    return E.tostring(robot, encoding='unicode')+'\n'

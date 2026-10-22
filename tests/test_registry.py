import copy
import json
from pathlib import Path
import pytest
from robotforge.registry import validate, load, simulation_gaps, ValidationError
from robotforge.cli import main

MANIFEST = Path(__file__).resolve().parents[1] / "robots/omega1/robot.json"

def test_inventory_loads():
    assert load(MANIFEST)["id"] == "omega1"

@pytest.mark.parametrize("value", [None, [], "robot", 1])
def test_rejects_non_object(value):
    with pytest.raises(ValidationError):
        validate(value)

@pytest.mark.parametrize("version", [None, 2, True, "1"])
def test_rejects_unsupported_version(version):
    data = load(MANIFEST)
    data["schema_version"] = version
    with pytest.raises(ValidationError):
        validate(data)

def test_duplicate_component_rejected():
    data = load(MANIFEST)
    data["components"].append(copy.deepcopy(data["components"][0]))
    with pytest.raises(ValidationError, match="duplicate"):
        validate(data)

def test_bad_component_rejected():
    data = load(MANIFEST)
    data["components"] = [None, {"id": []}]
    with pytest.raises(ValidationError):
        validate(data)

def test_unknown_geometry_is_reported():
    assert "wheel_radius_m" in simulation_gaps(load(MANIFEST))

def test_cli_validate(capsys):
    assert main(["validate", str(MANIFEST)]) == 0
    assert "Valid manifest" in capsys.readouterr().out

def test_cli_gaps():
    assert main(["simulation-gaps", str(MANIFEST)]) == 1

def test_cli_bad_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{")
    assert main(["validate", str(path)]) == 2

def test_cli_missing_file(tmp_path):
    assert main(["validate", str(tmp_path / "absent")]) == 2

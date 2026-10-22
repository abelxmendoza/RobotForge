import copy
from pathlib import Path
import xml.etree.ElementTree as E
import pytest
from robotforge.registry import load, ValidationError
from robotforge.model import world

ROOT = Path(__file__).resolve().parents[1]

def fixture():
    return load(ROOT / 'robots/reference/robot.json')

def test_generated_model_has_drive_and_connected_links():
    model = E.fromstring(world(fixture())).find('world/model[@name="reference_rover"]')
    links = {link.get('name') for link in model.findall('link')}
    assert links == {'base_link', 'left_wheel', 'right_wheel', 'caster'}
    for joint in model.findall('joint'):
        assert joint.findtext('parent') in links
        assert joint.findtext('child') in links
    assert model.find('plugin').findtext('wheel_radius') == '0.08'

def test_omega1_cannot_generate_unmeasured_model():
    with pytest.raises(ValidationError):
        world(load(ROOT / 'robots/omega1/robot.json'))

@pytest.mark.parametrize('value', [None, True, -1, 0, float('nan'), float('inf'), '0.1'])
def test_invalid_physical_values_rejected(value):
    data = fixture()
    data['simulation']['wheel_radius_m'] = value
    with pytest.raises(ValidationError):
        world(data)

@pytest.mark.parametrize('field,value', [('chassis_dimensions_m',[1,2]), ('wheel_separation_m',0.1), ('drive_configuration','unknown'), ('source',''), ('provenance','guessed'), ('caster_mass_kg',None)])
def test_invalid_geometry_and_provenance_rejected(field, value):
    data = fixture()
    data['simulation'][field] = value
    with pytest.raises(ValidationError):
        world(data)

def test_urdf_tree_has_correct_wheel_axes_and_geometry():
    from robotforge.model import urdf
    robot = E.fromstring(urdf(fixture()))
    assert robot.tag == 'robot'
    assert len(robot.findall('joint')) == 3
    assert robot.find('link[@name="base_link"]/collision/geometry/box').get('size') == '0.4 0.2 0.1'
    assert robot.find('joint[@name="left_joint"]/axis').get('xyz') == '0 0 -1'
    assert robot.find('link[@name="left_wheel"]/inertial/mass').get('value') == '0.15'

def test_simulation_readiness_matches_generator():
    from robotforge.registry import simulation_gaps
    assert simulation_gaps(fixture()) == []
    data = fixture()
    data['simulation']['wheel_radius_m'] = -1
    assert simulation_gaps(data)

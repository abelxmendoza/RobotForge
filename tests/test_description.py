from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
from robotforge.description import RobotDescription, import_description
from robotforge.registry import ValidationError
from robotforge.gazebo import DifferentialDrive

ROBOT = '''<robot name="arm"><link name="base"/><link name="tip"/>
<joint name="elbow" type="continuous"><parent link="base"/><child link="tip"/>
<axis xyz="0 0 1"/></joint><ros2_control name="arm_control" type="system">
<hardware><plugin>vendor/Arm</plugin></hardware></ros2_control>
<gazebo reference="tip"><sensor name="camera" type="camera"/></gazebo></robot>'''


def test_preserves_articulated_capabilities_and_roundtrips():
    model = RobotDescription('urdf', ROBOT, 'fixture').validate()
    data = model.manifest()
    assert len(data['links']) == 2
    assert data['sensors'][0]['name'] == 'camera'
    assert data['controllers'][0]['name'] == 'arm_control'
    assert model.export('urdf') == ROBOT
    assert 'vendor/Arm' in data['description_xml']


@pytest.mark.parametrize('xml', [
    '<robot name="x"/>',
    '<robot name="x"><link name="a"/><link name="a"/></robot>',
    ROBOT.replace('link="tip"', 'link="missing"'),
    ROBOT.replace('<link name="tip"/>', '<link name="tip"/><link name="isolated"/>'),
    '<robot name="x"><link name="a"/><joint name="j" type="fixed"><parent link="a"/><child link="a"/></joint></robot>',
    '<robot>',
])
def test_invalid_descriptions_fail(xml):
    with pytest.raises(ValidationError):
        RobotDescription('urdf', xml, 'fixture').validate()


def test_sdf_preserves_frames_and_sensor_physics():
    xml = '<sdf version="1.9"><model name="drone"><link name="body"><sensor name="imu" type="imu"/></link><frame name="rotor" attached_to="body"/></model></sdf>'
    model = RobotDescription('sdf', xml, 'fixture').validate()
    assert model.manifest()['sensors'][0]['type'] == 'imu'
    assert model.export('sdf') == xml
    with pytest.raises(ValidationError, match='Unsupported conversion'):
        model.export('urdf')


def test_multi_model_world_requires_selection():
    with pytest.raises(ValidationError, match='exactly one'):
        RobotDescription('sdf', '<sdf><world><model name="a"/><model name="b"/></world></sdf>', 'fixture').validate()


def test_xacro_is_expanded_and_comments_do_not_trigger_false_positives(tmp_path):
    pytest.importorskip('xacro')
    import shutil
    if not shutil.which('xacro'):
        pytest.skip('xacro executable not on PATH')
    path = tmp_path / 'robot.urdf'
    path.write_text('<robot xmlns:xacro="http://ros.org/wiki/xacro" name="x"><!-- $(find example) --><xacro:property name="base" value="body"/><link name="${base}"/></robot>')
    with pytest.raises(ValidationError, match='Unexpanded'):
        import_description(path)
    assert import_description(path, 'xacro').manifest()['links'][0]['name'] == 'body'


@pytest.mark.parametrize('filename', ['omega1/prototype.json', 'reference/robot.json'])
def test_legacy_manifests_use_common_interface(filename):
    model = import_description(Path(__file__).resolve().parents[1] / 'robots' / filename)
    assert model.manifest()['links']
    assert model.manifest()['joints']


def test_drive_rejects_unknown_and_duplicate_assignments():
    _, model = RobotDescription('urdf', ROBOT, 'fixture').root_and_model()
    for drive in (DifferentialDrive(('elbow',), ('missing',), .1, .2),
                  DifferentialDrive(('elbow',), ('elbow',), .1, .2)):
        with pytest.raises(ValidationError):
            drive.validate(model)


def test_interchange_json_reimports(tmp_path):
    import json
    path = tmp_path / 'model.json'
    path.write_text(json.dumps(RobotDescription('urdf', ROBOT, 'fixture').manifest()))
    assert import_description(path).export('urdf') == ROBOT


def test_gazebo_adapter_preserves_model_and_validates_assets(monkeypatch, tmp_path):
    from robotforge.gazebo import simulation_world
    xml = '<sdf version="1.9"><model name="rover"><link name="base"/><link name="left"/><link name="right"/><joint name="l" type="revolute"><parent>base</parent><child>left</child></joint><joint name="r" type="revolute"><parent>base</parent><child>right</child></joint></model></sdf>'
    model = RobotDescription('sdf', xml, 'fixture')
    drive = DifferentialDrive(('l',), ('r',), .03, .16)
    world = ET.fromstring(simulation_world(model, drive))
    assert len(world.findall('world/model[@name="rover"]/link')) == 3
    assert world.findtext('world/model[@name="rover"]/plugin/left_joint') == 'l'
    bad = xml.replace('<link name="base"/>', '<link name="base"><visual name="v"><geometry><mesh><uri>package://missing/a.stl</uri></mesh></geometry></visual></link>')
    with pytest.raises(ValidationError, match='Missing package'):
        simulation_world(RobotDescription('sdf', bad, 'fixture'), drive)

"""Reproduce the first two-robot import/export/motion experiment on Ubuntu."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

from robotforge.description import import_description, run_tool
from robotforge.gazebo import DifferentialDrive, simulation_world


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--turtlebot3-description', type=Path, required=True, help='Official turtlebot3_description package directory')
    parser.add_argument('--output', type=Path, default=Path('work/compatibility'))
    parser.add_argument('--motion', action='store_true', help='Launch bounded headless Gazebo forward and turn tests')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    args.output.mkdir(parents=True, exist_ok=True)
    package = args.turtlebot3_description.resolve()
    cases = [
        ('omega1_prototype', root / 'robots/omega1/prototype.json', None,
         DifferentialDrive(('left_front_joint', 'left_rear_joint'), ('right_front_joint', 'right_rear_joint'), .0325, .125), .0425,
         'Provisional synthetic fixture; not measured Omega1'),
        ('turtlebot3_burger', package / 'urdf/turtlebot3_burger.urdf', 'xacro',
         DifferentialDrive(('wheel_left_joint',), ('wheel_right_joint',), .033, .160), .01,
         'ROBOTIS Burger URDF; radius and separation from wheel collision geometry and joint origins'),
    ]
    report = {'schema_version': 1, 'generated_at': datetime.now(timezone.utc).isoformat(), 'scope': 'Structural compatibility and wheel-derived odometry; no physical calibration or ROS bridge certification', 'robots': []}
    for name, source, format, drive, height, provenance in cases:
        entry = {'robot': name, 'source': str(source), 'provenance': provenance, 'checks': [], 'status': 'failed'}
        report['robots'].append(entry)
        try:
            description = import_description(source, format)
            (args.output / f'{name}.json').write_text(json.dumps(description.manifest(), indent=2) + '\n')
            entry['checks'].append({'name': 'import_and_structure', 'status': 'passed'})
            sdf = args.output / f'{name}.sdf'
            sdf.write_text(simulation_world(description, drive, {'turtlebot3_description': package}, height))
            output = run_tool(['gz', 'sdf', '-k', str(sdf)])
            entry['checks'].append({'name': 'gazebo_sdf_validation', 'status': 'passed', 'output': output.strip()})
            for mode in ('forward', 'turn'):
                if not args.motion:
                    entry['checks'].append({'name': mode, 'status': 'not_run'})
                    continue
                command = [sys.executable, str(root / 'scripts/smoke_gazebo.py'), '--sdf', str(sdf.resolve()), '--model-name', name]
                if mode == 'turn':
                    command.append('--turn')
                result = subprocess.run(command, capture_output=True, text=True, timeout=90, env=os.environ.copy())
                check = {'name': mode, 'status': 'passed' if result.returncode == 0 else 'failed'}
                if result.returncode == 0:
                    check['evidence'] = json.loads(result.stdout)
                else:
                    check['error'] = result.stderr or result.stdout
                entry['checks'].append(check)
            entry['status'] = 'failed' if any(check['status'] == 'failed' for check in entry['checks']) else ('passed' if args.motion else 'partial')
        except (ValueError, OSError, subprocess.TimeoutExpired) as error:
            entry['error'] = str(error)
    report_path = args.output / 'report.json'
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(report_path.resolve())
    return 1 if any(entry['status'] == 'failed' for entry in report['robots']) else 0


if __name__ == '__main__':
    raise SystemExit(main())

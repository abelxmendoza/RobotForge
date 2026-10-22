"""Bounded, isolated native Gazebo motion acceptance test; no ROS bridge required."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import uuid
from robotforge.registry import load
from robotforge.model import world


def main():
    root = Path(__file__).resolve().parents[1]
    data = load(root / 'robots/reference/robot.json')
    env = dict(os.environ, GZ_PARTITION='robotforge_' + uuid.uuid4().hex)
    with tempfile.TemporaryDirectory(prefix='robotforge-') as directory:
        path = Path(directory) / 'world.sdf'
        path.write_text(world(data))
        with (Path(directory) / 'server.log').open('w+') as log:
            server = subprocess.Popen(['gz', 'sim', '-s', '-r', str(path)], env=env, stdout=log, stderr=log)
            try:
                topic = '/model/reference_rover/'
                deadline = time.monotonic() + 20
                while time.monotonic() < deadline:
                    if server.poll() is not None:
                        log.seek(0)
                        raise RuntimeError(log.read())
                    topics = subprocess.run(['gz', 'topic', '-l'], env=env, capture_output=True, text=True, timeout=5)
                    if topic + 'odometry' in topics.stdout:
                        break
                    time.sleep(0.2)
                else:
                    raise RuntimeError('Gazebo odometry did not become ready within 20s')
                reader = subprocess.Popen(['gz', 'topic', '-e', '-t', topic+'odometry'], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                try:
                    subprocess.run(['gz', 'topic', '-t', topic+'cmd_vel', '-m', 'gz.msgs.Twist', '-p', 'linear: {x: 0.2}'], env=env, check=True, timeout=5, capture_output=True)
                    try:
                        output, _ = reader.communicate(timeout=4)
                    except subprocess.TimeoutExpired:
                        reader.terminate()
                        output, _ = reader.communicate(timeout=5)
                finally:
                    if reader.poll() is None:
                        reader.kill()
                        reader.wait()
                positions = [float(x) for x in re.findall(r'position\s*\{\s*x:\s*([-+\d.eE]+)', output)]
                displacement = positions[-1] - positions[0] if len(positions) > 1 else 0
                if displacement < 0.1:
                    raise RuntimeError(f'Insufficient odometry displacement: {displacement} m')
                print(json.dumps({'fixture':data['id'], 'odometry_samples':len(positions), 'displacement_m':displacement, 'passed':True}))
            finally:
                server.terminate()
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait()

if __name__ == '__main__':
    main()

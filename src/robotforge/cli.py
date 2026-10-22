import argparse
import json
import sys
from .registry import load, simulation_gaps, ValidationError

def main(argv=None):
    parser = argparse.ArgumentParser(description="RobotForge hardware manifest tools")
    parser.add_argument("command", choices=["validate", "simulation-gaps", "generate-sdf", "generate-urdf"])
    parser.add_argument("manifest")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        data = load(args.manifest)
        if args.command == "validate":
            print(f"Valid manifest: {data['id']} revision {data['revision']}")
            return 0
        if args.command in ("generate-sdf", "generate-urdf"):
            from .model import world, urdf
            from pathlib import Path
            result = world(data) if args.command == "generate-sdf" else urdf(data)
            if args.output:
                Path(args.output).write_text(result, encoding="utf-8")
            else:
                print(result, end="")
            return 0
        gaps = simulation_gaps(data)
        print(json.dumps({"missing_specifications": gaps}, indent=2))
        return 1 if gaps else 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())

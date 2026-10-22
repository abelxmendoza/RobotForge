import argparse
import json
import sys
from .registry import load, simulation_gaps, ValidationError

def main(argv=None):
    parser = argparse.ArgumentParser(description="RobotForge hardware manifest tools")
    parser.add_argument("command", choices=["validate", "simulation-gaps"])
    parser.add_argument("manifest")
    args = parser.parse_args(argv)
    try:
        data = load(args.manifest)
        if args.command == "validate":
            print(f"Valid manifest: {data['id']} revision {data['revision']}")
            return 0
        gaps = simulation_gaps(data)
        print(json.dumps({"missing_specifications": gaps}, indent=2))
        return 1 if gaps else 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())

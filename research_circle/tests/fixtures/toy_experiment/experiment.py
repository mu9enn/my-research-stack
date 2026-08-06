#!/usr/bin/env python3
import argparse
import json
import math
import sys
import time
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
parser.add_argument("--effect", type=float, default=0.2)
parser.add_argument("--sleep", type=float, default=0.0)
parser.add_argument("--fail", action="store_true")
parser.add_argument("--invalid", action="store_true")
args = parser.parse_args()

print("toy experiment started")
time.sleep(args.sleep)
if args.fail:
    print("intentional fixture failure", file=sys.stderr)
    raise SystemExit(7)

output = Path(args.output)
output.parent.mkdir(parents=True, exist_ok=True)
score = float("nan") if args.invalid else 0.5 + args.effect
output.write_text(json.dumps({"score": score}) + "\n", encoding="utf-8")
print("toy experiment finished")

"""Re-run the local research validation and retain exact command outputs."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "hardening-artifacts"
PYTHON = sys.executable
jobs = [
    ("full-suite", ROOT, ["-m", "pytest", "-q", "-ra"]),
    ("ai-ml-suite", ROOT, ["-m", "pytest", "-q", "ai-ml"]),
    ("cyber-suite", ROOT, ["-m", "pytest", "-q", "cybersec/pramana"]),
    ("regressions", ROOT, ["-m", "pytest", "-q", "ai-ml/tests"]),
    ("fusion-demo", ROOT / "ai-ml", ["-m", "pramana.demo"]),
    ("range-sim", ROOT / "ai-ml", ["-m", "pramana.range_sim", str(OUT / "range-sim")]),
    ("evaluation", ROOT / "ai-ml", ["-m", "pramana.evaluate"]),
    ("sensitivity", ROOT / "ai-ml", ["-m", "pramana.sensitivity"]),
    ("cyber-demo", ROOT / "cybersec/pramana", ["run_cyber_demo.py", "--output-dir", str(OUT / "cyber-demo")]),
    ("real-source-validation", ROOT / "cybersec/pramana", ["run_cyber_validation.py", "--output", str(OUT / "real-source.json")]),
    ("dependencies", ROOT, ["-m", "pip", "check"]),
]
results = []
for name, cwd, args in jobs:
    proc = subprocess.run([PYTHON, *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (OUT / (name + ".txt")).write_text(proc.stdout + proc.stderr, encoding="utf-8")
    results.append({"name": name, "cwd": str(cwd), "command": [PYTHON, *args], "exit_code": proc.returncode})
    print(name, "exit", proc.returncode, flush=True)
(OUT / "runs.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

sys.exit(1 if any(r["exit_code"] for r in results) else 0)

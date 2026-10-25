"""Repeat the pilot, measure subprocess time, and record actual output.

Run: python scripts/reproduce.py
Uses Python standard library only. Does not access the network.
"""
import hashlib
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src' / 'pilot.py'
OUTPUT = ROOT / 'results' / 'pilot.json'
LOG = ROOT / 'results' / 'run.log'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    previous = digest(OUTPUT) if OUTPUT.exists() else None
    command = [sys.executable, str(SOURCE), '--shots', '200000',
               '--seed', '20261025', '--output', str(OUTPUT)]
    start_utc = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    completed = subprocess.run(command, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    current = digest(OUTPUT) if OUTPUT.exists() else '(missing)'
    match = None if previous is None else (current == previous)
    lines = [
        'QEC-R01 timed reproduction; this file documents THIS run, not earlier ones',
        'UTC start: ' + start_utc,
        'Python: ' + sys.version.split()[0],
        'Platform: ' + platform.platform(),
        'Command: python src/pilot.py --shots 200000 --seed 20261025 --output results/pilot.json',
        'Source SHA256: ' + digest(SOURCE),
        'Return code: ' + str(completed.returncode),
        'Elapsed seconds: ' + f'{elapsed:.6f}',
        'JSON SHA256: ' + current,
        'Matches previous JSON: ' + str(match),
        '=== STDOUT ===',
        completed.stdout.rstrip(),
        '=== STDERR ===',
        completed.stderr.rstrip() or '(empty)',
        ''
    ]
    LOG.write_text('\n'.join(lines), encoding='utf-8')
    print(LOG.read_text(encoding='utf-8'))
    if completed.returncode != 0 or (match is False):
        raise SystemExit('FAIL: experiment failed or JSON changed')


if __name__ == '__main__':
    main()

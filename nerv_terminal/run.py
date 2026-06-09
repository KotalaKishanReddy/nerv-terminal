"""Package entry-point — delegates entirely to root run.py."""
import sys, os
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent
    run_py = root / 'run.py'
    if not run_py.exists():
        print('run.py not found. Re-install with install.sh.')
        sys.exit(1)
    os.execv(sys.executable, [sys.executable, str(run_py)] + sys.argv[1:])

if __name__ == '__main__':
    main()

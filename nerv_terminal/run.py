"""Package entry-point — called by `nerv` console script."""
import sys, os, time
from pathlib import Path
from nerv_terminal.updater import check_and_update

HERE    = Path(__file__).resolve().parent.parent
NERV_PY = HERE / 'nerv.py'


def main():
    from nerv_terminal.updater import check_and_update
    updated = check_and_update(NERV_PY)
    if updated:
        RED   = '\033[38;2;210;25;25m'
        AMBER = '\033[38;2;255;170;0m'
        RESET = '\033[0m'
        print(f'{RED}  [ NERV ]  {AMBER}Update applied — restarting…{RESET}')
        time.sleep(0.7)
    if not NERV_PY.exists():
        print('nerv.py missing. Run install.sh to reinstall.')
        sys.exit(1)
    os.execv(sys.executable, [sys.executable, str(NERV_PY)] + sys.argv[1:])


if __name__ == '__main__':
    main()

"""Compatibility entry point: validate the newly authenticated Kimi K3 profile."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('validate_kimi_connection.py')), run_name='__main__')

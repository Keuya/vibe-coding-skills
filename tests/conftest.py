from __future__ import annotations

import os
import sys

from _python_source_roots import REPO_ROOT


PYCACHE_ROOT = REPO_ROOT / ".tmp" / "pycache"

# Keep pytest runs hermetic for repo-owned Python sources.
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("PYTHONPYCACHEPREFIX", str(PYCACHE_ROOT))
sys.dont_write_bytecode = True
sys.pycache_prefix = str(PYCACHE_ROOT)

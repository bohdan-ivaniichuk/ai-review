"""Allow: python -m library_catalog (with PYTHONPATH including `src`)."""

import sys

from library_catalog.cli import main

if __name__ == "__main__":
    raise SystemExit(main())

---
name: prefer-uv-over-pip
enabled: true
event: bash
pattern: (?:pip\s+install|python\s+-m\s+pip|pip3\s+install)
action: warn
---

**Use uv instead of pip**

You're using pip directly, but this project prefers uv for Python package management.

**Instead of:**
- `pip install package` → `uv add package`
- `pip install -r requirements.txt` → `uv pip install -r requirements.txt`
- `python -m pip install` → `uv add` or `uv pip install`

uv is 10-100x faster than pip and provides better dependency resolution.

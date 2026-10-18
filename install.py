"""Install only this skill into an explicit host or destination."""
import argparse
import os
from pathlib import Path
import shutil
import sys
NAME = 'karmen-api-diagnostics'

def install(destination):
    source = Path(__file__).resolve().parent
    destination = Path(destination).expanduser()
    resolved = destination.resolve()
    if resolved == source or source in resolved.parents:
        raise ValueError("destination cannot be inside the source package")
    if destination.exists() or destination.is_symlink():
        raise ValueError("destination exists; choose a new directory or remove your old installation yourself")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    for name in ("SKILL.md", "README.md", "LICENSE", "NOTICE.md", "CHANGELOG.md", "CONTRIBUTING.md", "SUPPORT.md", "SECURITY.md", "skill.json", "install.py", "agents", "scripts", "docs", "examples", "tests"):
        item = source / name
        if item.is_dir():
            shutil.copytree(item, destination / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(item, destination / name)
    return destination

def main():
    parser = argparse.ArgumentParser(description="Install " + NAME + " without changing host permissions.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--host", choices=("codex", "deepseek", "grok", "agents"))
    group.add_argument("--destination", help="exact new directory for this skill")
    args = parser.parse_args()
    roots = {
        "codex": Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills",
        "deepseek": Path(os.environ.get("DSH_HOME", str(Path.home() / ".dsh"))) / "skills",
        "grok": Path.home() / ".grok" / "skills",
        "agents": Path.home() / ".agents" / "skills",
    }
    try:
        destination = args.destination if args.destination else roots[args.host] / NAME
        print(install(destination))
        return 0
    except (OSError, ValueError) as exc:
        print("Error: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())

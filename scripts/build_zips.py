"""Rebuild the archives the students download, from the folders they mirror.

    python scripts/build_zips.py                      # every archive
    python scripts/build_zips.py projects/project0    # one of them

`projects/projectN/` goes to `projects/projectN.zip`, with its content at the
root of the archive and without its `README.md`, which GitHub renders anyway.
`python-tutorial/tutorial_code/` goes to `python-tutorial/tutorial_code.zip`,
with its content under `tutorial_code/`, as the tutorial expects.

The archives are written deterministically, files sorted and timestamps fixed,
so that rebuilding one without touching its folder leaves it byte for byte
identical and out of the commit.

Prints the path of every archive that was written, which the pre-commit hook
adds to the commit.
"""

import sys
import zipfile

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# folder -> (archive, prefix of the paths inside the archive)
ARCHIVES = {
    "projects/project0": ("projects/project0.zip", ""),
    "projects/project0bis": ("projects/project0bis.zip", ""),
    "projects/project1": ("projects/project1.zip", ""),
    "projects/project2": ("projects/project2.zip", ""),
    "python-tutorial/tutorial_code": ("python-tutorial/tutorial_code.zip",
                                      "tutorial_code/"),
}

SKIP_DIRS = {"__pycache__", "__MACOSX", ".venv", ".ipynb_checkpoints", ".git"}
SKIP_NAMES = {"README.md", ".DS_Store", ".gitignore"}
SKIP_SUFFIXES = {".pyc", ".pyo"}

TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def content(folder):
    """The files of `folder` that belong in its archive, sorted."""
    keep = []

    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        if set(path.parts) & SKIP_DIRS:
            continue
        if path.name in SKIP_NAMES or path.suffix in SKIP_SUFFIXES:
            continue
        keep.append(path)

    return keep


def build(folder, archive, prefix):
    """Write `archive` from `folder`, and say whether its content changed."""
    files = content(folder)
    buffer = zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED)

    with buffer as zf:
        for path in files:
            name = prefix + path.relative_to(folder).as_posix()
            info = zipfile.ZipInfo(name, date_time=TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())

    return len(files)


if __name__ == "__main__":
    wanted = [Path(arg).as_posix().rstrip("/") for arg in sys.argv[1:]]

    for folder, (archive, prefix) in ARCHIVES.items():
        if wanted and folder not in wanted:
            continue

        path, target = ROOT / folder, ROOT / archive

        if not path.is_dir():
            continue

        before = target.read_bytes() if target.exists() else None
        count = build(path, target, prefix)

        if target.read_bytes() != before:
            print(archive)
            print(f"  {count} files from {folder}", file=sys.stderr)

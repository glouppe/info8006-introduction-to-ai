"""Fetch the trajectory of the Apollo 12 third stage (S-IVB) from Earth to the Moon, for the orbit demo.

    uv run python scripts/fetch_apollo_trajectory.py

Writes `demo/lec6/apollo12.json`: the positions of the stage and of the Moon every 10 minutes, from
1969-11-14 19:40 UTC (half an hour after translunar injection) to a day after the lunar flyby, in km,
geocentric. The trajectory is the reconstruction by D. R. Adamo for NASA (2012), served by JPL
Horizons (object -399120); the Moon is Horizons' object 301. Coordinates are in a frame whose first two
axes span the plane that best fits both paths, which the demo draws; the third is out of that plane.
"""

import json
from pathlib import Path

import numpy as np
import requests

ROOT = Path(__file__).resolve().parent.parent
API = "https://ssd.jpl.nasa.gov/api/horizons.api"
START, STOP, STEP = "1969-11-14 19:40", "1969-11-19 10:00", "10m"


def vectors(target):
    params = {
        "format": "text", "COMMAND": f"'{target}'", "EPHEM_TYPE": "VECTORS", "CENTER": "'500@399'",
        "REF_PLANE": "ECLIPTIC", "START_TIME": f"'{START}'", "STOP_TIME": f"'{STOP}'", "STEP_SIZE": f"'{STEP}'",
        "VEC_TABLE": "2", "CSV_FORMAT": "YES", "OUT_UNITS": "KM-S",
    }
    text = requests.get(API, params=params, timeout=60).text
    rows = text[text.index("$$SOE") + 5:text.index("$$EOE")].strip().splitlines()
    return np.array([[float(v) for v in row.split(",")[2:8]] for row in rows])


def main():
    craft, moon = vectors(-399120), vectors(301)
    # the plane that best fits both paths, oriented so that the Moon moves counterclockwise
    points = np.vstack([craft[:, :3], moon[:, :3]])
    _, _, vt = np.linalg.svd(points, full_matrices=False)
    e1, e2 = vt[0], vt[1]
    if np.dot(np.cross(moon[0, :3], moon[0, 3:]), np.cross(e1, e2)) < 0:
        e2 = -e2
    normal = np.cross(e1, e2)
    project = lambda xs: np.stack([xs @ e1, xs @ e2, xs @ normal], axis=1)
    out = {
        "source": "JPL Horizons, Apollo 12 S-IVB (-399120), reconstruction by D. R. Adamo (2012); Moon (301)",
        "start": START + " UTC",
        "step": 600,
        "velocity": [round(float(v), 4) for v in project(craft[:1, 3:6])[0]],
        "craft": np.round(project(craft[:, :3])).astype(int).tolist(),
        "moon": np.round(project(moon[:, :3])).astype(int).tolist(),
    }
    path = ROOT / "demo" / "lec6" / "apollo12.json"
    path.write_text(json.dumps(out, separators=(",", ":")))
    distance = np.linalg.norm(craft[:, :3] - moon[:, :3], axis=1)
    print(path.relative_to(ROOT), len(out["craft"]), "points; closest to the Moon:", round(distance.min()), "km")


if __name__ == "__main__":
    main()

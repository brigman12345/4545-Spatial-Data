#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import random
from pathlib import Path
import argparse


# -----------------------------
# Threat type configuration
# -----------------------------
THREAT_TYPES = {
    "alien": {
        "speed_kmh": (800, 1600),
        "duration_min": (30, 90),
    },
    "orbital": {
        "speed_kmh": (2000, 8000),
        "duration_min": (10, 40),
    },
    "airborne": {
        "speed_kmh": (500, 1200),
        "duration_min": (30, 90),
    },
    "kaiju": {
        "speed_kmh": (30, 80),
        "duration_min": (120, 600),
    },
}


# -----------------------------
# Helpers
# -----------------------------
def random_point_around(
    lat: float, lon: float, radius_km: float
) -> tuple[float, float]:
    """
    Generate a random point roughly radius_km away from (lat, lon).
    Flat-earth approximation is fine for simulation.
    """
    r = radius_km / 111.0  # ~km per degree
    angle = random.uniform(0, 2 * math.pi)

    dlat = r * math.cos(angle)
    dlon = r * math.sin(angle) / max(math.cos(math.radians(lat)), 0.1)

    return lat + dlat, lon + dlon


def random_bearing_toward(
    origin_lat, origin_lon, target_lat, target_lon, jitter_deg=20
):
    dy = target_lat - origin_lat
    dx = target_lon - origin_lon
    bearing = math.degrees(math.atan2(dx, dy))
    bearing = (bearing + 360) % 360
    bearing += random.uniform(-jitter_deg, jitter_deg)
    return bearing % 360


# -----------------------------
# Main generator
# -----------------------------
def simulate_threats(
    base_lat: float,
    base_lon: float,
    count: int,
    radius_km: float,
    seed: int | None = None,
):
    if seed is not None:
        random.seed(seed)

    threats = []

    for i in range(count):
        threat_type = random.choice(list(THREAT_TYPES.keys()))
        cfg = THREAT_TYPES[threat_type]

        origin_lat, origin_lon = random_point_around(base_lat, base_lon, radius_km)

        bearing = random_bearing_toward(origin_lat, origin_lon, base_lat, base_lon)

        speed = random.uniform(*cfg["speed_kmh"])
        duration = random.uniform(*cfg["duration_min"])

        threats.append(
            {
                "id": f"T{i+1:03d}",
                "type": threat_type,
                "origin_lat": round(origin_lat, 6),
                "origin_lon": round(origin_lon, 6),
                "bearing_deg": round(bearing, 2),
                "speed_kmh": round(speed, 1),
                "duration_min": round(duration, 1),
            }
        )

    return threats


# -----------------------------
# CLI
# -----------------------------
def main():
    ap = argparse.ArgumentParser(description="Simulate non-human missile threats")
    ap.add_argument("--base-lat", type=float, required=True)
    ap.add_argument("--base-lon", type=float, required=True)
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--radius-km", type=float, default=3000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=Path, default=Path("threats.json"))

    args = ap.parse_args()

    threats = simulate_threats(
        base_lat=args.base_lat,
        base_lon=args.base_lon,
        count=args.count,
        radius_km=args.radius_km,
        seed=args.seed,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(threats, indent=2))

    print(f"Generated {len(threats)} threats → {args.out}")


if __name__ == "__main__":
    main()

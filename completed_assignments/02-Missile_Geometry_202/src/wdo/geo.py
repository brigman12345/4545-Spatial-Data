"""
 ____      ____  ______      ___       ______  ________    ___
|_  _|    |_  _||_   _ `.  .'   `.   .' ___  ||_   __  | .'   `.
  \ \  /\  / /    | | `. \/  .-.  \ / .'   \_|  | |_ \_|/  .-.  \
   \ \/  \/ /     | |  | || |   | | | |   ____  |  _| _ | |   | |
    \  /\  /     _| |_.' /\  `-'  /_\ `.___]  |_| |__/ |\  `-'  /
     \/  \/     |______.'  `.___.'(_)`._____.'|________| `.___.'

wdo_geo.py — World Defense Organization geometry helpers

This file is intentionally SMALL and focused (well its growing):
- distance (haversine)
- bearing
- destination point
- interpolation for visualization (simple)
- bounding box helpers
- geojson help

It is NOT a GIS replacement.
It is a learning toolkit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import radians, degrees, sin, cos, asin, atan2, sqrt
from typing import Iterable, List, Sequence, Tuple


EARTH_RADIUS_KM: float = 6371.0088  # mean Earth radius (km) — good enough for class


@dataclass(frozen=True)
class LatLon:
    lat: float
    lon: float

    def as_tuple(self) -> Tuple[float, float]:
        return (self.lat, self.lon)


def _deg_to_rad(x: float) -> float:
    return radians(x)


def _rad_to_deg(x: float) -> float:
    return degrees(x)


def normalize_bearing_deg(bearing: float) -> float:
    """
    Normalize any angle into [0, 360).
    """
    b = bearing % 360.0
    return b if b >= 0 else b + 360.0


# ----------------------------------------
# Distance: Haversine (km)
# ----------------------------------------
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Compute great-circle distance between two lat/lon points.
    Returns distance in kilometers.
    Inputs: degrees
    Output: kilometers
    """
    phi1 = radians(lat1)
    phi2 = radians(lat2)

    dphi = radians(lat2 - lat1)
    dlmb = radians(lon2 - lon1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlmb / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def initial_bearing_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Initial bearing (forward azimuth) from point 1 to point 2.

    Inputs: degrees
    Output: degrees in [0, 360)
    """
    phi1 = _deg_to_rad(lat1)
    phi2 = _deg_to_rad(lat2)
    dlambda = _deg_to_rad(lon2 - lon1)

    y = sin(dlambda) * cos(phi2)
    x = cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(dlambda)

    theta = atan2(y, x)  # radians
    return normalize_bearing_deg(_rad_to_deg(theta))


# ----------------------------------------
# Destination point (bearing + distance)
# ----------------------------------------
def destination_point(
    lat: float, lon: float, bearing_deg: float, distance_km: float
) -> LatLon:
    """
    Compute destination point given start, bearing, and distance on a sphere.

    Inputs:
      - lat, lon in degrees
      - bearing_deg in degrees
      - distance_km in kilometers
    Output:
      - LatLon (degrees)
    """
    if distance_km < 0:
        raise ValueError("distance_km must be >= 0")

    phi1 = _deg_to_rad(lat)
    lambda1 = _deg_to_rad(lon)
    theta = _deg_to_rad(normalize_bearing_deg(bearing_deg))

    delta = distance_km / EARTH_RADIUS_KM  # angular distance in radians

    sin_phi2 = sin(phi1) * cos(delta) + cos(phi1) * sin(delta) * cos(theta)
    phi2 = asin(max(-1.0, min(1.0, sin_phi2)))

    y = sin(theta) * sin(delta) * cos(phi1)
    x = cos(delta) - sin(phi1) * sin(phi2)
    lambda2 = lambda1 + atan2(y, x)

    lat2 = _rad_to_deg(phi2)
    lon2 = _rad_to_deg(lambda2)

    # Normalize lon to [-180, 180)
    lon2 = ((lon2 + 180.0) % 360.0) - 180.0

    return LatLon(lat2, lon2)


# ----------------------------------------
# Interpolate LatLons (list of points)
# ----------------------------------------
def interpolate_latlon_linear(start: LatLon, end: LatLon, n: int) -> List[LatLon]:
    """
    Simple linear interpolation in lat/lon space.
    This is NOT geodesic interpolation. It's mainly for quick visualization.
    It generates points between a start and end.

    n = number of points INCLUDING endpoints (n >= 2)
    """
    if n < 2:
        raise ValueError("n must be >= 2")

    pts: List[LatLon] = []
    for i in range(n):
        t = i / (n - 1)
        lat = start.lat + t * (end.lat - start.lat)
        lon = start.lon + t * (end.lon - start.lon)
        pts.append(LatLon(lat, lon))
    return pts


# ----------------------------------------
# Trajectory sampling (list of points)
# ----------------------------------------
def trajectory_points(
    origin_lat: float,
    origin_lon: float,
    bearing_deg: float,
    speed_kmh: float,
    duration_min: float,
    step_min: float = 2.0,
) -> List[Tuple[float, float]]:
    """
    Generate intermediate (lat, lon) points along a trajectory.
    This function uses an origin and a bearing to generate points (no set destination).
    """
    points = [(origin_lat, origin_lon)]

    steps = max(1, int(duration_min / step_min))
    for i in range(1, steps + 1):
        elapsed_hr = (i * step_min) / 60.0
        dist_km = speed_kmh * elapsed_hr
        lat2, lon2 = destination_point(origin_lat, origin_lon, bearing_deg, dist_km)
        points.append((lat2, lon2))

    return points


# ----------------------------------------
# Bounding Box
# ----------------------------------------
def bbox_latlon(points: Sequence[LatLon]) -> Tuple[float, float, float, float]:
    """
    Bounding box for a list of LatLon: (min_lat, min_lon, max_lat, max_lon)
    """
    if not points:
        raise ValueError("points must be non-empty")

    lats = [p.lat for p in points]
    lons = [p.lon for p in points]
    return (min(lats), min(lons), max(lats), max(lons))


def orientation(p: LatLon, q: LatLon, r: LatLon) -> int:
    """
    Returns orientation of the ordered triplet (p, q, r).

    Return values:
        0 -> collinear
        1 -> clockwise
        2 -> counterclockwise
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return 0
    return 1 if val > 0 else 2


def on_segment(p: LatLon, q: LatLon, r: LatLon) -> bool:
    """
    Assumes p, q, r are collinear.
    Returns True if q lies on the line segment pr.
    """
    return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[
        1
    ] <= max(p[1], r[1])


def segments_intersect(p1: LatLon, q1: LatLon, p2: LatLon, q2: LatLon) -> bool:
    """
    Returns True if line segment p1q1 intersects line segment p2q2.
    """

    # Find the 4 orientations needed for the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases: collinear points
    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False


def point_in_polygon(point: LatLon, polygon: List[LatLon]) -> bool:
    x, y = point
    inside = False
    n = len(polygon)

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        crosses = (y1 > y) != (y2 > y)
        if crosses:
            x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_intersect:
                inside = not inside

    return inside


def polygons_intersect(poly1: List[LatLon], poly2: List[LatLon]) -> bool:
    # Check edge intersections
    for i in range(len(poly1)):
        a1 = poly1[i]
        a2 = poly1[(i + 1) % len(poly1)]

        for j in range(len(poly2)):
            b1 = poly2[j]
            b2 = poly2[(j + 1) % len(poly2)]

            if segments_intersect(a1, a2, b1, b2):
                return True

    # Check containment
    if point_in_polygon(poly1[0], poly2):
        return True

    if point_in_polygon(poly2[0], poly1):
        return True

    return False


def signed_area(poly):
    """
    Compute signed area of a polygon.
    Positive -> CCW
    Negative -> CW
    """

    area = 0
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        area += x1 * y2 - x2 * y1

    return area / 2


def enforce_rhr(poly):
    """
    Ensure polygon follows the right-hand rule (CCW).
    """

    if signed_area(poly) < 0:
        poly = list(reversed(poly))

    return poly


"""
   ______  ________    ___       _____   ______     ___   ____  _____
 .' ___  ||_   __  | .'   `.    |_   _|.' ____ \  .'   `.|_   \|_   _|
/ .'   \_|  | |_ \_|/  .-.  \     | |  | (___ \_|/  .-.  \ |   \ | |
| |   ____  |  _| _ | |   | | _   | |   _.____`. | |   | | | |\ \| |
\ `.___]  |_| |__/ |\  `-'  /| |__' |  | \____) |\  `-'  /_| |_\   |_
 `._____.'|________| `.___.' `.____.'   \______.' `.___.'|_____|\____|

Below are Point Line Polygon geojson function helpers. You can create features using these three functions.
They are the simplest ones, and we don't implement multi-line or multi-polygon, but for now this is enough.
"""


def point_feature(lon, lat, props=None):
    """
    Creates a geojson feature point that can be added to a feature list.
    Example:
        p = point_feature(-97.3, 32.7, {"name": "Wichita Falls"})
    """

    if props is None:
        props = {}

    return {
        "type": "Feature",
        "properties": props,
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
    }


def line_feature(coords, props=None):
    """
    Creates a geojson feature line that can be added to a feature list.
    Example:
        line = line_feature([
            [-97.3, 32.7],
            [-96.8, 33.0]
        ])
    """

    if props is None:
        props = {}

    return {
        "type": "Feature",
        "properties": props,
        "geometry": {"type": "LineString", "coordinates": coords},
    }


def polygon_feature(coords, props=None):
    """
     Creates a geojson feature polygon that can be added to a feature list.
    Example:
        poly = polygon_feature([
            [-100,40],
            [-100,35],
            [-95,35],
            [-95,40]
        ])
    """

    if props is None:
        props = {}

    if coords[0] != coords[-1]:
        coords = coords + [coords[0]]

    return {
        "type": "Feature",
        "properties": props,
        "geometry": {"type": "Polygon", "coordinates": [coords]},
    }


def feature_collection(features):
    """
    This will accept a list of geojson features (like point, line, polygon) above and
    create a FeatureCollection that can be saved or used and displayed.
    """

    return {"type": "FeatureCollection", "features": features}

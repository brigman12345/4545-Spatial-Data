from __future__ import annotations

from typing import Dict, List, Tuple, Optional

import folium

from src.geo_math import trajectory_points


def make_base_map(
    lat: float, lon: float, zoom: int = 2, tiles: str = "OpenStreetMap"
) -> folium.Map:
    return folium.Map(location=[lat, lon], zoom_start=zoom, tiles=tiles)


def add_geojson_layer(
    m: folium.Map,
    features: List[dict],
    name: str = "Layer",
    tooltip_field: Optional[str] = None,
) -> None:
    """
    Add a list of GeoJSON-like Features (plain dicts) as a Folium GeoJson layer.
    """
    fc = {"type": "FeatureCollection", "features": features}

    tooltip = None
    if tooltip_field:
        tooltip = folium.GeoJsonTooltip(
            fields=[tooltip_field], aliases=[f"{tooltip_field}:"]
        )

    folium.GeoJson(fc, name=name, tooltip=tooltip).add_to(m)


def add_base_marker(m: folium.Map, lat: float, lon: float, label: str = "Base") -> None:
    folium.Marker(
        [lat, lon], tooltip=label, icon=folium.Icon(color="blue", icon="home")
    ).add_to(m)


# ---------------------------------------------------------
# Threat + Trajectory plotting (NO shapely required)
# ---------------------------------------------------------


def _threat_style(threat_type: str) -> Dict:
    """
    Central place to style threats by type.
    Keep it simple early; you can get fancy later.
    """
    t = (threat_type or "").lower()

    # Folium will pick default colors if we don't specify; we keep minimal.
    if t == "alien":
        return {"marker_color": "green", "line_weight": 3}
    if t == "orbital":
        return {"marker_color": "purple", "line_weight": 4}
    if t == "airborne":
        return {"marker_color": "orange", "line_weight": 3}
    if t == "kaiju":
        return {"marker_color": "red", "line_weight": 5}

    return {"marker_color": "gray", "line_weight": 3}


def add_threat_origin_marker(m: folium.Map, threat: Dict) -> None:
    """
    Add a marker for the threat origin.
    Threat is a plain dict (loaded from JSON).
    Required keys: id, type, origin_lat, origin_lon
    """
    tid = threat.get("id", "unknown")
    ttype = threat.get("type", "unknown")
    lat = float(threat["origin_lat"])
    lon = float(threat["origin_lon"])

    style = _threat_style(ttype)

    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        tooltip=f"{tid} ({ttype}) origin",
        fill=True,
        color=None,  # let folium default outline
    ).add_to(m)


def add_threat_trajectory(
    m: folium.Map,
    threat: Dict,
    step_min: float = 2.0,
    show_steps: bool = False,
    steps_every: int = 3,
) -> List[Tuple[float, float]]:
    """
    Compute and plot a threat trajectory.

    Returns the list of (lat, lon) points used, so caller can reuse them.

    Required keys:
      - origin_lat, origin_lon
      - bearing_deg
      - speed_kmh
      - duration_min
      - id, type (for labels)
    """
    tid = threat.get("id", "unknown")
    ttype = threat.get("type", "unknown")

    origin_lat = float(threat["origin_lat"])
    origin_lon = float(threat["origin_lon"])
    bearing = float(threat["bearing_deg"])
    speed = float(threat["speed_kmh"])
    duration = float(threat["duration_min"])

    pts = trajectory_points(
        origin_lat=origin_lat,
        origin_lon=origin_lon,
        bearing_deg=bearing,
        speed_kmh=speed,
        duration_min=duration,
        step_min=step_min,
    )

    style = _threat_style(ttype)

    folium.PolyLine(
        locations=pts,  # folium wants [(lat, lon), ...]
        tooltip=f"{tid} trajectory",
        weight=style["line_weight"],
    ).add_to(m)

    if show_steps:
        # Drop little markers on every Nth step so students can "see time"
        for idx, (lat, lon) in enumerate(pts):
            if idx % max(1, steps_every) != 0:
                continue
            folium.CircleMarker(
                location=[lat, lon], radius=2, tooltip=f"{tid} step {idx}", fill=True
            ).add_to(m)

    return pts


def add_threats_layer(
    m: folium.Map, threats: List[Dict], step_min: float = 2.0, show_steps: bool = False
) -> None:
    """
    Convenience: add all threats (origins + trajectories).
    """
    for th in threats:
        add_threat_origin_marker(m, th)
        add_threat_trajectory(m, th, step_min=step_min, show_steps=show_steps)

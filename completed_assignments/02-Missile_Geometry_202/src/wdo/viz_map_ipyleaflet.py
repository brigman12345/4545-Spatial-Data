from __future__ import annotations

from typing import Dict, List, Tuple, Optional, Any

from ipyleaflet import (
    GeoJSON,
    Map,
    Marker,
    CircleMarker,
    Polyline,
    LayersControl,
    ScaleControl,
    basemaps,
)
from ipywidgets import HTML, Layout

from src.geo_math import trajectory_points


BASEMAPS = {
    "OpenStreetMap": basemaps.OpenStreetMap.Mapnik,
    "CartoDB.Positron": basemaps.CartoDB.Positron,
    "CartoDB.Voyager": basemaps.CartoDB.Voyager,
    "Esri.WorldStreetMap": basemaps.Esri.WorldStreetMap,
}


def _resolve_basemap(tiles: str):
    """
    Resolve a friendly tile name to an ipyleaflet basemap.
    Defaults to CartoDB.Positron to avoid raw OSM tile-policy headaches.
    """
    return BASEMAPS.get(tiles, basemaps.CartoDB.Positron)


def make_base_map(
    lat: float,
    lon: float,
    zoom: int = 2,
    tiles: str = "CartoDB.Positron",
    add_scale: bool = True,
    add_layers_control: bool = False,
    height: str = "600px",
    width: str = "100%",
) -> Map:
    """
    Create a base ipyleaflet map.

    Notes
    -----
    - ipyleaflet expects center=(lat, lon)
    - GeoJSON coordinates remain [lon, lat]
    """
    m = Map(
        center=(lat, lon),
        zoom=zoom,
        basemap=_resolve_basemap(tiles),
        layout=Layout(height=height, width=width),
        scroll_wheel_zoom=True,
    )

    if add_scale:
        m.add(ScaleControl(position="bottomleft"))
    if add_layers_control:
        m.add(LayersControl(position="topright"))

    return m


def add_geojson_layer(
    m: Map,
    features: List[dict],
    name: str = "Layer",
    tooltip_field: Optional[str] = None,
    style: Optional[dict] = None,
    hover_style: Optional[dict] = None,
) -> GeoJSON:
    """
    Add a list of GeoJSON-like Features (plain dicts) as an ipyleaflet GeoJSON layer.

    ipyleaflet does not provide the same one-line tooltip API as Folium, so when
    tooltip_field is supplied we attach a popup to each feature in-place.
    """
    fc = {"type": "FeatureCollection", "features": features}

    if tooltip_field:
        for feature in fc["features"]:
            props = feature.setdefault("properties", {})
            value = props.get(tooltip_field, "")
            props["popup"] = f"<b>{tooltip_field}:</b> {value}"

    layer = GeoJSON(
        data=fc,
        name=name,
        style=style or {},
        hover_style=hover_style or {},
    )
    m.add(layer)
    return layer


def add_base_marker(m: Map, lat: float, lon: float, label: str = "Base") -> Marker:
    """
    Add a marker for the base location.
    """
    marker = Marker(
        location=(lat, lon),
        title=label,
        draggable=False,
    )
    marker.popup = HTML(value=f"<b>{label}</b>")
    m.add(marker)
    return marker


# ---------------------------------------------------------
# Threat + Trajectory plotting (NO shapely required)
# ---------------------------------------------------------


def _threat_style(threat_type: str) -> Dict[str, Any]:
    """
    Central place to style threats by type.
    """
    t = (threat_type or "").lower()

    if t == "alien":
        return {"color": "green", "weight": 3, "radius": 5}
    if t == "orbital":
        return {"color": "purple", "weight": 4, "radius": 5}
    if t == "airborne":
        return {"color": "orange", "weight": 3, "radius": 5}
    if t == "kaiju":
        return {"color": "red", "weight": 5, "radius": 6}

    return {"color": "gray", "weight": 3, "radius": 5}


def add_threat_origin_marker(m: Map, threat: Dict) -> CircleMarker:
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

    marker = CircleMarker(
        location=(lat, lon),
        radius=style["radius"],
        color=style["color"],
        fill_color=style["color"],
        fill_opacity=0.85,
        weight=2,
    )
    marker.popup = HTML(value=f"<b>{tid}</b> ({ttype}) origin")
    m.add(marker)
    return marker


def add_threat_trajectory(
    m: Map,
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

    line = Polyline(
        locations=pts,  # ipyleaflet wants [(lat, lon), ...]
        color=style["color"],
        weight=style["weight"],
        fill=False,
    )
    line.popup = HTML(value=f"<b>{tid}</b> trajectory")
    m.add(line)

    if show_steps:
        for idx, (lat, lon) in enumerate(pts):
            if idx % max(1, steps_every) != 0:
                continue
            step_marker = CircleMarker(
                location=(lat, lon),
                radius=2,
                color=style["color"],
                fill_color=style["color"],
                fill_opacity=0.75,
                weight=1,
            )
            step_marker.popup = HTML(value=f"{tid} step {idx}")
            m.add(step_marker)

    return pts


def add_threats_layer(
    m: Map,
    threats: List[Dict],
    step_min: float = 2.0,
    show_steps: bool = False,
) -> None:
    """
    Convenience: add all threats (origins + trajectories).
    """
    for th in threats:
        add_threat_origin_marker(m, th)
        add_threat_trajectory(m, th, step_min=step_min, show_steps=show_steps)

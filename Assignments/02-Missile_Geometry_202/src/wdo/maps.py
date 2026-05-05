from __future__ import annotations

from typing import Any, Iterable

from ipyleaflet import (
    GeoJSON,
    LayersControl,
    Map,
    Marker,
    ScaleControl,
    basemaps,
)
from ipywidgets import Layout


# Small, explicit set of supported basemaps.
# Keep this list short so the course stays simple.
BASEMAPS = {
    "positron": basemaps.CartoDB.Positron,
    "voyager": basemaps.CartoDB.Voyager,
    "esri": basemaps.Esri.WorldStreetMap,
    "osm": basemaps.OpenStreetMap.Mapnik,
}


def map(
    center: tuple[float, float] = (33.8715, -98.5217),
    zoom: int = 10,
    basemap_name: str = "positron",
    scale: bool = True,
    layers_control: bool = False,
    scroll_wheel_zoom: bool = True,
    height: str = "600px",
    width: str = "100%",
    **kwargs: Any,
) -> Map:
    """
    Create and return an ipyleaflet Map with safe classroom defaults.

    Parameters
    ----------
    center : tuple[float, float]
        Map center as (latitude, longitude).
    zoom : int
        Initial zoom level.
    basemap_name : str
        One of: "positron", "voyager", "esri", "osm".
    scale : bool
        If True, add a scale control in the bottom-left corner.
    layers_control : bool
        If True, add a layers control in the top-right corner.
    scroll_wheel_zoom : bool
        Enable zooming with the mouse wheel.
    height : str
        Map height, e.g. "600px".
    width : str
        Map width, e.g. "100%".
    **kwargs : Any
        Extra keyword arguments passed directly to ipyleaflet.Map.

    Returns
    -------
    Map
        A configured ipyleaflet Map object.

    Notes
    -----
    - center uses (lat, lon) because that is what ipyleaflet expects.
    - GeoJSON coordinates remain [lon, lat].
    - The default basemap is CartoDB Positron to avoid unnecessary
      headaches with raw OSM tile usage in classroom settings.
    """
    basemap = BASEMAPS.get(basemap_name.lower(), BASEMAPS["positron"])

    m = Map(
        center=center,
        zoom=zoom,
        basemap=basemap,
        scroll_wheel_zoom=scroll_wheel_zoom,
        layout=Layout(width=width, height=height),
        **kwargs,
    )

    if scale:
        m.add(ScaleControl(position="bottomleft"))

    if layers_control:
        m.add(LayersControl(position="topright"))

    return m


def add_marker(
    m: Map,
    location: tuple[float, float],
    popup: Any | None = None,
    draggable: bool = False,
    **kwargs: Any,
) -> Marker:
    """
    Add a marker to an existing map and return the marker.

    Parameters
    ----------
    m : Map
        The map to modify.
    location : tuple[float, float]
        Marker location as (latitude, longitude).
    popup : Any | None
        Optional popup widget or text-like object.
    draggable : bool
        Whether the marker can be dragged.
    **kwargs : Any
        Extra keyword arguments passed to ipyleaflet.Marker.

    Returns
    -------
    Marker
        The created marker.
    """
    marker = Marker(location=location, draggable=draggable, **kwargs)

    if popup is not None:
        marker.popup = popup

    m.add(marker)
    return marker


def add_geojson(
    m: Map,
    data: dict,
    style: dict | None = None,
    hover_style: dict | None = None,
    name: str | None = None,
    **kwargs: Any,
) -> GeoJSON:
    """
    Add a GeoJSON layer to an existing map and return the layer.

    Parameters
    ----------
    m : Map
        The map to modify.
    data : dict
        A GeoJSON dictionary.
    style : dict | None
        Optional style dictionary for the GeoJSON layer.
    hover_style : dict | None
        Optional hover style dictionary.
    name : str | None
        Optional layer name.
    **kwargs : Any
        Extra keyword arguments passed to ipyleaflet.GeoJSON.

    Returns
    -------
    GeoJSON
        The created GeoJSON layer.
    """
    layer = GeoJSON(
        data=data,
        style=style or {},
        hover_style=hover_style or {},
        name=name,
        **kwargs,
    )
    m.add(layer)
    return layer


def bbox_to_bounds(
    bbox: Iterable[float],
) -> tuple[tuple[float, float], tuple[float, float]]:
    """
    Convert a bbox in [min_lon, min_lat, max_lon, max_lat] format
    into ipyleaflet bounds format:
        ((south, west), (north, east))

    Parameters
    ----------
    bbox : Iterable[float]
        Bounding box as [min_lon, min_lat, max_lon, max_lat].

    Returns
    -------
    tuple[tuple[float, float], tuple[float, float]]
        Bounds in the format expected by map.fit_bounds(...).
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    return ((min_lat, min_lon), (max_lat, max_lon))


def fit_bbox(m: Map, bbox: Iterable[float]) -> None:
    """
    Fit an existing map to a bbox in [min_lon, min_lat, max_lon, max_lat] format.

    Parameters
    ----------
    m : Map
        The map to modify.
    bbox : Iterable[float]
        Bounding box as [min_lon, min_lat, max_lon, max_lat].
    """
    m.fit_bounds(bbox_to_bounds(bbox))

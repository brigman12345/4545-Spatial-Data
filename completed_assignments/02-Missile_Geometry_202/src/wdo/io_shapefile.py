from __future__ import annotations

from pathlib import Path
import shapefile  # pyshp


def require_shapefile_set(shp_path: Path) -> None:
    """
    Ensure .shp, .shx, .dbf exist. Fail loudly with clear errors.
    """
    shp_path = Path(shp_path)
    if shp_path.suffix.lower() != ".shp":
        raise ValueError(f"Expected a .shp file path, got: {shp_path}")

    required = [shp_path, shp_path.with_suffix(".shx"), shp_path.with_suffix(".dbf")]
    missing = [p for p in required if not p.exists()]

    if missing:
        msg = "\n".join(f"  - missing: {p}" for p in missing)
        raise FileNotFoundError(
            f"Shapefile is incomplete. You need .shp + .shx + .dbf.\n{msg}"
        )


def read_prj_if_exists(shp_path: Path) -> str | None:
    prj = Path(shp_path).with_suffix(".prj")
    return prj.read_text(errors="ignore") if prj.exists() else None


def shapefile_to_features(shp_path: Path, id_field: str | None = None) -> list[dict]:
    """
    Convert a shapefile into a list of GeoJSON-like Features (plain dicts).
    No GeoPandas. No DataFrames.
    """
    require_shapefile_set(shp_path)

    r = shapefile.Reader(str(shp_path))
    fields = [f[0] for f in r.fields[1:]]  # skip deletion flag

    features: list[dict] = []
    for i, sr in enumerate(r.iterShapeRecords()):
        props = dict(zip(fields, sr.record))

        # pyshp gives geometry mappings compatible with GeoJSON-ish structure
        geom = sr.shape.__geo_interface__  # dict with type/coordinates

        # choose id
        fid = props.get(id_field) if (id_field and id_field in props) else i

        features.append(
            {
                "type": "Feature",
                "id": fid,
                "properties": props,
                "geometry": geom,
            }
        )

    return features

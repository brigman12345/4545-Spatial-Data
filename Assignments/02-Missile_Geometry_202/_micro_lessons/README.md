# Missile Geometry 202 — Micro Lesson Roadmap

These micro lessons are designed to build the skills needed for the **Missile Geometry 202** project one concept at a time. Each lesson introduces a small, focused idea. The final project is where those ideas are combined.

The general progression is:

```text
Paths → JSON/GeoJSON → Viewing Maps → Styling → Interactive Maps
→ Coordinate Geometry → Distance → Bearing → Intercept & Pursuit
→ Intersections → Buffers → Point in Polygon
→ Refactoring → WDO Library
```

| #   | Folder                                                                                   | Description                                               |
| --- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| 00  | [00-Paths](00-Paths)                                                                     | File paths, working directories, and locating data files  |
| 01  | [01-JSON_GeoJSON](01-JSON_GeoJSON)                                                       | Reading JSON and GeoJSON; FeatureCollection structure     |
| 02  | [02-Viewing_GeoJSON](02-Viewing_GeoJSON)                                                 | Displaying GeoJSON on interactive maps                    |
| 03  | [03-Attributes_Styling_Filtering](03-Attributes_Styling_Filtering)                       | Feature properties, dynamic styling, and filtering        |
| 04  | [04-Interactive_Maps](04-Interactive_Maps)                                               | Map events, clicks, dynamic layers, and output widgets    |
| 05  | [05-Coordinate_Geometry](05-Coordinate_Geometry)                                         | Coordinate ranges, bounding boxes, and lat/lon geometry   |
| 06  | [06-Distance](06-Distance)                                                               | Euclidean vs haversine distance; applications and batching|
| 07  | [07-Bearing](07-Bearing)                                                                 | Computing bearing, bearing drift, and navigation logic    |
| 08  | [08-Intercept_Pursuit_Module_Design](08-Intercept_Persuit_Module_Design)                 | Intercept geometry, pursuit curves, and simulations       |
| 09  | [09-Intersections](09-Intersections)                                                     | Line-segment and path-vs-polygon intersection detection   |
| 10  | [10-Buffers](10-Buffers)                                                                 | Point and line buffers, impact zones, CRS limitations     |
| 11  | [11-Point_In_Polygon](11-Point_In_Polygon)                                               | Ray-casting algorithm, click-to-region classification     |
| 12  | [12-Refactoring](12-Refactoring)                                                         | Refactoring notebook code into reusable helper functions  |
| 13  | [13-WDO_Library](13-WDO_Library)                                                         | Installing and importing the `wdo` project library        |

---

## 00 — Paths, Working Directories, and Data Files

### Goal

Learn how to locate files reliably before doing any spatial work.

### Students will practice

- checking the current working directory
- building paths with `pathlib`
- reading files relative to the notebook location
- finding the project root from any notebook

### Why this matters

Before students can load GeoJSON, JSON, or images, they need to understand where their code is running and where the data lives.

---

## 01 — JSON, GeoJSON, and Feature Collections

### Goal

Understand the structure of the data before trying to display it.

### Students will practice

- reading JSON files with Python's `json` module
- identifying `FeatureCollection`, `Feature`, `properties`, and `geometry`
- distinguishing regular JSON from GeoJSON
- understanding that GeoJSON coordinates are stored as `[lon, lat]`

### Why this matters

Students should know what they are holding in memory before trying to map or analyze it.

---

## 02 — Viewing GeoJSON

### Goal

Load GeoJSON and display it on an interactive map.

### Students will practice

- using geojson.io for quick visualization
- creating maps with ipyleaflet
- adding GeoJSON layers to a map
- controlling basemaps, zoom, and layer settings

### Why this matters

This is the first "reward" notebook: students see their data on a map.

---

## 03 — Attributes, Styling, and Filtering

### Goal

Use feature data to control how things look and what gets displayed.

### Students will practice

- reading `feature["properties"]`
- styling features dynamically with `style_callback`
- coloring based on attribute values
- filtering features before display

### Why this matters

Students learn that **data drives map output**.

---

## 04 — Interactive Maps

### Goal

Make maps respond to user input.

### Students will practice

- registering event handlers on ipyleaflet maps
- handling click events and extracting coordinates
- adding and removing GeoJSON layers dynamically
- displaying results using ipywidgets Output

### Why this matters

Students move from viewing maps to **interacting** with maps.

---

## 05 — Coordinate Geometry

### Goal

Understand the geometry of geographic coordinates before doing math with them.

### Students will practice

- working with valid longitude (−180 to 180) and latitude (−90 to 90) ranges
- computing bounding boxes from point sets
- drawing bounding boxes as GeoJSON polygons
- understanding why lat/lon arithmetic differs from Cartesian math

### Why this matters

This is the first step from "displaying shapes" to "reasoning about space."

---

## 06 — Distance

### Goal

Compute geographic distances between real locations.

### Students will practice

- computing naive Euclidean distance in degree space
- applying the haversine formula for spherically-accurate great-circle distance
- comparing both methods across latitudes
- solving range, nearest-target, and coverage problems

### Why this matters

Distance is one of the core mathematical tools needed for the final project.

---

## 07 — Bearing

### Goal

Compute compass direction as a measurable, usable quantity.

### Students will practice

- understanding bearing as clockwise degrees from North
- calculating bearing between two geographic points using `atan2`
- understanding bearing drift along a great-circle path
- applying bearing to sector filtering, direction arrows, and targeting

### Why this matters

Students isolate the directional math before using it in more complex trajectory work.

---

## 08 — Intercept & Pursuit

### Goal

Model the geometry of one object chasing or intercepting another.

### Students will practice

- defining the intercept problem: pursuer, target, velocity
- solving intercept time with binary search root-finding
- simulating iterative pursuit curves step by step
- building interactive click-to-place simulations

### Why this matters

Students combine distance and bearing into a dynamic, time-dependent geometry problem.

---

## 09 — Intersections

### Goal

Determine whether paths intersect polygon regions.

### Students will practice

- representing trajectories as GeoJSON LineStrings
- detecting two-segment crossings using orientation and cross-product math
- testing a path against a polygon by checking each edge pair
- running paths against real country boundary data

### Why this matters

This supports reasoning about routes, paths, and impacted regions.

---

## 10 — Buffers and Zones

### Goal

Create zones of influence around points or lines.

### Students will practice

- building accurate circular buffers in kilometers using the destination-point formula
- creating line corridor buffers via sampled overlapping circles
- comparing concentric zone rings and multi-target buffers
- understanding why degree-offset buffers are geometrically incorrect

### Why this matters

Buffers introduce area-based reasoning and set up future damage-zone logic.

---

## 11 — Point in Polygon

### Goal

Determine which polygon contains a clicked point.

### Students will practice

- capturing ipyleaflet click events
- understanding the `[lat, lon]` vs `[lon, lat]` coordinate flip
- implementing the ray-casting algorithm from scratch
- classifying a click by region name across a FeatureCollection

### Why this matters

This is the bridge between **click capture** and **spatial reasoning**.

---

## 12 — Refactoring Spatial Code

### Goal

Organize repeated notebook code into reusable functions and small helper classes.

### Students will practice

- identifying repeated code across notebooks
- refactoring into helper functions
- deciding when a small class is useful
- separating map state from geometry logic

### Why this matters

Students move from "working notebook code" to **reusable project code**.

---

## 13 — Installing and Using the WDO Library

### Goal

Install and use the reusable helper code stored in `src/wdo`.

### Students will practice

- understanding the `src` project layout
- reading the purpose of `pyproject.toml`
- running `pip install -e .`
- importing helper functions from `wdo`

### Why this matters

At this point students have seen enough repeated geometry code that packaging helper functions now feels useful instead of mysterious.

---

# Note to Students

- Each notebook teaches **one new capability**
- Not every notebook is a full assignment
- The final project is where these ideas are assembled together
- You are not expected to memorize everything — you are expected to build and reuse your own notes and examples

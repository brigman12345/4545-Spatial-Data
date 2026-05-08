# Data Manager — Micro Lesson Roadmap

These micro lessons are designed to build the skills needed for the **Data Manager** project one concept at a time. The central problem is a real one: a 40MB world railroad GeoJSON file is far too large to load on every map pan and zoom. These lessons build — from scratch — the tools needed to solve that problem intelligently. A library that solves all of this already exists. We are building the small version first.

The general progression is:

```text
Data Exploration → Douglas-Peucker Simplification → Generating LOD Files
→ Bounding Box Culling → Spatial Grid Index → Zoom-Driven Layer Switching
→ Putting It All Together → The Library Version
```

| #   | Folder                                             | Description                                                             | Notebooks |
| --- | -------------------------------------------------- | ----------------------------------------------------------------------- | :-------: |
| 00  | [00-Data_Exploration](00-Data_Exploration)         | Load and inspect the raw GeoJSON; measure the problem                   |     2     |
| 01  | [01-Douglas_Peucker](01-Douglas_Peucker)           | Understand and implement the core simplification algorithm              |     3     |
| 02  | [02-LOD_Generation](02-LOD_Generation)             | Apply simplification at multiple tolerances; write LOD output files     |     3     |
| 03  | [03-Bounding_Box_Culling](03-Bounding_Box_Culling) | Filter features to the visible viewport using bounding box intersection |     3     |
| 04  | [04-Spatial_Grid_Index](04-Spatial_Grid_Index)     | Speed up culling with a simple grid-based spatial index                 |     3     |
| 05  | [05-Zoom_Layer_Switching](05-Zoom_Layer_Switching) | Select and load the correct LOD file based on zoom level                |     2     |
| 06  | [06-Putting_It_Together](06-Putting_It_Together)   | Combine all components into a working interactive railroad viewer       |     2     |
| 07  | [07-The_Library_Version](07-The_Library_Version)   | Reproduce the same result using `tippecanoe` and vector tiles           |     3     |

---

## 00 — Data Exploration

### Goal

Understand the raw data before touching it. Measure the problem.

### Students will practice

- loading a large GeoJSON file and inspecting its structure
- counting features, checking geometry types, and reading properties
- computing a bounding box over the full dataset
- timing a naive load-and-display attempt to feel the performance problem firsthand

### Why this matters

You cannot design a solution to a problem you have not measured. This notebook makes the case for everything that follows.

---

## 01 — Douglas-Peucker Simplification

### Goal

Understand and implement the algorithm that reduces the number of points in a line while preserving its shape.

### Students will practice

- tracing the Douglas-Peucker algorithm by hand on a small example
- implementing the recursive algorithm in Python
- verifying their output against `shapely.simplify()`
- experimenting with different `epsilon` values and observing the tradeoff

### Why this matters

This is the core concept. Every LOD pipeline, every simplification tool, every geometry compression scheme rests on ideas like this one. Students who can build a toy version understand the tool. Students who only import it do not.

---

## 02 — LOD File Generation

### Goal

Apply the simplification algorithm at four tolerance levels and write the output files.

### Students will practice

- designing an epsilon-to-zoom-level mapping
- writing a pipeline that processes all features and applies D-P at each level
- measuring how feature count and file size change at each level
- writing four output GeoJSON files: `coarse`, `medium`, `fine`, `extra_fine`

### Why this matters

This is the first time the algorithm is applied at scale. Students see the connection between epsilon, visual fidelity, and file size — and make deliberate tradeoffs.

| Level      | Zoom Range | Epsilon (degrees) | Approx. Output Size |
| ---------- | ---------- | ----------------- | ------------------- |
| Coarse     | 1–3        | ~1.0              | ~500 KB             |
| Medium     | 4–6        | ~0.1              | ~2–3 MB             |
| Fine       | 7–10       | ~0.01             | ~8–10 MB            |
| Extra Fine | 11+        | ~0.001            | ~20–25 MB           |

---

## 03 — Bounding Box Culling

### Goal

Eliminate features that fall entirely outside the current map viewport before rendering.

### Students will practice

- computing an axis-aligned bounding box for any GeoJSON feature
- writing a bounding box intersection test
- applying the filter to a LOD file and measuring how many features are removed
- displaying only the culled result on a map

### Why this matters

Even the simplified `fine` layer has thousands of features spread across the world. When you are looking at Kansas, you do not need Siberia. This lesson teaches spatial filtering as a performance tool.

---

## 04 — Spatial Grid Index

### Goal

Speed up viewport culling by avoiding a full linear scan of every feature.

### Students will practice

- dividing the world into a uniform grid of cells
- pre-assigning features to the cells they overlap
- querying only the cells that intersect the current viewport
- comparing query time with and without the index

### Why this matters

Iterating every feature for every pan event is O(n). A spatial index reduces the query to a small subset. Students learn _why_ spatial indexes exist — not just that they do. This is the conceptual precursor to R-trees, quadtrees, and every other spatial data structure they will encounter later.

---

## 05 — Zoom-Driven Layer Switching

### Goal

Select and load the correct LOD file in response to zoom level changes.

### Students will practice

- registering a zoom event handler in ipyleaflet
- writing a `get_layer(zoom)` decision function
- dynamically swapping the active GeoJSON layer on the map
- combining layer switching with bounding box culling

### Why this matters

This is the moment the pieces connect. The map now behaves like a real mapping application: different data at different scales, loaded on demand.

---

## 06 — Putting It All Together

### Goal

Combine every component into a working interactive railroad viewer.

### Students will practice

- wiring up D-P simplified LOD files, viewport culling, and zoom-driven switching into one clean notebook
- identifying which parts are slow and which are fast
- observing where the remaining pain points are (reload time, layer flicker, file I/O)
- documenting the design decisions they made

### Why this matters

Students see a working system built entirely from components they understand. This is the completion moment — and also the setup for the next lesson.

---

## 07 — The Library Version

### Goal

Reproduce the LOD pipeline using `tippecanoe` and understand what it automates.

### Students will practice

- installing and running `tippecanoe` on the raw GeoJSON
- inspecting the output: `.pmtiles` or `.mbtiles` format, tile pyramid structure
- loading vector tiles in ipyleaflet
- comparing the library output visually and structurally against their handbuilt version

### Why this matters

At this point students have built the small version and felt every tradeoff. The library version is no longer a black box. Students can now answer: _what did tippecanoe just save us from?_ — and name specific things, because they built those things.

---

# Note to Students

- Each notebook teaches **one new capability**
- Not every notebook is a full assignment — some are conceptual exercises
- The final viewer is where all the ideas assemble
- You should be able to explain every component you use, even the ones you borrowed
- If you cannot explain what a library parameter does, you are not done learning it

## Module 00-Data_Exploration

```
00-Data_Exploration/
├── README.md
├── 00-Loading_and_Inspecting.ipynb
└── 01-Measuring_the_Problem.ipynb
```

### 00-Loading_and_Inspecting:

students load the file, inspect the FeatureCollection structure, examine a single feature's geometry and properties, verify all geometry types, then do two exercises (`unique categories`, `scalerank counts`). CYU asks them to find the most common `natlscale` value.

### 01-Measuring_the_Problem:

students measure file size, total coordinate count, load time, see a 500-feature random sample on a map, and build a problem summary. Exercises: find the 10 longest features, and measure what fraction of coordinates the high-importance trunk lines account for. CYU asks them to name two other costs beyond file load before a feature is visible.

## Module 01-Douglas_Peucker

```
01-Douglas_Peucker/
├── README.md
├── 00-The_Algorithm.ipynb
├── 01-Implementation.ipynb
└── 02-Epsilon_and_Tradeoffs.ipynb
```

### 00-The_Algorithm

> conceptual

Explains perpendicular distance visually, walks the 7-point example step by step with matplotlib plots, traces both rounds of recursion. Exercises ask students to trace a 5-point line at two epsilon values. CYU asks why endpoints are never candidates for removal.

### 01-Implementation:

> implementation

Derives the perpendicular distance formula from the cross product, implements both functions, verifies on the known 7-point example, plots four epsilon levels side by side, then cross-checks against shapely.simplify() on a generated wavy line. Exercises: add recursion tracing, then adapt for GeoJSON [lon, lat] lists. CYU asks for the worst-case recursive call count.

### 02-Epsilon_and_Tradeoffs:

> real data

Applies both implementations to actual railroad features, builds a table of total coordinate counts and reduction percentages across all four epsilon levels, renders a 500-feature sample on an ipyleaflet map, does a direct Shapely comparison on the longest feature. Exercises: design the LOD epsilon table with justifications; count 2-point features at coarse level. CYU asks about degree-space epsilon and latitude distortion.

## Module 02-LOD_Generation

```
02-LOD_Generation/
├── README.md
├── 00-Designing_the_Pipeline.ipynb
├── 01-Writing_the_LOD_Files.ipynb
└── 02-Comparing_the_Levels.ipynb
```

### 00-Designing_the_Pipeline:

> Design decisions before any code

Introduces the four zoom bands, the degree-to-km epsilon guide, and the two edge cases (feature collapse + scalerank filtering). Students measure exactly how many features collapse at each epsilon and how many survive a scalerank filter. Exercises: argue for/against keeping the scalerank filter; evaluate natlscale as an alternative filter. CYU: defend dropping collapsed features against the "never drop data" argument.

### 01-Writing_the_LOD_Files:

> The Pipeline

Defines a LOD_LEVELS config list, implements simplify_feature(), runs the full pipeline with a formatted output table (in/out/dropped/size/time), spot-checks a loaded output file. Exercises: run coarse without scalerank filter and compare; measure the file size cost of indent=2. CYU: preserve_topology=True vs False — which is right for this use case and why.

### 02-Comparing_the_Levels:

> Comparison

Loads all four files, builds a summary table vs. the original, displays each level on an ipyleaflet map at its intended zoom, and plots all four levels side-by-side cropped to Europe. Exercises: trace a single feature by rwdb_rr_id across all four levels; calculate compression ratios. CYU: what happens in a region where all features are filtered out by scalerank — and what does that reveal about the filter's limitation.

## Module 03-Bounding_Box_Culling

```
03-Bounding_Box_Culling/
├── README.md
├── 00-Bounding_Boxes.ipynb
├── 01-Intersection_Test.ipynb
└── 02-Viewport_Culling.ipynb
```

### 00-Bounding_Boxes:

> What a bounding box is and how to compute one

Discovers that the raw railroad dataset already has precomputed bbox fields, verifies the computed version matches, visualizes a feature and its bbox on a map, and confirms the LOD files don't have them (so we compute on the fly). Exercises: write collection_bbox() and compare extents across all four LOD files; find the 5 largest bbox-area features. CYU: two different features can have identical bounding boxes — describe when and whether it causes a problem.

### 01-Intersection_Test:

> The intersection test

Derives the logic from the non-overlap conditions (left/right/below/above), implements bbox_intersects, runs 13 named test cases covering every spatial relationship, visualizes 4 of them with matplotlib patches. Exercises: write a strict version that rejects edge-touching; write cull() and apply to fine LOD over Europe. CYU: describe a false-positive case (feature bbox intersects viewport but actual geometry doesn't) and whether it's worth solving.

### 02-Viewport_Culling

> Live culling

Introduces m.bounds and the lat/lon flip gotcha, measures cull reduction at 5 viewport scales (world → central Paris), builds a live map where pan/zoom events trigger re-culling with a status readout. Exercises: add basic zoom-based LOD switching as a preview of Module 05; time a single cull call and calculate CPU cost at 10 pans/second. CYU: the diagonal-railroad false-positive problem and what a more precise solution would cost.

## Module 04-Spatial_Grid_Index:

```
04-Spatial_Grid_Index/
├── README.md
├── 00-The_Grid_Idea.ipynb
├── 01-Building_the_Index.ipynb
└── 02-Querying_and_Benchmarking.ipynb
```

### 00-The_Grid_Idea

> The concept

Motivates the problem (O(n) per query), explains the grid idea with ASCII diagrams, visualizes the 10° world grid with matplotlib, builds a cells_for_bbox function and runs it across five zoom-level viewports to show how few cells a small viewport touches. Exercises: rerun with 5° cells and explain the effect; find the feature assigned to the most cells. CYU: what happens when the underlying data changes — does the index need a full rebuild?

### 01-Building_The_Index:

> The implementation

Builds the full GridIndex class with build() and query(), populates it with the fine LOD, shows stats (occupied cells, total refs, busiest cell), renders a density heatmap with imshow (which is itself a geographic insight), verifies all features are indexed. Exercises: build at three cell sizes and compare memory/time; display the busiest cell's features on a map. CYU: why set for deduplication instead of a list check.

### 02-Querying_and_Benchmarking

> Correctness check then benchmark

Verifies grid and linear scan return identical feature sets, benchmarks both methods 100× each across five viewports and prints a speedup table, wires the grid index into a live ipyleaflet map with per-query timing in the status bar, explains why the grid loses at world zoom and wins at city zoom, introduces quadtrees/R-trees as the next evolution. Exercises: instrument the world-zoom query to explain why it's slower; try Shapely STRtree and compare. CYU: references vs. copies — memory cost of multi-cell storage and why dedup is still needed.

## 05-Zoom_Layer_Switching

```
05-Zoom_Layer_Switching/
├── README.md
├── 00-The_Decision_Function.ipynb
└── 01-Live_Layer_Switching.ipynb
```

### 00-The_Decision_Function

> The decision function

Explains web map zoom levels with a log-scale chart and a zoom→degrees table, marks the LOD transition boundaries on that chart, implements the basic get_lod(zoom), then introduces the flicker problem and solves it with hysteresis (different thresholds for zoom-in vs. zoom-out). Simulates a full zoom-in and zoom-out pass to show where switches happen. Exercises: refactor with a configurable thresholds dict; plot the zoom-in vs. zoom-out LOD trajectories to visualize the hysteresis band. CYU: how to extend get_lod to also consider viewport width in degrees.

### 01-Live_Layer_Switching

> The live map

Loads all four LOD files and builds all four grid indexes at startup with timing output, then builds a compact map with a single update() handler that covers both zoom and bounds events, switching the active index and re-querying in one step. Status bar shows current LOD name, visible feature count, and query latency. Includes a system diagram showing the full data flow from user interaction to layer update. Exercises: add a zoom-level + scale label to the status bar; trace which event (zoom or bounds) fires when to observe their sequencing. CYU: eager vs. lazy index construction — tradeoffs for startup time vs. first-use latency.

## Module 06-Putting_It_Together

### 00-The_Viewer:

> This is the clean assembly

All components are in one readable file, LOD_CONFIG as the single source of truth, style_callback varying line weight by scalerank, status bar showing LOD/zoom/features/query time.

### 01-What_We_Built:

> This is the honest audit

A measurement table comparing all files, isolated analysis of each pain point (startup cost, verbose format, whole-file loading, no streaming), and a design decision inventory table. CYU: rank the four pain points by impact on a slow mobile connection.

## Module 07-The_Library_Version

### 00-What_Are_Vector_Tiles

Explains the tile pyramid data model, derives lon_lat_to_tile() from scratch, explains MVT integer encoding and PMTiles format, maps every tile system component back to something students built.

### 01-Using_Tippecanoe

Installs and runs the tool, captures output, maps every flag to a Module 02–05 decision, handles the display fallback gracefully.

### 02-The_Comparison

Has the side-by-side architecture diagram, the numbers table, a precise itemized list of what tippecanoe automated (by name), what it cannot do (real-time filtering), and closes with the opening quote from the precursor document. Final CYU: name three situations where skipping Modules 01–06 would cost the classmate something specific.

## 12 — Refactoring Spatial Code into Reusable Helpers

### Goal

Organize repeated notebook code into reusable functions and small helper classes.

### Students will practice

- identifying repeated code across notebooks
- extracting functions into a `.py` module
- using a `dataclass` to enforce coordinate order
- deciding when a class is better than a plain function
- separating pure geometry from map UI callbacks

### Why this matters

Students move from "working notebook code" to **reusable project code**.
This lesson bridges Modules 05–11 (where functions were written inline) to Module 13 (where they import `wdo.geo` instead of rewriting everything again).

### Notebooks

| #   | Notebook                           | Topics                                                                                      |
| --- | ---------------------------------- | ------------------------------------------------------------------------------------------- |
| 01  | `01-From-Notebook-to-Module.ipynb` | copy-paste problem, modules, `LatLon` dataclass, class vs. function, geometry/UI separation |

1. The copy-paste problem — shows two real haversine_km variants from different notebooks with subtly different constants and formulas, asks "which is right?"
2. Creating a module — writes a geo.py to disk in-notebook so students see exactly what a module is before any abstraction
3. The coordinate order problem — demonstrates that haversine_km(lon, lat, ...) silently produces wrong answers, motivating typed points
4. LatLon dataclass — introduces @dataclass(frozen=True) as a named container, shows how it catches the swap bug at runtime
5. Class vs. function decision — table-driven rule, then a side-by-side showing compute_bearing (stateless → module function) vs. InterceptProblem (stateful → class)
6. Geometry/UI separation — refactors the Module 04 click callback to pull geometry into a pure points_within_radius function that can be tested without a map
7. Structure of wdo/geo.py — shows the full module layout so students know what they're importing in Module 13
8. Refactoring exercise — students adapt point_in_ring to accept LatLon objects
9. Check Your Understanding — asks whether haversine_km or nearest_n should become a class method and why

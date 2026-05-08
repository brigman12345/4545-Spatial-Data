# Module 01 — Douglas-Peucker Simplification

Understand and implement the algorithm that reduces the number of points in a line while preserving its shape. This is the core concept behind every LOD pipeline we build.

| #   | Notebook                                                  | Description                                                                                  |
| --- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 00  | [The Algorithm](./00-The_Algorithm.ipynb)                 | Trace Douglas-Peucker by hand on a small example; understand what it keeps and why           |
| 01  | [Implementation](./01-Implementation.ipynb)               | Implement the recursive algorithm in Python and test it on generated data                    |
| 02  | [Epsilon and Tradeoffs](./02-Epsilon_and_Tradeoffs.ipynb) | Apply to real railroad data; compare outputs at different tolerances; verify against Shapely |

## Exercises & Check Your Understanding

| Notebook                                                  | Exercises                                                                                         | CYU                                                            |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [The Algorithm](./00-The_Algorithm.ipynb)                 | [A](./00-The_Algorithm.ipynb#exercise-a) [B](./00-The_Algorithm.ipynb#exercise-b)                 | [✓](./00-The_Algorithm.ipynb#check-your-understanding)         |
| [Implementation](./01-Implementation.ipynb)               | [A](./01-Implementation.ipynb#exercise-a) [B](./01-Implementation.ipynb#exercise-b)               | [✓](./01-Implementation.ipynb#check-your-understanding)        |
| [Epsilon and Tradeoffs](./02-Epsilon_and_Tradeoffs.ipynb) | [A](./02-Epsilon_and_Tradeoffs.ipynb#exercise-a) [B](./02-Epsilon_and_Tradeoffs.ipynb#exercise-b) | [✓](./02-Epsilon_and_Tradeoffs.ipynb#check-your-understanding) |

Notebook 00 — conceptual. Explains perpendicular distance visually, walks the 7-point example step by step with matplotlib plots, traces both rounds of recursion. Exercises ask students to trace a 5-point line at two epsilon values. CYU asks why endpoints are never candidates for removal.

Notebook 01 — implementation. Derives the perpendicular distance formula from the cross product, implements both functions, verifies on the known 7-point example, plots four epsilon levels side by side, then cross-checks against shapely.simplify() on a generated wavy line. Exercises: add recursion tracing, then adapt for GeoJSON [lon, lat] lists. CYU asks for the worst-case recursive call count.

Notebook 02 — real data. Applies both implementations to actual railroad features, builds a table of total coordinate counts and reduction percentages across all four epsilon levels, renders a 500-feature sample on an ipyleaflet map, does a direct Shapely comparison on the longest feature. Exercises: design the LOD epsilon table with justifications; count 2-point features at coarse level. CYU asks about degree-space epsilon and latitude distortion.

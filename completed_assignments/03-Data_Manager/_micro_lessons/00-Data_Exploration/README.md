# Module 00 — Data Exploration

Understand the raw railroad dataset before touching it. Measure the problem so the solution makes sense.

| #   | Notebook                                                    | Description                                                                               |
| --- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 00  | [Loading and Inspecting](./00-Loading_and_Inspecting.ipynb) | Load the GeoJSON file and explore its structure, geometry types, and properties           |
| 01  | [Measuring the Problem](./01-Measuring_the_Problem.ipynb)   | Count coordinates, measure file size, time a naive display, and quantify why this is hard |

## Exercises & Check Your Understanding

| Notebook                                                    | Exercises                                                                                           | CYU                                                             |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [Loading and Inspecting](./00-Loading_and_Inspecting.ipynb) | [A](./00-Loading_and_Inspecting.ipynb#exercise-a) [B](./00-Loading_and_Inspecting.ipynb#exercise-b) | [✓](./00-Loading_and_Inspecting.ipynb#check-your-understanding) |
| [Measuring the Problem](./01-Measuring_the_Problem.ipynb)   | [A](./01-Measuring_the_Problem.ipynb#exercise-a) [B](./01-Measuring_the_Problem.ipynb#exercise-b)   | [✓](./01-Measuring_the_Problem.ipynb#check-your-understanding)  |

Notebook 00 — students load the file, inspect the FeatureCollection structure, examine a single feature's geometry and properties, verify all geometry types, then do two exercises (unique categories, scalerank counts). CYU asks them to find the most common natlscale value.

Notebook 01 — students measure file size, total coordinate count, load time, see a 500-feature random sample on a map, and build a problem summary. Exercises: find the 10 longest features, and measure what fraction of coordinates the high-importance trunk lines account for. CYU asks them to name two other costs beyond file load before a feature is visible.

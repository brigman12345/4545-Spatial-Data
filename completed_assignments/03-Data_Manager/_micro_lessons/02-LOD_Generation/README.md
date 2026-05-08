# Module 02 — LOD File Generation

Apply simplification at four tolerance levels and write the output files that power the rest of the project. This is where epsilon values become real files on disk.

| #   | Notebook                                                    | Description                                                                                 |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 00  | [Designing the Pipeline](./00-Designing_the_Pipeline.ipynb) | Plan the four LOD levels, choose epsilons, and handle edge cases before writing any output  |
| 01  | [Writing the LOD Files](./01-Writing_the_LOD_Files.ipynb)   | Run the full simplification pipeline using Shapely and write four GeoJSON output files      |
| 02  | [Comparing the Levels](./02-Comparing_the_Levels.ipynb)     | Load the output files, compare sizes and coordinate counts, and display each level on a map |

## Exercises & Check Your Understanding

| Notebook                                                    | Exercises                                                                                           | CYU                                                             |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [Designing the Pipeline](./00-Designing_the_Pipeline.ipynb) | [A](./00-Designing_the_Pipeline.ipynb#exercise-a) [B](./00-Designing_the_Pipeline.ipynb#exercise-b) | [✓](./00-Designing_the_Pipeline.ipynb#check-your-understanding) |
| [Writing the LOD Files](./01-Writing_the_LOD_Files.ipynb)   | [A](./01-Writing_the_LOD_Files.ipynb#exercise-a) [B](./01-Writing_the_LOD_Files.ipynb#exercise-b)   | [✓](./01-Writing_the_LOD_Files.ipynb#check-your-understanding)  |
| [Comparing the Levels](./02-Comparing_the_Levels.ipynb)     | [A](./02-Comparing_the_Levels.ipynb#exercise-a) [B](./02-Comparing_the_Levels.ipynb#exercise-b)     | [✓](./02-Comparing_the_Levels.ipynb#check-your-understanding)   |

## Output Files

The pipeline writes four files to `data/lod/` in the project root:

| File                           | Epsilon | Zoom Range |
| ------------------------------ | ------- | ---------- |
| `railroads_coarse.geojson`     | 1.0     | 1–3        |
| `railroads_medium.geojson`     | 0.1     | 4–6        |
| `railroads_fine.geojson`       | 0.01    | 7–10       |
| `railroads_extra_fine.geojson` | 0.001   | 11+        |

Notebook 00 — design decisions before any code. Introduces the four zoom bands, the degree-to-km epsilon guide, and the two edge cases (feature collapse + scalerank filtering). Students measure exactly how many features collapse at each epsilon and how many survive a scalerank filter. Exercises: argue for/against keeping the scalerank filter; evaluate natlscale as an alternative filter. CYU: defend dropping collapsed features against the "never drop data" argument.

Notebook 01 — the pipeline. Defines a LOD_LEVELS config list, implements simplify_feature(), runs the full pipeline with a formatted output table (in/out/dropped/size/time), spot-checks a loaded output file. Exercises: run coarse without scalerank filter and compare; measure the file size cost of indent=2. CYU: preserve_topology=True vs False — which is right for this use case and why.

Notebook 02 — comparison. Loads all four files, builds a summary table vs. the original, displays each level on an ipyleaflet map at its intended zoom, and plots all four levels side-by-side cropped to Europe. Exercises: trace a single feature by rwdb_rr_id across all four levels; calculate compression ratios. CYU: what happens in a region where all features are filtered out by scalerank — and what does that reveal about the filter's limitation.

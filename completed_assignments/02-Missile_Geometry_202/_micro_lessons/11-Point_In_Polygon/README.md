# Module 11 — Point in Polygon

Turning a map into a query system: capture a click, ask which region contains it, and get a meaningful answer — built up from first principles.

| # | Notebook | Description |
|---|---|---|
| 00 | [Click Capture](./00_Click_Capture.ipynb) | Receiving ipyleaflet click events — print, store, and accumulate coordinates |
| 01 | [Point Representation](./01_Point_Representation.ipynb) | The `[lat, lon]` vs `[lon, lat]` coordinate flip — the gotcha that breaks everything silently |
| 02 | [Point in Polygon Basics](./02_Point_In_Polygon_Basics.ipynb) | Polygon structure, closed rings, convex vs. concave intuition, and boundary edge cases; builds `data/regions.geojson` |
| 03 | [Ray Casting Algorithm](./03_Ray_Casting_Algorithm.ipynb) | Odd/even crossing count, the edge loop implementation, and vertex-on-ray handling |
| 04 | [Testing Against Multiple Features](./04_Testing_Against_Multiple_Features.ipynb) | Early exit vs. full scan across a FeatureCollection; bbox pre-filter |
| 05 | [Region Classification](./05_Region_Classification.ipynb) | Properties → meaning: `classify_point()` with structured results and no-match handling |
| 06 | [Interactive Click Applications](./06_Interactive_Click_Applications.ipynb) | Full pipeline assembled — click to classification to highlighted map response |

## Exercises & Check Your Understanding

| Notebook | Exercises | CYU |
|---|---|---|
| [Click Capture](./00_Click_Capture.ipynb) | [A](./00_Click_Capture.ipynb#exercise-a) [B](./00_Click_Capture.ipynb#exercise-b) | [✓](./00_Click_Capture.ipynb#check-your-understanding) |
| [Point Representation](./01_Point_Representation.ipynb) | [A](./01_Point_Representation.ipynb#exercise-a) [B](./01_Point_Representation.ipynb#exercise-b) | [✓](./01_Point_Representation.ipynb#check-your-understanding) |
| [Point In Polygon Basics](./02_Point_In_Polygon_Basics.ipynb) | [A](./02_Point_In_Polygon_Basics.ipynb#exercise-a) [B](./02_Point_In_Polygon_Basics.ipynb#exercise-b) | [✓](./02_Point_In_Polygon_Basics.ipynb#check-your-understanding) |
| [Ray Casting Algorithm](./03_Ray_Casting_Algorithm.ipynb) | [A](./03_Ray_Casting_Algorithm.ipynb#exercise-a) [B](./03_Ray_Casting_Algorithm.ipynb#exercise-b) | [✓](./03_Ray_Casting_Algorithm.ipynb#check-your-understanding) |
| [Testing Against Multiple Features](./04_Testing_Against_Multiple_Features.ipynb) | [A](./04_Testing_Against_Multiple_Features.ipynb#exercise-a) [B](./04_Testing_Against_Multiple_Features.ipynb#exercise-b) | [✓](./04_Testing_Against_Multiple_Features.ipynb#check-your-understanding) |
| [Region Classification](./05_Region_Classification.ipynb) | [A](./05_Region_Classification.ipynb#exercise-a) [B](./05_Region_Classification.ipynb#exercise-b) | [✓](./05_Region_Classification.ipynb#check-your-understanding) |
| [Interactive Click Applications](./06_Interactive_Click_Applications.ipynb) | [A](./06_Interactive_Click_Applications.ipynb#exercise-a) [B](./06_Interactive_Click_Applications.ipynb#exercise-b) | [✓](./06_Interactive_Click_Applications.ipynb#check-your-understanding) |

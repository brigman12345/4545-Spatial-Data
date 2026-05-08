# Module 04 — Spatial Grid Index

Replace the linear feature scan with a grid-based spatial index. Instead of checking every feature on every pan, pre-bucket features into geographic cells and query only the cells the viewport touches.

| # | Notebook | Description |
|---|---|---|
| 00 | [The Grid Idea](./00-The_Grid_Idea.ipynb) | Why O(n) culling has a ceiling; how a grid index changes the query structure |
| 01 | [Building the Index](./01-Building_the_Index.ipynb) | Implement the grid, assign features to cells, visualize the populated structure |
| 02 | [Querying and Benchmarking](./02-Querying_and_Benchmarking.ipynb) | Query the index for a viewport, deduplicate results, and compare speed against linear scan |

## Exercises & Check Your Understanding

| Notebook | Exercises | CYU |
|---|---|---|
| [The Grid Idea](./00-The_Grid_Idea.ipynb) | [A](./00-The_Grid_Idea.ipynb#exercise-a) [B](./00-The_Grid_Idea.ipynb#exercise-b) | [✓](./00-The_Grid_Idea.ipynb#check-your-understanding) |
| [Building the Index](./01-Building_the_Index.ipynb) | [A](./01-Building_the_Index.ipynb#exercise-a) [B](./01-Building_the_Index.ipynb#exercise-b) | [✓](./01-Building_the_Index.ipynb#check-your-understanding) |
| [Querying and Benchmarking](./02-Querying_and_Benchmarking.ipynb) | [A](./02-Querying_and_Benchmarking.ipynb#exercise-a) [B](./02-Querying_and_Benchmarking.ipynb#exercise-b) | [✓](./02-Querying_and_Benchmarking.ipynb#check-your-understanding) |

# Module 10 — Buffers

Converting a point or path into an area of influence: accurate km-radius circles, line corridors, concentric impact zones, and the CRS distortion that breaks naive approaches.

| # | Notebook | Description |
|---|---|---|
| 00 | [Buffer Concepts](./00_Buffer_Concepts.ipynb) | What a buffer is — point → disk, line → corridor — and why degree offsets are wrong |
| 01 | [Buffering Points](./01_Buffering_Points.ipynb) | Accurate circular buffers in kilometers using the destination point formula; builds `data/targets.geojson` |
| 02 | [Buffering Lines](./02-Buffering_Lines.ipynb) | Line corridor buffers via sampled overlapping circles |
| 03 | [Comparing Buffer Sizes](./03-Comparing_Buffer_Sizes.ipynb) | Concentric zone rings, exclusive band area formula, overlapping multi-target buffers |
| 04 | [Buffer Visualization Strategies](./04-Buffer_Visualization_Strategies.ipynb) | Layer order, opacity scaling, and color ramp best practices |
| 05 | [CRS Limitations](./05-CRS_Limitations.ipynb) | Why degree-offset buffers are geometrically incorrect and how distortion grows with latitude |
| 06 | [Applications: Impact Zones](./06-Applications_Impact_Zones.ipynb) | Blast radii, trajectory corridors, containment checks, and combined maps |

## Exercises & Check Your Understanding

| Notebook | Exercises | CYU |
|---|---|---|
| [Buffer Concepts](./00_Buffer_Concepts.ipynb) | [A](./00_Buffer_Concepts.ipynb#exercise-a) [B](./00_Buffer_Concepts.ipynb#exercise-b) | [✓](./00_Buffer_Concepts.ipynb#check-your-understanding) |
| [Buffering Points](./01_Buffering_Points.ipynb) | [A](./01_Buffering_Points.ipynb#exercise-a) [B](./01_Buffering_Points.ipynb#exercise-b) | [✓](./01_Buffering_Points.ipynb#check-your-understanding) |
| [Buffering Lines](./02-Buffering_Lines.ipynb) | [A](./02-Buffering_Lines.ipynb#exercise-a) [B](./02-Buffering_Lines.ipynb#exercise-b) | [✓](./02-Buffering_Lines.ipynb#check-your-understanding) |
| [Comparing Buffer Sizes](./03-Comparing_Buffer_Sizes.ipynb) | [A](./03-Comparing_Buffer_Sizes.ipynb#exercise-a) [B](./03-Comparing_Buffer_Sizes.ipynb#exercise-b) | [✓](./03-Comparing_Buffer_Sizes.ipynb#check-your-understanding) |
| [Buffer Visualization Strategies](./04-Buffer_Visualization_Strategies.ipynb) | [A](./04-Buffer_Visualization_Strategies.ipynb#exercise-a) [B](./04-Buffer_Visualization_Strategies.ipynb#exercise-b) | [✓](./04-Buffer_Visualization_Strategies.ipynb#check-your-understanding) |
| [CRS Limitations](./05-CRS_Limitations.ipynb) | [A](./05-CRS_Limitations.ipynb#exercise-a) [B](./05-CRS_Limitations.ipynb#exercise-b) | [✓](./05-CRS_Limitations.ipynb#check-your-understanding) |
| [Applications Impact Zones](./06-Applications_Impact_Zones.ipynb) | [A](./06-Applications_Impact_Zones.ipynb#exercise-a) [B](./06-Applications_Impact_Zones.ipynb#exercise-b) | [✓](./06-Applications_Impact_Zones.ipynb#check-your-understanding) |


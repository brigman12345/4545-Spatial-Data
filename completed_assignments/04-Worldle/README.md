# Unit 04 — Final Project: Build Your Own Worldle

> **Due:** Friday, May 8, 2026 (last day of classes)
> **Library mandate:** Every piece of spatial math in this project lives in `wdo`. If you catch yourself writing `math.sin` inside your notebook, stop, back away slowly, and move it into a `wdo` module.
> **Stack:** Python, Jupyter, `ipyleaflet`, `ipywidgets`, and your own freshly-promoted `wdo` code.

## What you're building

A web-game-ish recreation of [Worldle](https://worldle.teuteuf.fr/) that runs inside a Jupyter notebook:

1. A mystery country polygon is drawn on an `ipyleaflet` map — no name, no flag, no hints.
2. The player picks a country from a searchable dropdown.
3. After each guess:
   - If it's the correct country: 🎉 (go ahead, make it obnoxious).
   - If not: add a row with the country's flag, its name, a directional arrow pointing _from_ the guess _toward_ the target, and the great-circle distance in km (or miles — your call).
4. Game ends on a correct guess, or when the player gives up. You decide if there's a guess limit.

The spec is small. The craftsmanship bar is not. Style it, sweat the UX, and make it yours. This isn't a web design class so I'm not going to grade your kerning, but a project you're proud to demo is always more fun to build.

## The rules of engagement

- **`wdo` is mandatory.** Distance, bearing, compass, feature centering, guess feedback — all of it comes from `wdo`. Notebook code should look like a director calling shots, not a mathematician sweating trig.
- **Write your own functions first.** For anything not already in `wdo`, draft the function yourself before reaching for Shapely/GeoPy/etc. You can use libraries later for speed or edge cases, but the first cut should be yours.
- **Promote back to the library.** If you write it in a notebook cell and use it twice, promote it into `wdo`. That's the whole point of the package.
- **Your style, your game.** Colors, fonts, layout, emoji policy — your choice. I just don't want 20 identical-looking projects.

## The data you have

- **Country polygons:** `Resources/Data/countries_export.json` — a GeoJSON `FeatureCollection` where each feature has `properties.ADMIN` (country name) and `properties.ISO_A3` (3-letter ISO code). The geometries are `Polygon`s. Most countries, anyway — island chains and some territories show up as `MultiPolygon` in richer datasets, but this one stays mostly polygonal.
- **Flag icons:** `Resources/Data/flag-icons/` — SVG flags named by **ISO-2** lowercase (`af.svg`, `us.svg`, `gb.svg`). There's a `country.json` index with ISO-2 code → name → flag paths. Two aspect ratios: `flags/1x1/` and `flags/4x3/`.

> 🪤 **Gotcha of the year:** your polygons are keyed by ISO-**3** and your flags are keyed by ISO-**2**. You will need a bridge. See Microlesson 2.

## The pieces of `wdo` you'll touch

| Module                     | Status     | What you'll do                                                                       |
| -------------------------- | ---------- | ------------------------------------------------------------------------------------ |
| `wdo.io.geojson_tools`     | ✅ done    | Use it — load countries, iterate features                                            |
| `wdo.geometry.distance`    | ✅ done    | Use `haversine_km` / `haversine_miles`                                               |
| `wdo.geometry.bearing`     | ✅ done    | Use `initial_bearing`, `bearing_to_compass`                                          |
| `wdo.geometry.bbox`        | 🟡 stubbed | **Finish `bbox_from_feature`**                                                       |
| `wdo.maps.leaflet_helpers` | 🟡 stubbed | **Implement `make_map`, `add_geojson`, `fit_map_to_geojson`**                        |
| `wdo.games.worldle`        | 🟡 stubbed | **Implement `choose_target`, `feature_center`, `guess_feedback`, `format_feedback`** |

By the end of this unit, those yellow rows should be green. You're not being asked to build `wdo` from scratch — you're _finishing the parts that make Worldle possible._

---

# The Microlessons

Each microlesson is meant to be a single notebook (or one notebook section) that runs in 15–30 minutes. Do them in order. By the end, you have all the parts; the final assignment is stitching them into one polished notebook.

## Microlesson 1 — Editable ("develop") installs of `wdo`

**Goal:** Get `wdo` importable in any notebook on your machine, and make edits to `wdo` immediately visible without reinstalling.

**What you'll learn:**

- What `pip install -e .` actually does (spoiler: it creates a `.pth` file in `site-packages` pointing at your source folder).
- Why that matters: you can edit `wdo/games/worldle.py` and your notebook sees the change on the next import — no copying files, no republishing.
- The difference between a **regular install** (a frozen snapshot) and an **editable install** (a live link).

**Steps:**

1. Navigate to the `wdo` folder. If it doesn't yet have a `pyproject.toml`, add a minimal one:

   ```toml
   # pyproject.toml
   [project]
   name = "wdo"
   version = "0.1.0"
   requires-python = ">=3.10"

   [build-system]
   requires = ["setuptools>=61"]
   build-backend = "setuptools.build_meta"
   ```

2. From a terminal (in the virtual environment you use for class):

   ```bash
   pip install -e /path/to/Resources/wdo
   ```

3. In a notebook, verify:

   ```python
   import wdo
   print(wdo.__file__)        # Should point INSIDE your wdo source folder
   from wdo.geometry.distance import haversine_km
   print(haversine_km((34.0, -118.0), (40.7, -74.0)))
   ```

4. Open `wdo/geometry/distance.py`, change a docstring, save, and in the notebook run:

   ```python
   %load_ext autoreload
   %autoreload 2
   ```

   Now re-import and confirm your change is picked up. `autoreload` is the magic incantation that makes editable installs feel instantaneous.

**Check yourself:** If `wdo.__file__` points somewhere inside `site-packages` and not your source folder, your install isn't editable. Redo step 2.

---

## Microlesson 2 — Meet the data (and the ISO-2/ISO-3 bridge)

**Goal:** Load the country polygons, the flag index, and build one lookup table that joins them.

**What you'll learn:**

- Using `wdo.io.geojson_tools.load_geojson` and `iter_features`.
- Why real-world spatial data always needs a join table.

**Exercises:**

1. Load `countries_export.json`. Print `feature_count`, `property_names`, and the first feature.
2. Load `flag-icons/country.json`. Find the field names (you're looking for ISO-2 code and a flag path).
3. Build a dict like this:

   ```python
   # iso3 -> { "name": ..., "iso2": ..., "flag_path": ... }
   country_lookup = { ... }
   ```

   There's no clean column named `ISO_A2` in the polygons file — you'll have to match on **country name** (`ADMIN` vs the flag index's `name`). Yes, you'll get misses ("United States" vs "United States of America"). That's the real world. Log the misses, fix the obvious ones by hand, and move on.

**Suggested function to write (and promote to `wdo`):**

```python
def build_country_lookup(countries_geojson, flag_index):
    """Return {iso3: {...}} by joining polygons to flag metadata on country name.

    Unmatched entries are returned with flag_path=None so the game can still use them.
    Misses are printed once so you know which manual aliases to add.
    """
```

Put that in `wdo/games/worldle.py` or a new `wdo/io/country_lookup.py` — your call. (Recommend the latter; it's not game logic, it's data plumbing.)

**Stretch:** add an `aliases` dict (`{"United States": "United States of America", ...}`) that catches the usual suspects.

---

## Microlesson 3 — Draw a country on a map (without spoiling it)

**Goal:** Put one country's polygon on an `ipyleaflet` map — no labels, no popups, no tooltips. Fit the view to the polygon's bounds.

**What you'll learn:**

- `ipyleaflet.Map` basics.
- `ipyleaflet.GeoJSON` with a style dict.
- Why `fit_bounds` matters: a small country on a world view looks like a pixel, and a giant country on a zoomed-in view looks like a wall.

**Steps:**

1. Implement `wdo.maps.leaflet_helpers.make_map`:

   ```python
   def make_map(center=(0, 0), zoom=2, basemap=None, scroll_wheel_zoom=True):
       """Return an ipyleaflet.Map with sensible Worldle defaults."""
   ```

2. Implement `wdo.geometry.bbox.bbox_from_feature`. Suggestion:

   ```python
   def bbox_from_feature(feature):
       """Return (min_lon, min_lat, max_lon, max_lat) for a Polygon or MultiPolygon feature.

       Why we write this ourselves: it's four lines of min/max over the coords, and
       writing it yourself means you understand the GeoJSON nesting:
           Polygon     -> [ [ring] ]         where ring is a list of [lon, lat]
           MultiPolygon-> [ [ [ring] ], ... ]
       Hint: flatten to a list of (lon, lat), then min/max.
       """
   ```

3. Implement a thin `add_geojson(map_obj, data, style=None)` that wraps `ipyleaflet.GeoJSON`, and a `fit_map_to_geojson(map_obj, data)` that uses your `bbox_from_feature(s)` to call `map_obj.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])`.

4. In a notebook, draw Chile. Then Russia. Then Nauru. Your map should handle all three without looking silly.

**A little styling talk (since this isn't a web class):**

`ipyleaflet.GeoJSON(data=..., style={...})` takes an ordinary Python dict. You don't need CSS. You need these keys:

- `color` — outline color (hex or CSS name: `"#1f77b4"` or `"darkred"`).
- `fillColor` — fill color.
- `weight` — outline thickness in pixels.
- `fillOpacity` — 0.0 to 1.0.
- `dashArray` — e.g. `"4,4"` for a dashed outline (optional).

Experiment with two or three palettes until one feels like "your" game. A dark fill on a light basemap reads differently from a bright fill on a dark basemap. Pick one and commit.

---

## Microlesson 4 — Find the middle of a country

**Goal:** Given a country polygon, return a single `(lat, lon)` representative point so we can compute distances and bearings from it.

**What you'll learn:**

- Why "centroid" is harder than it sounds.
- Two approaches, with tradeoffs.

**Approach A — bounding-box center:**

- Fast, trivial: `((min_lat+max_lat)/2, (min_lon+max_lon)/2)`.
- Works well for most countries.
- Fails hilariously for the U.S. (center ends up in Canada if you include Alaska) and Russia (wraps the antimeridian).

**Approach B — mean of boundary vertices:**

- Average of all `(lat, lon)` points in the ring.
- Biased toward areas where vertices are dense.
- Still bad at the antimeridian.

**Approach C — "representative point" (mentioned for context, not required):**

- Libraries like Shapely provide `representative_point()`, which is guaranteed to lie inside the polygon. Worth knowing about, not required to implement.

**Write this:**

```python
def feature_center(feature, method="bbox"):
    """Return a representative (lat, lon) for a Polygon/MultiPolygon feature.

    method="bbox"  -> center of the bounding box (fast, mostly fine)
    method="mean"  -> mean of boundary vertices (alternative; try both)

    Why we expose the method: Worldle judges "direction from your guess to the target."
    If your centers are garbage, your arrows are garbage. Students should eyeball
    their centers on a map before trusting them.
    """
```

Put it in `wdo/games/worldle.py` — the stub is already there waiting for you.

**Sanity-check task:** plot a red dot at each country's center on a world map. Scan for any that fall in the ocean or on the wrong continent. Russia and the U.S. will misbehave. Note it in your write-up; don't try to fix the antimeridian — that's a rabbit hole.

---

## Microlesson 5 — Pick a target country

**Goal:** Randomly choose the country the player has to guess. Reproducibly.

**Write this:**

```python
def choose_target(features, seed=None):
    """Pick one feature at random. If seed is given, the pick is reproducible.

    Why seed matters: when a classmate shares their screenshot, they can send
    the seed too and you can play the same round. Also useful for debugging.
    """
```

Use Python's `random.Random(seed).choice(features)`. One-liner, but document it like you mean it.

**Stretch:** add a `difficulty` parameter that filters to "big countries" (area > threshold) for easy mode or "small countries" for nightmare mode. Computing area from lat/lon is non-trivial — cheat with `bbox` size for a rough proxy.

---

## Microlesson 6 — Judge the guess

**Goal:** Given the guess feature and the target feature, return everything the UI needs:

```python
{
    "correct": False,
    "distance_km": 8742.1,
    "distance_miles": 5432.7,
    "bearing_deg": 47.3,
    "compass": "NE",
    "arrow": "↗",
}
```

**What you'll learn:**

- Composing existing `wdo` functions instead of duplicating them.
- How bearings translate to arrow glyphs.

**Write this:**

```python
def guess_feedback(guess_feature, target_feature):
    """Compare a guess to the target and return a dict with distance, bearing, compass, arrow.

    Uses wdo.geometry.distance.haversine_km, wdo.geometry.bearing.initial_bearing,
    and wdo.geometry.bearing.bearing_to_compass. The arrow is a Unicode glyph
    that corresponds to the compass label (see ARROWS below).
    """

ARROWS = {
    "N": "↑", "NE": "↗", "E": "→", "SE": "↘",
    "S": "↓", "SW": "↙", "W": "←", "NW": "↖",
}
```

**Key design decision to make:** the bearing goes _from the guess to the target_. So if the player guesses Brazil and the target is France, the arrow should point roughly NE ("go this way to find it"). Double-check the direction by picking two countries you know the relationship of and reading the arrow. Nothing is more embarrassing than shipping a game where every arrow is backwards.

**Also write:**

```python
def format_feedback(result, units="km"):
    """Plain-text version of the feedback, useful for logging and testing before the UI lands."""
```

---

## Microlesson 7 — Render one guess row (flag, name, arrow, distance)

**Goal:** Produce an HTML snippet that shows: 🇫🇷 `France` `↗` `8,742 km`.

**What you'll learn:**

- `ipywidgets.HTML` is your friend. You write HTML as a Python string; it renders.
- How to embed an SVG flag from disk.

**Two ways to include the flag:**

1. **File path (simplest):** `<img src="flag-icons/flags/4x3/fr.svg" width="36">` — works if the notebook is next to the flags folder.
2. **Data URI (portable):** base64-encode the SVG file and inline it as `<img src="data:image/svg+xml;base64,...">`. Works even if the notebook moves. Slightly more code, zero broken-image surprises.

**Write this:**

```python
def render_guess_row(country_name, flag_path, arrow, distance_km):
    """Return an HTML string for one row of the guess history."""
```

Keep the row structure consistent so the history reads like a table. Your friends should be able to skim "oh, I've been drifting north, I should guess further south" in three seconds.

**Style pointers (remember: HTML, not CSS files):**

- Use inline `style="..."` attributes: `<div style="display:flex;align-items:center;gap:8px">...</div>`.
- A `<table>` works too, and honestly for rows of identical data a table is fine.
- Keep font-families to system stacks unless you want to wrestle with `@font-face`: `font-family: -apple-system, system-ui, sans-serif;`.
- Use emoji sparingly — one per row is a garnish; five is a cry for help.

---

## Microlesson 8 — Wire up the UI (dropdown + history + map)

**Goal:** One notebook cell creates the whole game: a map on top, a country dropdown below, a "Guess" button, and a growing list of guess rows.

**What you'll learn:**

- `ipywidgets` composition: `VBox`, `HBox`, `Dropdown`/`Combobox`, `Button`, `HTML`, `Output`.
- Observer pattern: `button.on_click(handler)`.
- Keeping state in a plain Python object so it's inspectable.

**Recommended widgets:**

- **`Combobox`** (from `ipywidgets`) — like `Dropdown` but with type-ahead search. With ~200 countries, this is the difference between "fun" and "tedious."
- **`Output`** widget — renders anything you `display(...)` inside it. Perfect home for the growing guess history.
- **`Button`** — "Guess," "Give up," "New game."

**Suggested game state:**

```python
class WorldleGame:
    def __init__(self, features, seed=None, max_guesses=6):
        self.features = features
        self.target = choose_target(features, seed=seed)
        self.guesses = []
        self.max_guesses = max_guesses
        self.finished = False

    def submit_guess(self, guess_iso3):
        ...  # returns a feedback dict; marks finished on correct or out of guesses
```

Keeping state in an object (not scattered globals) makes it easy to test, to replay, and to add features like "Share this game."

**Handler sketch:**

```python
def on_guess_click(_):
    if game.finished: return
    iso3 = combobox.value_to_iso3(...)  # however you wire it up
    fb = game.submit_guess(iso3)
    with history_output:
        display(HTML(render_guess_row(..., fb)))
    if fb["correct"]:
        with banner_output:
            display(HTML("<h2 style='color:#2a9d8f'>You got it!</h2>"))
```

---

## Microlesson 9 — Polish (strongly suggested)

Pick at least two of these. They're what separate a passing project from a memorable one.

- **Proximity coloring.** Color the distance green when close, yellow at medium, red when far. Use a threshold scheme (e.g., <500 km green, <2,000 km yellow, else red). One if/elif/else, huge UX payoff.
- **Proximity emoji.** Closer-to-target = warmer emoji (🔥 close, 🌡️ medium, 🧊 cold). Same threshold logic as above.
- **Guess limit.** Six guesses, Wordle-style. Reveal the country on loss.
- **Reveal the polygon on the world map** at game end, so the player sees where they _actually_ were.
- **Shareable result string.** Build a text version of the guess history, copy-to-clipboard-friendly. Minus the flags, plus emoji — you know the vibe.
- **Keyboard enter-to-guess.** `combobox.on_submit(handler)` in addition to the button.
- **Difficulty selector.** Tiny-country mode, continent-restricted mode, etc.
- **Per-region basemap.** Light basemap for bright country fills; dark basemap for glowing outlines. Let the player toggle.

Pick the ones that _fit the game you want to make._ If your vibe is minimalist, don't add emoji. If you want it loud, go loud.

---

# The Final Deliverable

## What to submit

1. **One notebook** (`worldle.ipynb`) that, when you Run All, produces a playable game.
2. **Your updated `wdo` package** — with the functions from Microlessons 2–6 implemented and committed.
3. **A short README** (or top-of-notebook markdown cell) describing:
   - Which `wdo` functions you added or finished.
   - Any aliases/hacks you added to the country-name join.
   - Known bugs (be honest — credit for documenting > credit for hiding).
   - One screenshot of a completed round.

## Rubric (100 pts)

| Area                                   | Points | What earns full marks                                                                                                                                          |
| -------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Core gameplay works**                | 30     | Mystery country draws, dropdown selects, each guess produces flag + name + arrow + distance, win condition triggers.                                           |
| **wdo implementations**                | 25     | `feature_center`, `choose_target`, `guess_feedback`, `format_feedback`, `bbox_from_feature` implemented correctly. No spatial math duplicated in the notebook. |
| **Editable install + reproducibility** | 10     | Notebook imports `wdo` via an editable install; a second student could clone and run. Seed-able targets.                                                       |
| **Own style & polish**                 | 15     | The game looks and feels like yours. At least two polish items from Microlesson 9. Reasonable layout.                                                          |
| **Code quality**                       | 10     | Functions have docstrings. No giant cells. State isn't just loose globals.                                                                                     |
| **Write-up & honesty**                 | 10     | README covers what you did, known gaps, and a screenshot.                                                                                                      |

## Grad-student (5993) add-on

Pick one of:

- **Non-polygon centers that make sense.** Implement a "representative point" approach that guarantees the center is _inside_ the polygon (not just bbox center). Compare results on the US/Russia/Chile against the naive methods.
- **Area-aware difficulty.** Compute an approximate area for each polygon (spherical excess, or projected) and build three difficulty tiers. Justify your thresholds.
- **Fuzzy country-name joining.** Replace the manual alias dict with a fuzzy matcher (`rapidfuzz` or your own Levenshtein) and report precision on the country join.

---

# Suggested timeline

This is 9 microlessons plus the final integration. Given the May 8 due date and that we have about three weeks:

- **Week 1 (now):** Microlessons 1–4. You should be able to draw any country on an `ipyleaflet` map with a red dot at its center.
- **Week 2:** Microlessons 5–7. You should have a working `guess_feedback` and a rendered guess row — even if there's no UI around it yet.
- **Week 3:** Microlesson 8 + polish from Microlesson 9 + write-up.

That leaves the last few days for the stuff that always surprises you: the `ipywidgets` callback that doesn't fire, the flag that's a broken-image icon, the country whose name is spelled differently in one dataset.

---

# A few closing reminders

- **When in doubt, promote.** If you wrote a helper in your notebook and used it twice, move it to `wdo`.
- **Don't debug in your head.** `print(fb)` or `display(fb)` the feedback dict before worrying about HTML rendering.
- **Eyeball your centers.** Half the "my arrow is wrong" bugs are actually "my center is wrong."
- **Have fun with it.** This should feel more like a project than a problem set. If it doesn't, come talk to me.

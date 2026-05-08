def build_expected_tree(paths: list[str], base: Path) -> dict:
    """Build a nested dict from flat path list. Leaves are True (found) / False (missing)."""
    tree = {}
    for p in paths:
        parts = Path(p).parts
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (base / p).exists()
    return tree


def render_expected_tree(node: dict, prefix: str = "", lines: list = None) -> list[str]:
    if lines is None:
        lines = []
    keys = sorted(node.keys(), key=lambda k: (isinstance(node[k], dict), k.lower()))
    for i, key in enumerate(keys):
        connector = "└── " if i == len(keys) - 1 else "├── "
        value = node[key]
        if isinstance(value, dict):
            lines.append(prefix + connector + key + "/")
            extension = "    " if i == len(keys) - 1 else "│   "
            render_expected_tree(value, prefix + extension, lines)
        else:
            marker = "✅" if value else "❌"
            lines.append(prefix + connector + marker + " " + key)
    return lines


# ---------------------------------------------------------------------------
# Actual tree rendering
# ---------------------------------------------------------------------------


def render_actual_tree(path: Path, prefix: str = "", lines: list = None) -> list[str]:
    if lines is None:
        lines = []
    items = [
        p
        for p in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        if p.name not in IGNORE_DIRS and not p.name.startswith(".")
    ]
    for i, item in enumerate(items):
        connector = "└── " if i == len(items) - 1 else "├── "
        lines.append(prefix + connector + item.name)
        if item.is_dir():
            extension = "    " if i == len(items) - 1 else "│   "
            render_actual_tree(item, prefix + extension, lines)
    return lines


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def section_stats(paths: list[str], base: Path) -> dict[str, tuple[int, int]]:
    stats: dict[str, list] = {}
    for p in paths:
        section = Path(p).parts[0]
        stats.setdefault(section, [0, 0])
        stats[section][1] += 1
        if (base / p).exists():
            stats[section][0] += 1
    return {k: tuple(v) for k, v in stats.items()}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def emit(lines_buf: list, text: str = "") -> None:
    """Print a line and collect it for the output file."""
    print(text)
    lines_buf.append(text)


def main():
    root = Path.cwd()
    completed = root / "completed_assignments"

    if not completed.exists():
        print()
        print("  ERROR: 'completed_assignments/' folder not found.")
        print("  Create it in your repo root and place your notebooks inside.")
        print()
        return

    buf: list[str] = []

    # ── Expected tree ────────────────────────────────────────────────────────
    emit(buf)
    emit(buf, "=" * 60)
    emit(buf, "  EXPECTED STRUCTURE")
    emit(buf, "  (✅ = found in your completed_assignments/  ❌ = missing)")
    emit(buf, "=" * 60)
    emit(buf)
    emit(buf, "completed_assignments/")
    tree = build_expected_tree(EXPECTED, completed)
    for line in render_expected_tree(tree):
        emit(buf, line)

    # ── Actual tree ──────────────────────────────────────────────────────────
    emit(buf)
    emit(buf, "=" * 60)
    emit(buf, "  YOUR completed_assignments/ TREE")
    emit(buf, "=" * 60)
    emit(buf)
    emit(buf, "completed_assignments/")
    actual_lines = render_actual_tree(completed)
    if actual_lines:
        for line in actual_lines:
            emit(buf, line)
    else:
        emit(buf, "  (empty)")

    # ── Summary ──────────────────────────────────────────────────────────────
    emit(buf)
    emit(buf, "=" * 60)
    emit(buf, "  SUMMARY")
    emit(buf, "=" * 60)
    emit(buf)
    stats = section_stats(EXPECTED, completed)
    total_found = total_expected = 0
    for section, (found, expected) in stats.items():
        note = SECTION_NOTES.get(section, "")
        bar = "█" * found + "░" * (expected - found)
        emit(buf, f"  {section}")
        emit(buf, f"    {found}/{expected}  [{bar}]")
        if note:
            emit(buf, f"    Goal: {note}")
        emit(buf)
        total_found += found
        total_expected += expected

    emit(buf, f"  Total: {total_found}/{total_expected} notebooks found")
    emit(buf)

    # ── Self-reported progress score placeholder ─────────────────────────────
    score_section = [
        "",
        "=" * 60,
        "  SELF-REPORTED PROGRESS SCORE",
        "  Edit this file and replace the line below with your score.",
        "  Use a number from 0 to 10, where 10 = 100% complete.",
        "=" * 60,
        "",
        "  Score: __ / 10",
        "",
    ]
    for line in score_section:
        buf.append(line)

    # ── Write progress_checklist.txt ─────────────────────────────────────────
    out_path = root / "progress_checklist.txt"
    out_path.write_text("\n".join(buf) + "\n", encoding="utf-8")
    print()
    print(f"  Saved: {out_path}")
    print("  Open that file and replace '__ / 10' with your score before submitting.")
    print()


if __name__ == "__main__":
    main()

import random
from core.models.question_model import Question


_UNITS_HINT = "Write your answer with units — type cm2 for cm², m2 for m², etc."


def _norm(s: str) -> str:
    return s.strip().lower().replace("²", "2").replace("^2", "2").replace(" ", "")


def _fmt(value: float, unit: str) -> str:
    v = int(value) if value == int(value) else round(value, 4)
    return f"{v} {unit}²"


# ── SVG helpers ──────────────────────────────────────────────────────────────

def _svg_square(side_label: str) -> str:
    S = 150
    pl, pt, pr, pb = 50, 20, 50, 60
    W = pl + S + pr
    H = pt + S + pb
    cx = pl + S / 2
    cy = pt + S / 2
    t = 9  # tick half-length
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
        f'<rect x="{pl}" y="{pt}" width="{S}" height="{S}" fill="#dbeafe" stroke="#1e293b" stroke-width="2.5"/>'
        # tick marks on all four sides (= equal lengths)
        f'<line x1="{cx}" y1="{pt-t}" x2="{cx}" y2="{pt+t}" stroke="#475569" stroke-width="2.5"/>'
        f'<line x1="{cx}" y1="{pt+S-t}" x2="{cx}" y2="{pt+S+t}" stroke="#475569" stroke-width="2.5"/>'
        f'<line x1="{pl-t}" y1="{cy}" x2="{pl+t}" y2="{cy}" stroke="#475569" stroke-width="2.5"/>'
        f'<line x1="{pl+S-t}" y1="{cy}" x2="{pl+S+t}" y2="{cy}" stroke="#475569" stroke-width="2.5"/>'
        f'<text x="{cx}" y="{pt+S+46}" text-anchor="middle"'
        f' font-family="Arial,sans-serif" font-size="16" fill="#b91c1c" font-weight="bold">{side_label}</text>'
        f'</svg>'
    )


def _svg_rect(w_label: str, h_label: str, w_val: float, h_val: float) -> str:
    max_px, min_px = 155, 65
    ratio = w_val / h_val
    if ratio >= 1:
        pw = max_px
        ph = int(max(min_px, round(max_px / ratio)))
    else:
        ph = max_px
        pw = int(max(min_px, round(max_px * ratio)))

    pl, pt, pr, pb = 45, 20, 70, 60
    W = pl + pw + pr
    H = pt + ph + pb
    cx = pl + pw / 2
    cy = pt + ph / 2
    rx = pl + pw + 54

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
        f'<rect x="{pl}" y="{pt}" width="{pw}" height="{ph}" fill="#dbeafe" stroke="#1e293b" stroke-width="2.5"/>'
        f'<text x="{cx}" y="{pt+ph+46}" text-anchor="middle"'
        f' font-family="Arial,sans-serif" font-size="16" fill="#b91c1c" font-weight="bold">{w_label}</text>'
        f'<text x="{rx}" y="{cy}" text-anchor="middle"'
        f' transform="rotate(-90 {rx} {cy})"'
        f' font-family="Arial,sans-serif" font-size="16" fill="#b91c1c" font-weight="bold">{h_label}</text>'
        f'</svg>'
    )


def _svg_triangle(base_label: str, height_label: str, b_val: float, h_val: float) -> str:
    """Right-angled triangle — right angle at bottom-left, base horizontal, height vertical."""
    max_px, min_px = 155, 65
    ratio = b_val / h_val
    if ratio >= 1:
        pb = max_px
        ph = int(max(min_px, round(max_px / ratio)))
    else:
        ph = max_px
        pb = int(max(min_px, round(max_px * ratio)))

    pl, pt, pr, pbo = 70, 20, 45, 60
    W = pl + pb + pr
    H = pt + ph + pbo

    x0, y0 = pl, pt + ph        # bottom-left (right angle)
    x1, y1 = pl + pb, pt + ph   # bottom-right
    x2, y2 = pl, pt             # top-left

    sq = 12
    base_cx = pl + pb / 2
    lx = pl - 52
    ly = pt + ph / 2

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
        f'<polygon points="{x0},{y0} {x1},{y1} {x2},{y2}" fill="#dcfce7" stroke="#1e293b" stroke-width="2.5"/>'
        # right-angle marker
        f'<polyline points="{x0+sq},{y0} {x0+sq},{y0-sq} {x0},{y0-sq}" fill="none" stroke="#1e293b" stroke-width="2"/>'
        # base label
        f'<text x="{base_cx}" y="{y0+44}" text-anchor="middle"'
        f' font-family="Arial,sans-serif" font-size="16" fill="#b91c1c" font-weight="bold">{base_label}</text>'
        # height label (rotated, left side)
        f'<text x="{lx}" y="{ly}" text-anchor="middle"'
        f' transform="rotate(-90 {lx} {ly})"'
        f' font-family="Arial,sans-serif" font-size="16" fill="#b91c1c" font-weight="bold">{height_label}</text>'
        f'</svg>'
    )


# ── Level generators ──────────────────────────────────────────────────────────

def _level1() -> Question:
    unit = random.choice(["mm", "cm", "m"])
    is_square = random.choice([True, False])

    if is_square:
        side = random.randint(2, 20)
        area = side * side
        ans = _fmt(area, unit)
        return Question(
            question_text=f"Find the area of this square.\n\n{_UNITS_HINT}",
            correct_answer=ans,
            topic="area",
            level=1,
            scaffold_steps=[
                {"prompt": f"Area = side × side = {side} × {side} = ?", "answer": area}
            ],
            worked_solution=[
                "Area = side × side",
                f"Area = {side} {unit} × {side} {unit}",
                f"Area = {ans}",
            ],
            metadata={
                "svg": _svg_square(f"{side} {unit}"),
                "accepted_answers": [_norm(ans)],
            },
        )
    else:
        w = random.randint(2, 20)
        h = random.randint(2, 20)
        while h == w:
            h = random.randint(2, 20)
        area = w * h
        ans = _fmt(area, unit)
        return Question(
            question_text=f"Find the area of this rectangle.\n\n{_UNITS_HINT}",
            correct_answer=ans,
            topic="area",
            level=1,
            scaffold_steps=[
                {"prompt": f"Area = length × width = {w} × {h} = ?", "answer": area}
            ],
            worked_solution=[
                "Area = length × width",
                f"Area = {w} {unit} × {h} {unit}",
                f"Area = {ans}",
            ],
            metadata={
                "svg": _svg_rect(f"{w} {unit}", f"{h} {unit}", w, h),
                "accepted_answers": [_norm(ans)],
            },
        )


def _level2() -> Question:
    """Rectangle with sides in two different units."""
    # (small_unit, large_unit, factor)  — factor small units = 1 large unit
    small_u, large_u, factor = random.choice([
        ("mm", "cm", 10),
        ("cm", "m", 100),
    ])

    if small_u == "mm":
        w = random.randint(2, 15)           # cm
        h_small = random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # mm
    else:
        w = random.randint(2, 9)            # m
        h_small = random.choice([100, 200, 300, 400, 500])  # cm

    h_large = h_small / factor
    area_large = w * h_large
    area_small = (w * factor) * h_small

    ans_large = _fmt(area_large, large_u)
    ans_small = _fmt(area_small, small_u)

    svg = _svg_rect(f"{w} {large_u}", f"{h_small} {small_u}", w, h_large)

    return Question(
        question_text=(
            f"Find the area of this rectangle.\n\n"
            f"The sides are in different units — convert first.\n"
            f"{_UNITS_HINT}"
        ),
        correct_answer=ans_large,
        topic="area",
        level=2,
        scaffold_steps=[
            {
                "prompt": f"Convert {h_small} {small_u} to {large_u} (÷ {factor}):",
                "answer": h_large,
            },
            {
                "prompt": f"Area = {w} {large_u} × {h_large} {large_u} = ?",
                "answer": area_large,
            },
        ],
        worked_solution=[
            f"Convert {h_small} {small_u} → {h_large} {large_u}",
            f"Area = {w} {large_u} × {h_large} {large_u}",
            f"Area = {ans_large}",
            f"Also accepted: {ans_small}",
        ],
        metadata={
            "svg": svg,
            "accepted_answers": [_norm(ans_large), _norm(ans_small)],
        },
    )


def _level3() -> Question:
    """Right-angled triangle, same unit throughout."""
    unit = random.choice(["mm", "cm", "m"])
    base = random.randrange(2, 22, 2)   # even so ½ × base is always integer
    height = random.randint(2, 20)
    area = base * height // 2           # integer guaranteed

    ans = _fmt(area, unit)
    return Question(
        question_text=f"Find the area of this triangle.\n\n{_UNITS_HINT}",
        correct_answer=ans,
        topic="area",
        level=3,
        scaffold_steps=[
            {"prompt": f"base × height = {base} × {height} = ?", "answer": base * height},
            {"prompt": f"Area = ½ × {base * height} = ?", "answer": area},
        ],
        worked_solution=[
            "Area = ½ × base × height",
            f"Area = ½ × {base} {unit} × {height} {unit}",
            f"Area = {ans}",
        ],
        metadata={
            "svg": _svg_triangle(f"{base} {unit}", f"{height} {unit}", base, height),
            "accepted_answers": [_norm(ans)],
        },
    )


def _level4() -> Question:
    """Right-angled triangle with base and height in different units."""
    small_u, large_u, factor = random.choice([
        ("mm", "cm", 10),
        ("cm", "m", 100),
    ])

    if small_u == "mm":
        base = random.randrange(2, 16, 2)           # even cm
        h_small = random.choice([20, 40, 60, 80, 100])  # mm (multiples of 20)
    else:
        base = random.randrange(2, 10, 2)           # even m
        h_small = random.choice([100, 200, 300, 400])   # cm

    h_large = h_small / factor
    area_large = int(base * h_large / 2)    # integer guaranteed (even base, integer h_large)
    area_small = int((base * factor) * h_small / 2)

    ans_large = _fmt(area_large, large_u)
    ans_small = _fmt(area_small, small_u)

    svg = _svg_triangle(f"{base} {large_u}", f"{h_small} {small_u}", base, h_large)

    return Question(
        question_text=(
            f"Find the area of this triangle.\n\n"
            f"The sides are in different units — convert first.\n"
            f"{_UNITS_HINT}"
        ),
        correct_answer=ans_large,
        topic="area",
        level=4,
        scaffold_steps=[
            {
                "prompt": f"Convert {h_small} {small_u} to {large_u} (÷ {factor}):",
                "answer": h_large,
            },
            {
                "prompt": f"base × height = {base} × {h_large} = ?",
                "answer": base * h_large,
            },
            {
                "prompt": f"Area = ½ × {int(base * h_large)} = ?",
                "answer": area_large,
            },
        ],
        worked_solution=[
            f"Convert {h_small} {small_u} → {h_large} {large_u}",
            f"Area = ½ × {base} {large_u} × {h_large} {large_u}",
            f"Area = {ans_large}",
            f"Also accepted: {ans_small}",
        ],
        metadata={
            "svg": svg,
            "accepted_answers": [_norm(ans_large), _norm(ans_small)],
        },
    )


def generate_area_question(level: int) -> Question:
    return {1: _level1, 2: _level2, 3: _level3, 4: _level4}[level]()

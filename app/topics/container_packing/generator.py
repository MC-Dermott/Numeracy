import random
from core.models.question_model import Question


examples_map = {
    1: [
        "Level 1 Example (1D packing with unit conversion):",
        "A shelf is 2 m long. Each book is 25 cm wide.",
        "Convert: 2 m = 200 cm",
        "200 ÷ 25 = 8",
        "Answer = 8 books"
    ],
    2: [
        "Level 2 Example (Choose best orientation):",
        "A box is 15 cm × 25 cm. Shelf is 300 cm long.",
        "Using 15 cm side: 300 ÷ 15 = 20 boxes",
        "Using 25 cm side: 300 ÷ 25 = 12 boxes",
        "Maximum = 20 boxes"
    ],
    3: [
        "Level 3 Example (Tiles on a 2D surface):",
        "Tiles are 20 cm × 20 cm. Floor is 160 cm × 120 cm.",
        "160 ÷ 20 = 8 columns",
        "120 ÷ 20 = 6 rows",
        "8 × 6 = 48 tiles"
    ],
    4: [
        "Level 4 Example (Cubes in a 3D volume):",
        "Cube side = 10 cm. Box = 60 cm × 40 cm × 30 cm.",
        "60 ÷ 10 = 6,  40 ÷ 10 = 4,  30 ÷ 10 = 3",
        "6 × 4 × 3 = 72 cubes"
    ]
}


# ─────────────────────────────────────────
# LEVEL 1: 1D packing with mixed units
# ─────────────────────────────────────────

def _level1_same_unit():
    shelf_options = [60, 80, 100, 120, 150, 180, 200, 240, 300]
    shelf_cm = random.choice(shelf_options)
    divisors = [s for s in [5, 8, 10, 12, 15, 20, 25, 30]
                if shelf_cm % s == 0 and shelf_cm // s >= 3]
    if not divisors:
        divisors = [10]
    obj_cm = random.choice(divisors)
    n_fit = shelf_cm // obj_cm

    obj_pl = random.choice(["books", "tiles", "boxes", "bricks"])
    obj_sg = obj_pl[:-1]
    container = random.choice(["shelf", "table", "bench", "counter"])

    scaffold_steps = [
        {"prompt": f"Divide {shelf_cm} cm by {obj_cm} cm", "answer": n_fit}
    ]
    worked_solution = [
        f"{shelf_cm} ÷ {obj_cm} = {n_fit}",
        f"Answer = {n_fit} {obj_pl}"
    ]
    question_text = (
        f"A {container} is {shelf_cm} cm long. "
        f"Each {obj_sg} is {obj_cm} cm wide. "
        f"How many {obj_pl} fit along the {container}?"
    )
    return question_text, n_fit, scaffold_steps, worked_solution


def _level1_m_to_cm():
    shelf_m_choices = [1, 1.5, 2, 2.5, 3, 4]
    shelf_m = random.choice(shelf_m_choices)
    shelf_cm = int(shelf_m * 100)
    divisors = [s for s in [10, 15, 20, 25, 30, 40, 50]
                if shelf_cm % s == 0 and shelf_cm // s >= 3]
    if not divisors:
        divisors = [10]
    obj_cm = random.choice(divisors)
    n_fit = shelf_cm // obj_cm

    obj_pl = random.choice(["books", "tiles", "boxes", "bricks"])
    obj_sg = obj_pl[:-1]
    container = random.choice(["shelf", "table", "bench", "counter"])
    shelf_m_str = f"{shelf_m:g}"

    scaffold_steps = [
        {"prompt": f"Convert {shelf_m_str} m to cm (multiply by 100)", "answer": shelf_cm},
        {"prompt": f"Divide {shelf_cm} cm by {obj_cm} cm", "answer": n_fit}
    ]
    worked_solution = [
        f"{shelf_m_str} m = {shelf_cm} cm",
        f"{shelf_cm} ÷ {obj_cm} = {n_fit}",
        f"Answer = {n_fit} {obj_pl}"
    ]
    question_text = (
        f"A {container} is {shelf_m_str} m long. "
        f"Each {obj_sg} is {obj_cm} cm wide. "
        f"How many {obj_pl} fit along the {container}?"
    )
    return question_text, n_fit, scaffold_steps, worked_solution


def _level1_cm_to_mm():
    shelf_cm_choices = [60, 80, 100, 120, 150, 160, 200]
    shelf_cm = random.choice(shelf_cm_choices)
    shelf_mm = shelf_cm * 10
    divisors = [s for s in [50, 60, 80, 100, 120, 125, 150, 160, 200, 250]
                if shelf_mm % s == 0 and shelf_mm // s >= 3]
    if not divisors:
        divisors = [100]
    obj_mm = random.choice(divisors)
    n_fit = shelf_mm // obj_mm

    obj_pl = random.choice(["tiles", "bricks", "stickers", "blocks"])
    obj_sg = obj_pl[:-1] if obj_pl != "stickers" else "sticker"
    container = random.choice(["shelf", "strip", "row", "surface"])

    scaffold_steps = [
        {"prompt": f"Convert {shelf_cm} cm to mm (multiply by 10)", "answer": shelf_mm},
        {"prompt": f"Divide {shelf_mm} mm by {obj_mm} mm", "answer": n_fit}
    ]
    worked_solution = [
        f"{shelf_cm} cm = {shelf_mm} mm",
        f"{shelf_mm} ÷ {obj_mm} = {n_fit}",
        f"Answer = {n_fit} {obj_pl}"
    ]
    question_text = (
        f"A {container} is {shelf_cm} cm long. "
        f"Each {obj_sg} is {obj_mm} mm wide. "
        f"How many {obj_pl} fit along the {container}?"
    )
    return question_text, n_fit, scaffold_steps, worked_solution


def generate_level1_question(level):
    mode = random.choice(["same", "m_to_cm", "cm_to_mm"])
    if mode == "m_to_cm":
        q, ans, scaffold, solution = _level1_m_to_cm()
    elif mode == "cm_to_mm":
        q, ans, scaffold, solution = _level1_cm_to_mm()
    else:
        q, ans, scaffold, solution = _level1_same_unit()

    return Question(
        question_text=q,
        correct_answer=str(ans),
        topic="container_packing",
        level=level,
        scaffold_steps=scaffold,
        worked_solution=solution,
        examples=examples_map[1],
        videos=[]
    )


# ─────────────────────────────────────────
# LEVEL 2: Best orientation along 1D line
# ─────────────────────────────────────────

_L2_SCENARIOS = [
    (120, 8, 15), (120, 10, 12),
    (150, 10, 25), (150, 15, 25),
    (180, 9, 12), (180, 12, 15),
    (200, 8, 25), (200, 10, 25),
    (240, 8, 12), (240, 12, 15), (240, 16, 24),
    (300, 12, 15), (300, 15, 20), (300, 20, 25),
]

_L2_OBJECTS = [
    ("cereal box", "cereal boxes"),
    ("book",       "books"),
    ("storage box","storage boxes"),
    ("brick",      "bricks"),
    ("box",        "boxes"),
    ("tin",        "tins"),
]


def generate_level2_question(level):
    length_cm, dim1, dim2 = random.choice(_L2_SCENARIOS)
    small, large = min(dim1, dim2), max(dim1, dim2)
    n_small = length_cm // small
    n_large = length_cm // large
    answer = n_small

    obj_sg, obj_pl = random.choice(_L2_OBJECTS)
    container = random.choice(["shelf", "counter", "table", "workbench"])

    scaffold_steps = [
        {"prompt": f"How many {obj_pl} fit if you line up the {small} cm side?",  "answer": n_small},
        {"prompt": f"How many {obj_pl} fit if you line up the {large} cm side?",  "answer": n_large},
    ]
    worked_solution = [
        f"Using {small} cm side: {length_cm} ÷ {small} = {n_small} {obj_pl}",
        f"Using {large} cm side: {length_cm} ÷ {large} = {n_large} {obj_pl}",
        f"Maximum = {answer} {obj_pl}"
    ]
    question_text = (
        f"A {obj_sg} measures {small} cm × {large} cm. "
        f"A {container} is {length_cm} cm long. "
        f"What is the maximum number of {obj_pl} that can fit in a single row along the {container}?"
    )

    return Question(
        question_text=question_text,
        correct_answer=str(answer),
        topic="container_packing",
        level=level,
        scaffold_steps=scaffold_steps,
        worked_solution=worked_solution,
        examples=examples_map[2],
        videos=[]
    )


# ─────────────────────────────────────────
# LEVEL 3: Square tiles on a 2D surface
# ─────────────────────────────────────────

_L3_SCENARIOS = [
    (120, 80,  20),
    (150, 100, 25),
    (160, 120, 20),
    (180, 120, 30),
    (200, 150, 25),
    (240, 160, 20),
    (240, 180, 30),
    (300, 200, 25),
    (160, 80,  40),
    (200, 100, 20),
    (210, 150, 30),
    (280, 200, 40),
]

_L3_CONTEXTS = [
    ("floor",   "square tile",    "square tiles"),
    ("wall",    "square tile",    "square tiles"),
    ("table",   "square coaster", "square coasters"),
    ("tray",    "square block",   "square blocks"),
    ("surface", "square mat",     "square mats"),
]


def generate_level3_question(level):
    width_cm, height_cm, tile_cm = random.choice(_L3_SCENARIOS)
    cols = width_cm  // tile_cm
    rows = height_cm // tile_cm
    answer = cols * rows

    surface, tile_sg, tile_pl = random.choice(_L3_CONTEXTS)

    scaffold_steps = [
        {"prompt": f"How many {tile_pl} fit along the {width_cm} cm side?",  "answer": cols},
        {"prompt": f"How many {tile_pl} fit along the {height_cm} cm side?", "answer": rows},
    ]
    worked_solution = [
        f"{width_cm} ÷ {tile_cm} = {cols} (columns)",
        f"{height_cm} ÷ {tile_cm} = {rows} (rows)",
        f"{cols} × {rows} = {answer} {tile_pl}"
    ]
    question_text = (
        f"A {surface} measures {width_cm} cm × {height_cm} cm. "
        f"How many {tile_cm} cm × {tile_cm} cm {tile_pl} are needed to cover it completely?"
    )

    return Question(
        question_text=question_text,
        correct_answer=str(answer),
        topic="container_packing",
        level=level,
        scaffold_steps=scaffold_steps,
        worked_solution=worked_solution,
        examples=examples_map[3],
        videos=[]
    )


# ─────────────────────────────────────────
# LEVEL 4: Cubes packed into a 3D volume
# ─────────────────────────────────────────

_L4_SCENARIOS = [
    (60,  40, 30, 10),
    (80,  60, 40, 20),
    (100, 60, 40, 20),
    (60,  30, 20, 10),
    (90,  60, 30, 30),
    (120, 90, 60, 30),
    (100, 80, 60, 20),
    (80,  40, 20, 10),
    (60,  45, 30, 15),
    (120, 60, 40, 20),
    (50,  40, 30, 10),
    (60,  60, 40, 20),
]

_L4_CONTEXTS = [
    ("storage box", "cubes"),
    ("crate",       "cubes"),
    ("container",   "cube-shaped blocks"),
    ("box",         "cube-shaped parcels"),
    ("cabinet",     "cube boxes"),
]


def generate_level4_question(level):
    L, W, H, cube = random.choice(_L4_SCENARIOS)
    n_L = L // cube
    n_W = W // cube
    n_H = H // cube
    answer = n_L * n_W * n_H

    container, obj = random.choice(_L4_CONTEXTS)

    scaffold_steps = [
        {"prompt": f"How many {obj} fit along the {L} cm length?", "answer": n_L},
        {"prompt": f"How many {obj} fit along the {W} cm width?",  "answer": n_W},
        {"prompt": f"How many {obj} fit along the {H} cm height?", "answer": n_H},
    ]
    worked_solution = [
        f"Length: {L} ÷ {cube} = {n_L}",
        f"Width:  {W} ÷ {cube} = {n_W}",
        f"Height: {H} ÷ {cube} = {n_H}",
        f"{n_L} × {n_W} × {n_H} = {answer} {obj}"
    ]
    question_text = (
        f"A {container} measures {L} cm × {W} cm × {H} cm. "
        f"How many {cube} cm × {cube} cm × {cube} cm {obj} can fit inside it?"
    )

    return Question(
        question_text=question_text,
        correct_answer=str(answer),
        topic="container_packing",
        level=level,
        scaffold_steps=scaffold_steps,
        worked_solution=worked_solution,
        examples=examples_map[4],
        videos=[]
    )


# ─────────────────────────────────────────
# MAIN GENERATOR
# ─────────────────────────────────────────

def generate_container_packing_question(level):
    if level == 1:
        return generate_level1_question(level)
    if level == 2:
        return generate_level2_question(level)
    if level == 3:
        return generate_level3_question(level)
    if level == 4:
        return generate_level4_question(level)
    return generate_level1_question(level)

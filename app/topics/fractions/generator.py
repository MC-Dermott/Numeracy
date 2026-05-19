import random

from core.models.question_model import Question


# ---------------------------------------------------
# EXAMPLES (MATCHES PERCENTAGE STYLE)
# ---------------------------------------------------

examples_map = {
    1: [
        "Example for Level 1 (Unit fractions):",
        "What is 1/5 of 40?",
        "40 ÷ 5 = 8",
        "Answer = 8"
    ],
    2: [
        "Example for Level 2 (Non-unit fractions):",
        "What is 3/5 of 40?",
        "1/5 of 40 = 8",
        "3/5 of 40 = 3 × 8",
        "Answer = 24"
    ]
}


# ---------------------------------------------------
# LEVEL 1
# UNIT FRACTIONS
# ---------------------------------------------------

def generate_unit_fraction_question(level):

    denominators = [2, 3, 4, 5, 6, 8, 10]
    denominator = random.choice(denominators)

    multiplier = random.randint(2, 12)
    amount = denominator * multiplier

    answer = amount // denominator

    scaffold_steps = [
        {
            "prompt": f"Divide {amount} by {denominator}?",
            "answer": round(amount / denominator,2) 
        }
    ]

    worked_solution = [
        f"{amount} ÷ {denominator}",
        f"= {answer}"
    ]

    return Question(
        question_text=f"What is 1/{denominator} of {amount}?",
        correct_answer=str(answer),
        topic="fractions",
        level=level,
        scaffold_steps=scaffold_steps,
        worked_solution=worked_solution,
        examples=examples_map[1],
        videos=[]
    )


# ---------------------------------------------------
# LEVEL 2
# NON-UNIT FRACTIONS
# ---------------------------------------------------

def generate_non_unit_fraction_question(level):

    fraction_pairs = [
        (2, 3), (3, 4), (2, 5), (3, 5),
        (5, 6), (3, 8), (5, 8), (7, 10)
    ]

    numerator, denominator = random.choice(fraction_pairs)

    multiplier = random.randint(2, 12)
    amount = denominator * multiplier

    unit_value = amount // denominator
    answer = unit_value * numerator

    scaffold_steps = [
        {
            "prompt": f"Find 1/{denominator} of {amount}",
            "answer": round(amount / denominator,2)
        },
        {   "prompt": f"Multiply 1/{denominator} of {amount}  by {numerator}",
            "answer": answer
        }            
       
    ]

    worked_solution = [
        f"1/{denominator} of {amount} = {unit_value}",
        f"{unit_value} × {numerator} = {answer}"
    ]

    return Question(
        question_text=f"What is {numerator}/{denominator} of {amount}?",
        correct_answer=str(answer),
        topic="fractions",
        level=level,
        scaffold_steps=scaffold_steps,
        worked_solution=worked_solution,
        examples=examples_map[2],
        videos=[]
    )


# ---------------------------------------------------
# MAIN GENERATOR
# ---------------------------------------------------

def generate_fraction_question(level):

    if level == 1:
        return generate_unit_fraction_question(level)

    if level == 2:
        return generate_non_unit_fraction_question(level)

    return generate_unit_fraction_question(level)

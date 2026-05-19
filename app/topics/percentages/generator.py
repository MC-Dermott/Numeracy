import random

from core.models.question_model import Question


def generate_percentage_question(level):

    examples_map = {
        1: [
            "Example for Level 1 (Find 1% of a round number):",
            "What is 1% of 400?",
            "1% of 400 = 400 ÷ 100",
            "Answer = 4"
        ],
        2: [
            "Example for Level 2 (Find any whole % of a round number):",
            "What is 15% of 300?",
            "1% of 300 = 3",
            "15% of 300 = 15 × 3 = 45",
            "Answer = 45"
        ],
        3: [
            "Example for Level 3 (Find 1% of any small number):",
            "What is 1% of 67?",
            "1% of 67 = 67 ÷ 100",
            "Answer = 0.67"
        ],
        4: [
            "Example for Level 4 (Find any whole % of any small number):",
            "What is 12% of 45?",
            "1% of 45 = 0.45",
            "12% of 45 = 12 × 0.45",
            "Answer = 5.4"
        ],
        5: [
            "Example for Level 5 (Find decimal percentages):",
            "What is 3.5% of 200?",
            "1% of 200 = 2",
            "3.5% of 200 = 3.5 × 2",
            "Answer = 7"
        ]
    }

    if level == 1:
        percentage = 1
        amount = random.choice(range(100, 901, 10))

    elif level == 2:
        percentage = random.randint(1, 99)
        amount = random.choice(range(100, 901, 10))

    elif level == 3:
        percentage = 1
        amount = random.randint(0, 100)

    elif level == 4:
        percentage = random.randint(1, 99)
        amount = random.randint(0, 100)

    else:
        percentage = random.choice([x * 0.5 for x in range(1, 201)])
        amount = random.randint(0, 1000)

    answer = round((amount * percentage) / 100, 2)

    # ✔ FIXED scaffold (proper indentation)
    if level == 1:
        scaffold_steps = [
            {
                "prompt": f"What is 1% of {amount}? (divide {amount} by 100)",
                "answer": round(amount / 100,2)
            }
        ]

    else:
        scaffold_steps = [
            {
                "prompt": f"What is 1% of {amount}? (divide {amount} by 100)",
                "answer": round(amount / 100,2)
            },
            {
                "prompt": f"What is {percentage} × 1% of {amount}?",
                "answer": answer
            }
        ]

    level_examples = examples_map.get(level, examples_map[2])

    return Question(
        question_text=f"What is {percentage}% of {amount}?",
        correct_answer= answer,
        topic="percentages",
        level=level,
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"1% of {amount} = {(amount / 100):g}",
            f"Multiply by {percentage}",
            f"Answer = {answer:g}"
        ],
        examples=level_examples,
        videos=[
            {
                "title": "Percentages Tutorial",
                "url": "https://glowscotland-my.sharepoint.com/:v:/g/personal/eslmcdermott1u_glow_sch_uk/IQC73Pb9lrFRSYmcyRfZKmDIAXs34uXQAhWVwDKQkVhTXb4?e=DZT6QE"
            }
        ]
    )

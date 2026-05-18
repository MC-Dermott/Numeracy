
import random

from core.models.question_model import Question

def generate_percentage_question(level):

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

        percentage = random.choice(
            [x * 0.5 for x in range(1, 201)]
        )

        amount = random.randint(0, 1000)

    answer = round(
        (amount * percentage) / 100,
        2
    )

    if level == 1:

        scaffold_steps = [
            "What is 1% of the amount? (divide amount by 100)"
        ]

    else:

        scaffold_steps = [
            "What is 1% of the amount? (divide amount by 100)",
            f"What is {percentage} lots of 1%? ({percentage} times your answer to part 1)"
        ]

    return Question(
        question_text=(
            f"What is {percentage}% of {amount}?"
        ),
        correct_answer=str(answer),
        topic="percentages",
        level=level,
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"1% of {amount} = {amount / 100}",
            f"Multiply by {percentage}",
            f"Answer = {answer}"
        ],
        examples=[
            "1% of 300 = 3",
            "15% of 300 = 15 x 3 = 45"
        ],
        videos=[
            {
                "title": "Percentages Tutorial",
                "url": "https://youtu.be/m2oEVW0p8A8"
            }
        ]
    )

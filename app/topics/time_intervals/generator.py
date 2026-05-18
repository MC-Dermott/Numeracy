
import random
from datetime import datetime, timedelta

from core.models.question_model import Question

def generate_time_interval_question(level):

    step_map = {
        1: 60,
        2: 30,
        3: 15,
        4: 10,
        5: 5
    }

    increment = step_map[level]

    start = datetime(
        2000,
        1,
        1,
        random.randint(0, 23),
        random.choice(range(0, 60, increment))
    )

    end = start + timedelta(
        minutes=random.randint(1, 20) * increment
    )

    diff = int((end - start).total_seconds() / 60)

    hours = diff // 60
    minutes = diff % 60

    return Question(
        question_text=(
            f"What is the time interval between "
            f"{start.strftime('%H:%M')} and "
            f"{end.strftime('%H:%M')}?"
        ),
        correct_answer={
            "hours": hours,
            "minutes": minutes
        },
        topic="time_intervals",
        level=level,
        scaffold_steps=[
            "How many minutes from the start time to the next o'clock?",
            "How many hours between this o'clock and the target o'clock?",
            "How many minutes are there between the target o'clock and the finish time?"
        ],
        worked_solution=[
            f"Start time: {start.strftime('%H:%M')}",
            f"End time: {end.strftime('%H:%M')}",
            f"Total interval = {hours} hours and {minutes} minutes"
        ],
        examples=[
            "Calculate the time interval between 10:30 to 1515",
            "1030 -> 1100 =30 mins",
            "1100 -> 1500 = 4 hours",
            "1500 -> 1515 = 15 minutes",
            "Interval = 15 mins + 30 mins + 4 hours",
            "Interval = 4 hours 45 mins"
        ],
        videos=[
            {
                "title": "Time Interval Tutorial",
                "url": "https://youtu.be/Ni2dnR-yjhU"
            }
        ]
    )

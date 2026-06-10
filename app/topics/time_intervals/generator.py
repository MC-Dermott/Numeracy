import random
from datetime import datetime, timedelta

from core.models.question_model import Question


def generate_time_interval_question(level):

    # --------------------------------------------------
    # Difficulty settings
    # --------------------------------------------------

    step_map = {
        1: 60,  # on the hour
        2: 5,   # finish not on hour
        3: 5,   # start not on hour
        4: 5    # neither on hour
    }

    # --------------------------------------------------
    # Examples
    # --------------------------------------------------

    examples_map = {
        1: [
            "Calculate the time interval between 10:00 and 14:00",
            "10:00 -> 14:00 = 4 hours",
            "Interval = 4 hours"
        ],

        2: [
            "Calculate the time interval between 10:00 and 13:25",
            "10:00 -> 13:00 = 3 hours",
            "13:00 -> 13:25 = 25 mins",
            "Interval = 3 hours 25 mins"
        ],

        3: [
            "Calculate the time interval between 10:35 and 14:00",
            "10:35 -> 11:00 = 25 mins",
            "11:00 -> 14:00 = 3 hours",
            "Interval = 3 hours 25 mins"
        ],

        4: [
            "Calculate the time interval between 10:35 and 14:25",
            "10:35 -> 11:00 = 25 mins",
            "11:00 -> 14:00 = 3 hours",
            "14:00 -> 14:25 = 25 mins",
            "Interval = 3 hours 50 mins"
        ]
    }

    increment = step_map[level]

    level_examples = examples_map.get(level, examples_map[4])

    # --------------------------------------------------
    # Generate times
    # --------------------------------------------------

    if level == 1:

        # BOTH TIMES ON THE HOUR

        start = datetime(
            2000,
            1,
            1,
            random.randint(0, 20),
            0
        )

        end = start + timedelta(
            hours=random.randint(1, 5)
        )

    elif level == 2:

        # START ON HOUR
        # END NOT ON HOUR

        start = datetime(
            2000,
            1,
            1,
            random.randint(0, 20),
            0
        )

        end = start + timedelta(
            hours=random.randint(1, 5),
            minutes=random.choice([5, 10, 15, 20, 25,
                                   30, 35, 40, 45, 50, 55])
        )

    elif level == 3:

        # START NOT ON HOUR
        # END ON HOUR

        start_minute = random.choice(
            [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        )

        start = datetime(
            2000,
            1,
            1,
            random.randint(0, 18),
            start_minute
        )

        mins_to_next_hour = 60 - start.minute

        end = start + timedelta(
            minutes=mins_to_next_hour,
            hours=random.randint(1, 4)
        )

    else:

        # BOTH TIMES NOT ON HOUR

        start_minute = random.choice(
            [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        )

        end_minute = random.choice(
            [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        )

        start = datetime(
            2000,
            1,
            1,
            random.randint(0, 18),
            start_minute
        )

        mins_to_next_hour = 60 - start.minute

        end = start + timedelta(
    minutes=mins_to_next_hour + end_minute,
    hours=random.randint(1, 4)
)

    # --------------------------------------------------
    # Calculate interval
    # --------------------------------------------------

    diff = int((end - start).total_seconds() / 60)

    hours = diff // 60
    minutes = diff % 60

    # --------------------------------------------------
    # Scaffold steps — "count on" through o'clock stepping stones
    # --------------------------------------------------

    scaffold_steps = []
    current = start

    if current.minute != 0:
        next_hour = current.replace(minute=0) + timedelta(hours=1)
        mins = int((next_hour - current).total_seconds() / 60)
        scaffold_steps.append({
            "prompt": f"Count on from {current.strftime('%H:%M')} to {next_hour.strftime('%H:%M')} — how many minutes?",
            "answer": mins
        })
        current = next_hour

    end_oclock = end if end.minute == 0 else end.replace(minute=0)
    while current < end_oclock:
        next_hour = current + timedelta(hours=1)
        scaffold_steps.append({
            "prompt": f"Count on from {current.strftime('%H:%M')} to {next_hour.strftime('%H:%M')} — how many hours?",
            "answer": 1
        })
        current = next_hour

    if end.minute != 0:
        scaffold_steps.append({
            "prompt": f"Count on from {current.strftime('%H:%M')} to {end.strftime('%H:%M')} — how many minutes?",
            "answer": end.minute
        })

    # --------------------------------------------------
    # Return question
    # --------------------------------------------------

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

        scaffold_steps=scaffold_steps,

        worked_solution=[
            f"Start time: {start.strftime('%H:%M')}",
            f"End time: {end.strftime('%H:%M')}",
            f"Total interval = {hours} hours and {minutes} minutes"
        ],

        examples=level_examples,

        videos=[
            {
                "title": "Time Interval Tutorial",
                "url": (
                    "https://glowscotland-my.sharepoint.com/"
                    ":v:/g/personal/"
                    "eslmcdermott1u_glow_sch_uk/"
                    "IQARbgWg_fwMR5FGGBr4RFYCAdOg_6FVElyDZRpKPj5M3z4"
                    "?e=ZHcnni"
                )
            }
        ]
    )

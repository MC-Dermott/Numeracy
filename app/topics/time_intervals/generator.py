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

    # Define unique examples for each difficulty level
    examples_map = {
        1: [
            "Calculate the time interval between 10:00 to 14:00",
            "10:00 -> 14:00 = 4 hours",
            "Interval = 4 hours 0 mins"
        ],
        2: [
            "Calculate the time interval between 10:30 to 13:00",
            "10:30 -> 11:00 = 30 mins",
            "11:00 -> 13:00 = 2 hours",
            "Interval = 2 hours 30 mins"
        ],
        3: [
            "Calculate the time interval between 10:30 to 15:15",
            "10:30 -> 11:00 = 30 mins",
            "11:00 -> 15:00 = 4 hours",
            "15:00 -> 15:15 = 15 minutes",
            "Interval = 15 mins + 30 mins + 4 hours",
            "Interval = 4 hours 45 mins"
        ],
        4: [
            "Calculate the time interval between 08:10 to 10:40",
            "08:10 -> 09:00 = 50 mins",
            "09:00 -> 10:00 = 1 hour",
            "10:00 -> 10:40 = 40 mins",
            "Interval = 50 mins + 40 mins + 1 hour",
            "40 mins + 30 mins = 70 mins = 1 hour 10 mins",
            "Interval = 2 hours 30 mins "
        ],
        5: [
            "Calculate the time interval between 09:05 to 11:25",
            "09:05 -> 10:00 = 55 mins",
            "10:00 -> 11:00 = 1 hour",
            "11:00 -> 11:25 = 25 mins",
            "Interval = 55 mins + 25 mins + 1 hour",
            "55 mins + 25 mins = 80 mins = 1 hour 20 mins",
            "Interval = 2 hours 20 mins"
        ]
    }

    increment = step_map[level]
    # Fallback to level 3 examples if a level is missing from the map
    level_examples = examples_map.get(level, examples_map[3]) 

    start = datetime(
        2000,
        1,
        1,
        random.randint(0, 23),
        random.choice(range(0, 60, increment))
    )

    # --- Update the end time logic here ---
    if level == 1:
        # Calculate how many hours are left in the current day
        hours_left = 23 - start.hour
        if hours_left < 1:
            # If start is 23:00, force end to be 23:00 + 0 hours (same time) 
            # Or reset start hour to allow a gap: start = start.replace(hour=random.randint(0, 22))
            hours_to_add = 0
        else:
            # Pick a random number of hours that fits perfectly within today
            hours_to_add = random.randint(1, hours_left)
            
        end = start + timedelta(hours=hours_to_add)
    else:
        # Keep original logic for other levels
        end = start + timedelta(
            minutes=random.randint(1, 20) * increment
        )
    # --------------------------------------


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
            "How many hours between this o'clock and the finish o'clock?",
            "How many minutes are there between the finish o'clock and the finish time?"
        ],
        worked_solution=[
            f"Start time: {start.strftime('%H:%M')}",
            f"End time: {end.strftime('%H:%M')}",
            f"Total interval = {hours} hours and {minutes} minutes"
        ],
        examples=level_examples,  # Uses the level-specific list here
        videos=[
            {
                "title": "Time Interval Tutorial",
                "url": "https://glowscotland-my.sharepoint.com/:v:/g/personal/eslmcdermott1u_glow_sch_uk/IQARbgWg_fwMR5FGGBr4RFYCAdOg_6FVElyDZRpKPj5M3z4?e=ZHcnni"
            }
        ]
    )



from topics.time_intervals.generator import generate_time_interval_question
from topics.percentages.generator import generate_percentage_question
from topics.fractions.generator import generate_fraction_question

TOPIC_REGISTRY = {
    "Time Intervals": {
        "generator": generate_time_interval_question,
        "levels": [
            {
                "id": 1,
                "label": "Level 1",
                "description": "Start and finish are o'clocks"
            },
            {
                "id": 2,
                "label": "Level 2",
                "description": "Final time is an o'clock"
            },
            {
                "id": 3,
                "label": "Level 3",
                "description": "Start time is an o'clock"
            },
            {
                "id": 4,
                "label": "Level 4",
                "description": "Neither time is an o'clock"
            }
        ]
    },

    "Percentages": {
        "generator": generate_percentage_question,
        "levels": [
            {
                "id": 1,
                "label": "Level 1",
                "description": "Find 1% of amounts"
            },
            {
                "id": 2,
                "label": "Level 2",
                "description": "Find different percentages of amounts"
            },
            {
                "id": 3,
                "label": "Level 3",
                "description": "Find 1% of smaller amounts"
            },
            {
                "id": 4,
                "label": "Level 4",
                "description": "Find different percentages of different types of amounts"
            }
        ]
    },
    "Fractions": {
        "generator": generate_fraction_question,
        "levels": [
            {
                "id": 1,
                "label": "Level 1",
                "description": "Find unit fractions of amounts"
            },
            {
                "id": 2,
                "label": "Level 2",
                "description": "Find non-unit fractions of amounts"
            }
        ]
    }
    
}


def get_topic_levels(topic):
    return TOPIC_REGISTRY[topic]["levels"]



def generate_question(topic, level):
    generator = TOPIC_REGISTRY[topic]["generator"]
    return generator(level)

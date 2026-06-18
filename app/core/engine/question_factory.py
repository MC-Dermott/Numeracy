
from topics.area.generator import generate_area_question
from topics.time_intervals.generator import generate_time_interval_question
from topics.percentages.generator import generate_percentage_question
from topics.fractions.generator import generate_fraction_question
from topics.container_packing.generator import generate_container_packing_question

TOPIC_REGISTRY = {
    "Area": {
        "generator": generate_area_question,
        "levels": [
            {"id": 1, "label": "Level 1", "description": "Squares & rectangles (same unit)"},
            {"id": 2, "label": "Level 2", "description": "Rectangles with mixed units"},
            {"id": 3, "label": "Level 3", "description": "Triangles (same unit)"},
            {"id": 4, "label": "Level 4", "description": "Triangles with mixed units"},
        ],
    },
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
    },

    "Container Packing": {
        "generator": generate_container_packing_question,
        "levels": [
            {
                "id": 1,
                "label": "Level 1",
                "description": "How many objects fit along a line (mixed units)"
            },
            {
                "id": 2,
                "label": "Level 2",
                "description": "Choose the best side to maximise objects along a line"
            },
            {
                "id": 3,
                "label": "Level 3",
                "description": "How many square tiles fit in an area"
            },
            {
                "id": 4,
                "label": "Level 4",
                "description": "Choose the best orientation to maximise objects in an area"
            },
            {
                "id": 5,
                "label": "Level 5",
                "description": "How many cubes fit in a 3D volume"
            }
        ]
    }

}


def get_topic_levels(topic):
    return TOPIC_REGISTRY[topic]["levels"]



def generate_question(topic, level):
    generator = TOPIC_REGISTRY[topic]["generator"]
    return generator(level)


from topics.time_intervals.generator import generate_time_interval_question
from topics.percentages.generator import generate_percentage_question

TOPIC_REGISTRY = {
    "Time Intervals": generate_time_interval_question,
    "Percentages": generate_percentage_question
}

def generate_question(topic, level):
    return TOPIC_REGISTRY[topic](level)

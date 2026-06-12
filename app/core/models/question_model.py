import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Question:
    question_text: str
    correct_answer: Any
    topic: str
    level: int
    scaffold_steps: list[str] = field(default_factory=list)
    worked_solution: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    videos: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    qid: str = field(default_factory=lambda: str(uuid.uuid4()))

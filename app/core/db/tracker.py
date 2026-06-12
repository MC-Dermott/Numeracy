from core.db.client import get_supabase


def save_practice_attempt(user_id: str, topic: str, level: str, correct: bool):
    try:
        get_supabase().table("numeracy_attempts").insert({
            "user_id": user_id,
            "topic": topic,
            "level": level,
            "correct": correct,
        }).execute()
    except Exception:
        pass


def save_test_result(user_id: str, topic: str, level: str, score: int, total: int):
    try:
        get_supabase().table("numeracy_test_results").insert({
            "user_id": user_id,
            "topic": topic,
            "level": level,
            "score": score,
            "total": total,
        }).execute()
    except Exception:
        pass

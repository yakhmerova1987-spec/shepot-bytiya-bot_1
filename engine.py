# engine.py
import random
from datetime import datetime, time
from typing import Optional

from content import BASE_PHRASES, NIGHT_PHRASES, METAPHORS_WITH_QUESTIONS


def is_night(now: datetime) -> bool:
    """
    Ночной режим: с 22:00 до 02:00.
    """
    return time(22, 0) <= now.time() or now.time() <= time(2, 0)


def choose_reply(user_text: str, now: Optional[datetime] = None) -> str:
    """
    Выбор ответа:
    - всегда текст
    - днём: баланс метафор и простых фраз
    - ночью: чуть больше метафор, но с примесью мягкой поддержки
    """
    if now is None:
        now = datetime.now()

    roll = random.random()

    if is_night(now):
        # ночью: 60% метафоры + вопрос, 40% короткие фразы (ночные + базовые)
        if roll < 0.6:
            text, question = random.choice(METAPHORS_WITH_QUESTIONS)
            return f"{text}\n\n{question}"
        else:
            pool = (NIGHT_PHRASES or []) + BASE_PHRASES
            return random.choice(pool)

    # днём: 50% метафоры, 50% короткие фразы
    if roll < 0.5:
        text, question = random.choice(METAPHORS_WITH_QUESTIONS)
        return f"{text}\n\n{question}"
    else:
        return random.choice(BASE_PHRASES)

import random
from datetime import datetime, time
from content import BASE_PHRASES, NIGHT_PHRASES, METAPHORS_WITH_QUESTIONS

def is_night(now: datetime) -> bool:
    return time(22, 0) <= now.time() or now.time() <= time(2, 0)

def choose_reply(user_text: str, now=None) -> str:
    if now is None:
        now = datetime.now()

    roll = random.random()

    if is_night(now):
        if roll < 0.7:
            text, question = random.choice(METAPHORS_WITH_QUESTIONS)
            return f"{text}\n\n{question}"
        else:
            return random.choice(NIGHT_PHRASES or BASE_PHRASES)

    if roll < 0.6:
        text, question = random.choice(METAPHORS_WITH_QUESTIONS)
        return f"{text}\n\n{question}"
    else:
        return random.choice(BASE_PHRASES)

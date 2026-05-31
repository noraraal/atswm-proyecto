import secrets

# Diccionario global token -> user_id
SESSIONS: dict[str, int] = {}


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def create_session(user_id: int) -> str:
    token = generate_token()
    SESSIONS[token] = user_id
    return token


def validate_session(token: str) -> int | None:
    return SESSIONS.get(token)


def delete_session(token: str):
    SESSIONS.pop(token, None)

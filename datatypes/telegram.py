from pydantic import BaseModel


class Response(BaseModel):
    ok: bool
    error_code: int | None
    description: str | None

from pydantic import BaseModel

class Lecture(BaseModel):
    name: str
    text: str
    speaker: str
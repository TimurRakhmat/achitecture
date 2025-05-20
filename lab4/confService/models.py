from pydantic import BaseModel

class Lecture(BaseModel):
    name: str
    text: str
    speaker: str

class LectureResponse(Lecture):
    lk_id: str
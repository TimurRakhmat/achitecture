from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models import Lecture

SECRET_KEY = "secret"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")

app = FastAPI()

Lectures = []

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

@app.post("/lectures")
def add_post(post: Lecture, username: str = Depends(verify_token)):
    Lectures.append(post)
    return post

@app.get("/lectures")
def get_all_lectures():
    return Lectures

@app.get("/lectures/{l_id}")
def get_lecture(l_id: int, username: str = Depends(verify_token)):
    for lect in Lectures:
        if l_id == lect.name:
            return lect
    raise HTTPException(status_code=404, detail="Lecture not found")
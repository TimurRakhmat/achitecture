from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from bson import ObjectId
from models import Lecture, LectureResponse
from pymongo import mongo_client
import mongo_init
from datetime import datetime

SECRET_KEY = "secret"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")

mongo_init.db_init()
client = mongo_client.MongoClient(host='mongo', port=27017, uuidRepresentation='standard')
lk = client['conf']['lectures']

app = FastAPI()


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

@app.post("/lectures", response_model=LectureResponse)
def add_post(post: Lecture):
    dump = post.model_dump()
    dump['sending_time'] = datetime.now()
    result = lk.insert_one(dump)
    return LectureResponse(**post.model_dump(), lk_id=str(result.inserted_id))

def convert_def(item):
    item['lk_id'] = str(item['_id'])
    print(item)
    print(str(item))
    return item

@app.get("/lectures", response_model=list[Lecture])
def get_all_lectures():
    res = lk.find()
    return list(res)

@app.get("/lectures/{l_id}", response_model=Lecture)
def get_lecture(l_id: str):
    query = {"_id": ObjectId(l_id)}
    result = lk.find_one(query)

    if result:
        print(f"Lecture found: {result}")
        return result
    else:
        print("Lecture not found")
        raise HTTPException(status_code=404, detail="Lecture not found")
    
@app.get("/lectures/find/{name}", response_model=Lecture)
def get_lecture(name: str):
    query = {"name": name}
    result = lk.find_one(query)

    if result:
        print(f"Lk found: {result}")
        return result
    else:
        print("Lecture not found")
        raise HTTPException(status_code=404, detail="Lecture not found")
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import auth, models, database
from datetime import timedelta
from redis import Redis
import json
from sqlalchemy.exc import IntegrityError

database.init_db()
redis_client = Redis(host='redis', decode_responses=True)
app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: database.Session = Depends(get_db)):
    password_check = False
    current_user = db.query(models.DbUser).filter(models.DbUser.username == form_data.username).first()

    if current_user:
        hashPassword = current_user.password_hash
        if auth.pwd_context.verify(form_data.password, hashPassword):
            password_check = True

    if password_check:
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@app.post("/conference_users", response_model=models.UserResponse)
def create_user(conference_user: models.UserCreate, db: database.Session = Depends(get_db)):
    db_user = models.DbUser(**conference_user.model_dump())
    db_user.password_hash = auth.pwd_context.hash(db_user.password_hash)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")


@app.get("/conference_users/", response_model= list[models.UserResponse])
async def get_conference_users(current_user: str = Depends(auth.get_current_user), db: database.Session = Depends(get_db)):
    users = db.query(models.DbUser).all()
    return users

@app.get(
        "/conference_users/{user_id}", response_model=models.UserResponse)
async def get_user(user_id: int, current_user: str = Depends(auth.get_current_user), db: database.Session = Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get(
        "/conference_users/find/{name}", response_model=models.UserResponse)
async def get_user_by_name(name: str, current_user: str = Depends(auth.get_current_user), db: database.Session = Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.username == name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get(
        "/conference_users/find/redis/{name}", response_model=models.UserResponse)
async def get_user_by_name(name: str, current_user: str = Depends(auth.get_current_user), db: database.Session = Depends(get_db)):
    cache_key = f"user:{name}"
    if redis_client.exists(cache_key):
        cached_user = redis_client.get(cache_key)
        return json.loads(cached_user)
    else:
        user = db.query(models.DbUser).filter(models.DbUser.username == name).first()
        user_json = user.__dict__
        user_json.pop('_sa_instance_state', None)
        user_json.pop('created_at', None)
        print(user_json)

        if user:
            redis_client.set(cache_key, json.dumps(user_json),ex = 180)
        else:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@app.get("/me",
        summary="endpoint для обычного получения текущего пользователя")
async def read_users_me(current_user=Depends(auth.get_current_user)):
    return current_user

@app.post("/conference_users/testfill")
def create_user_test(db: database.Session = Depends(get_db)):
    for i in range(1001,100000):
        db_user = models.DbUser()
        db_user.username=f'Ivan{i}'
        db_user.password_hash=auth.pwd_context.hash(f'Ivanov{i}')
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Username already exists")
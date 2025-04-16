from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import auth, models
from datetime import timedelta

app = FastAPI()

@app.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    password_check = False
    print(form_data)
    if form_data.username in auth.users_db:
        hashPassword = auth.users_db.get(form_data.username)["password"]
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

@app.get("/conference_users",
        summary="endpoint для обычного получения всех пользователей без авторизации")
async def get_conference_users():
    return auth.users_db

@app.get(
        "/conference_users/{user_id}",
        summary="endpoint для обычного получения пользователя по его id")
async def get_user(user_id: int, current_user: str = Depends(auth.get_current_user)):
    for conference_user in auth.users_db:
        if user_id == conference_user["id"]:
            return conference_user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/me",
        summary="endpoint для обычного получения текущего пользователя")
async def read_users_me(current_user=Depends(auth.get_current_user)):
    return current_user
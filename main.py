from fastapi import Depends, FastAPI
from routers import users
from services import oauth2_scheme

app = FastAPI()


app.include_router(users.router)


@app.get('/')
def root(token: str = Depends(oauth2_scheme)):
    return {"message": "Hello World"}
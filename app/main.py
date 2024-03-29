from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from pydantic import BaseSettings
from .config import settings

from pyngrok import ngrok

public_url = ngrok.connect(8000).public_url


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["https://www.google.com","https://www.youtube.com"]
origins = ["*"]
app.add_middleware(
    CORSMiddleware, # function -> runs before every request
    allow_origins=origins, # what domain should we able to talk to our api
    allow_credentials=True, # 
    allow_methods=["*"], # not only allow spicific domain but also we allow specific http method -> if public api -> user get data -> we not allow user to make put request 
    allow_headers=["*"], # spcific header
)

# get request function with path operation.
@app.get('/')
def root():
    return {'Status':'Application Ran succesfully On Server'}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)






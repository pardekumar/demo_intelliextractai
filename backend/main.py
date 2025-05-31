from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_query_token, get_token_header
from internal import admin
from routers import documents, users

from dotenv import load_dotenv

load_dotenv()


app = FastAPI(dependencies=[
    # Depends(get_query_token)
])

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(documents.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

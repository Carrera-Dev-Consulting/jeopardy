from fastapi import FastAPI
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 5000


api_settings = APISettings()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

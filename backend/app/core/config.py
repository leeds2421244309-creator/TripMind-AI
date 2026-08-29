from ast import Str
from pydantic_settings import BaseSettings
# 因为导入包名不能包含——所以改为_
class Settings(BaseSettings):
     # Database
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str


    # AI
    QWEN_API_KEY: str
    QWEN_MODEL:str
    QWEN_BASE_URL:str

    # Map
    AMAP_API_KEY: str
    AMAP_BASE_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()

from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv(verbose=True)
class Settings(BaseSettings):
    app_name:str="Import Training"
    app_url:str
    class Conifg:
        env_file = '../.env'
        env_file_encoding = 'utf-8'
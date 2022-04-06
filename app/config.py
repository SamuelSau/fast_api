from pydantic import BaseSettings

#pydantic allows us to perform validation for environment variables for our database without us having to manually do so in our local machine
#not have to use in production since you can do that manullay on your machine, but for development is good
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str 
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
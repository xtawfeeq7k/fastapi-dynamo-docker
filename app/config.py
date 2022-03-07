from pydantic import BaseSettings
class Settings(BaseSettings):

  endpoint_url: str = "http://localhost:4566"
  table : str = "users"


settings = Settings()

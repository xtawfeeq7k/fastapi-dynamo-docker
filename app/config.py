from pydantic import BaseSettings
class Settings(BaseSettings):

  endpoint_url: str = "http://localstack:4566"
  table : str = "table"

settings = Settings()
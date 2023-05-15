from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str = ''

    secret: str = 'my_secret'

    test: bool = False
    debug: bool = False

    def get_db_url(self):
        return self.db_url


settings = Settings()

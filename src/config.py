from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = '.env'


class Postgres(BaseSettings):
    name: str = 'postgres'
    username: str = 'postgres'
    password: str = 'password'
    host: str = 'localhost'
    port: int = 5325

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_prefix='POSTGRES_', extra='ignore')

    @property
    def uri(self) -> str:
        user_info = f'{self.username}:{self.password}'
        host_info = f'{self.host}:{self.port}/{self.name}'
        return f'postgresql+asyncpg://{user_info}@{host_info}'


class Config(BaseSettings):
    token: str
    postgres: Postgres = Postgres()

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')


config = Config()

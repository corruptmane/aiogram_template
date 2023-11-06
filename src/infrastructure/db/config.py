from dataclasses import dataclass

from sqlalchemy import URL


@dataclass(frozen=True, slots=True)
class DBConfig:
    host: str | None = 'localhost'
    port: int | None = 5432
    login: str | None = 'postgres'
    password: str | None = 'postgres'
    name: str | None = 'postgres'

    @property
    def url(self) -> URL:
        return URL(
            drivername="postgresql+asyncpg",
            username=self.login,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
            query={},
        )

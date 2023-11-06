from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: str = 'localhost'
    port: int = 6379
    db: int = 1
    password: str | None = None

    @property
    def url(self) -> str:
        url = 'redis://'
        if self.password is not None:
            url += f':{self.password}@'
        url += f'{self.host}:{self.port}/{self.db}'
        return url

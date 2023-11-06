# NATS migrations file
import asyncio

from src.infrastructure.config_loader import load_config
from src.infrastructure.log.config import LoggingConfig
from src.infrastructure.log.main import configure_logging
from .factory import init_nats_adapter
from .config import NATSConfig


async def init() -> None:
    config = load_config(NATSConfig, 'nats')
    configure_logging(load_config(LoggingConfig, 'logging'))
    adapter = init_nats_adapter(config)

    await adapter.connect(init_streams=True, init_consumers=True)

    await adapter.close()


def run() -> None:
    asyncio.run(init())


if __name__ == '__main__':
    run()

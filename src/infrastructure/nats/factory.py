from src.common import dcf_dump
from .adapter import NATSAdapter
from .callbacks import all_callbacks
from .config import NATSConfig


def init_nats_adapter(config: NATSConfig) -> NATSAdapter:
    return NATSAdapter(
        config.servers,
        streams=config.streams,
        consumers=config.consumers,
        **dcf_dump(config.connection),
        **all_callbacks,
    )

from dataclasses import dataclass, field
from typing import NamedTuple

from nats.aio.client import (
    DEFAULT_CONNECT_TIMEOUT, DEFAULT_RECONNECT_TIME_WAIT, DEFAULT_MAX_RECONNECT_ATTEMPTS, DEFAULT_PING_INTERVAL,
    DEFAULT_MAX_OUTSTANDING_PINGS, DEFAULT_MAX_FLUSHER_QUEUE_SIZE, DEFAULT_DRAIN_TIMEOUT, DEFAULT_PENDING_SIZE,
)
from nats.js.api import StreamConfig, ConsumerConfig


@dataclass
class ConnectionConfig:
    name: str = None
    pedantic: bool = False
    verbose: bool = False
    allow_reconnect: bool = True,
    connect_timeout: int = DEFAULT_CONNECT_TIMEOUT
    reconnect_time_wait: int = DEFAULT_RECONNECT_TIME_WAIT
    max_reconnect_attempts: int = DEFAULT_MAX_RECONNECT_ATTEMPTS
    ping_interval: int = DEFAULT_PING_INTERVAL
    max_outstanding_pings: int = DEFAULT_MAX_OUTSTANDING_PINGS
    dont_randomize: bool = False
    flusher_queue_size: int = DEFAULT_MAX_FLUSHER_QUEUE_SIZE
    no_echo: bool = False
    user: str | None = None
    password: str | None = None
    token: str | None = None
    drain_timeout: int = DEFAULT_DRAIN_TIMEOUT
    nkeys_seed: str | None = None
    pending_size: int = DEFAULT_PENDING_SIZE
    flush_timeout: float | None = None


class Streams(NamedTuple):
    some_stream: StreamConfig


@dataclass(slots=True, frozen=True)
class Consumer:
    stream_name: str
    config: ConsumerConfig


class Consumers(NamedTuple):
    some_consumer: Consumer


@dataclass(frozen=True, slots=True)
class NATSConfig:
    streams: Streams = field(default_factory=tuple)
    consumers: Consumers = field(default_factory=tuple)
    connection: ConnectionConfig = field(default_factory=ConnectionConfig)
    servers: list[str] = field(default_factory=lambda: ["nats://localhost:4222"])

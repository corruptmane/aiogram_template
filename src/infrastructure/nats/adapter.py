import asyncio
import ssl
from types import TracebackType
from typing import Callable, Awaitable, Self, Type, Any, Protocol

import structlog
from nats.aio.client import (
    Credentials, JWTCallback, SignatureCallback, DEFAULT_DRAIN_TIMEOUT, Callback, ErrorCallback,
    DEFAULT_INBOX_PREFIX, DEFAULT_PENDING_SIZE, DEFAULT_MAX_FLUSHER_QUEUE_SIZE, DEFAULT_MAX_OUTSTANDING_PINGS,
    DEFAULT_PING_INTERVAL, DEFAULT_MAX_RECONNECT_ATTEMPTS, DEFAULT_RECONNECT_TIME_WAIT, DEFAULT_CONNECT_TIMEOUT, Client,
)
from nats.aio.msg import Msg
from nats.aio.subscription import Subscription, DEFAULT_SUB_PENDING_MSGS_LIMIT, DEFAULT_SUB_PENDING_BYTES_LIMIT
from nats.js import JetStreamContext, api
from nats.js.api import StreamConfig
from nats.js.client import DEFAULT_JS_SUB_PENDING_MSGS_LIMIT, DEFAULT_JS_SUB_PENDING_BYTES_LIMIT
from nats.js.errors import NotFoundError

from .config import Streams, Consumers, Consumer

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class Unsubscribable(Protocol):
    async def unsubscribe(self) -> None:
        raise NotImplementedError


class NATSAdapter:
    def __init__(
            self,
            servers: list[str],
            error_cb: ErrorCallback | None = None,
            disconnected_cb: Callback | None = None,
            closed_cb: Callback | None = None,
            discovered_server_cb: Callback | None = None,
            reconnected_cb: Callback | None = None,
            name: str | None = None,
            pedantic: bool = False,
            verbose: bool = False,
            allow_reconnect: bool = True,
            connect_timeout: int = DEFAULT_CONNECT_TIMEOUT,
            reconnect_time_wait: int = DEFAULT_RECONNECT_TIME_WAIT,
            max_reconnect_attempts: int = DEFAULT_MAX_RECONNECT_ATTEMPTS,
            ping_interval: int = DEFAULT_PING_INTERVAL,
            max_outstanding_pings: int = DEFAULT_MAX_OUTSTANDING_PINGS,
            dont_randomize: bool = False,
            flusher_queue_size: int = DEFAULT_MAX_FLUSHER_QUEUE_SIZE,
            no_echo: bool = False,
            tls: ssl.SSLContext | None = None,
            tls_hostname: str | None = None,
            user: str | None = None,
            password: str | None = None,
            token: str | None = None,
            drain_timeout: int = DEFAULT_DRAIN_TIMEOUT,
            signature_cb: SignatureCallback | None = None,
            user_jwt_cb: JWTCallback | None = None,
            user_credentials: Credentials | None = None,
            nkeys_seed: str | None = None,
            inbox_prefix: str | bytes = DEFAULT_INBOX_PREFIX,
            pending_size: int = DEFAULT_PENDING_SIZE,
            flush_timeout: float | None = None,
            streams: Streams = tuple(),
            consumers: Consumers = tuple(),
    ) -> None:
        self.client = Client()
        self.servers = servers
        self.connection_kwargs = dict(
            error_cb=error_cb,
            disconnected_cb=disconnected_cb,
            closed_cb=closed_cb,
            discovered_server_cb=discovered_server_cb,
            reconnected_cb=reconnected_cb,
            name=name,
            pedantic=pedantic,
            verbose=verbose,
            allow_reconnect=allow_reconnect,
            connect_timeout=connect_timeout,
            reconnect_time_wait=reconnect_time_wait,
            max_reconnect_attempts=max_reconnect_attempts,
            ping_interval=ping_interval,
            max_outstanding_pings=max_outstanding_pings,
            dont_randomize=dont_randomize,
            flusher_queue_size=flusher_queue_size,
            no_echo=no_echo,
            tls=tls,
            tls_hostname=tls_hostname,
            user=user,
            password=password,
            token=token,
            drain_timeout=drain_timeout,
            signature_cb=signature_cb,
            user_jwt_cb=user_jwt_cb,
            user_credentials=user_credentials,
            nkeys_seed=nkeys_seed,
            inbox_prefix=inbox_prefix,
            pending_size=pending_size,
            flush_timeout=flush_timeout,
        )
        self.streams = streams
        self.consumers = consumers
        self.subscriptions: list[Unsubscribable] = []

    @property
    def jetstream(self) -> JetStreamContext:
        return self.client.jetstream()

    async def _init_streams(self) -> None:
        await log.ainfo('Initializing streams')
        for stream in self.streams:
            stream: StreamConfig
            await log.adebug('Initializing stream', stream=stream)
            with structlog.contextvars.bound_contextvars(stream_name=stream.name):
                try:
                    await self.jetstream.stream_info(stream.name)
                except NotFoundError:
                    await log.adebug('Stream not found, creating', stream=stream)
                    await self.jetstream.add_stream(stream)
                except Exception as exc:
                    await log.aexception('Failed to get stream info', exc_info=exc, stream=stream)

    async def _init_consumers(self) -> None:
        await log.ainfo('Initializing consumers')
        for consumer in self.consumers:
            consumer: Consumer
            await log.adebug('Initializing consumer', consumer=consumer)
            consumer_name = consumer.config.durable_name or consumer.config.name
            with structlog.contextvars.bound_contextvars(consumer_name=consumer_name):
                try:
                    await self.jetstream.consumer_info(consumer.stream_name, consumer_name)
                except NotFoundError:
                    await log.adebug('Consumer not found, creating', consumer=consumer)
                    await self.jetstream.add_consumer(consumer.stream_name, consumer.config)
                except Exception as exc:
                    await log.aexception('Failed to get consumer info', exc_info=exc, consumer=consumer)
                    raise exc

    async def connect(self, init_streams: bool = False, init_consumers: bool = False) -> None:
        await self.client.connect(self.servers, **self.connection_kwargs)
        if init_streams:
            await self._init_streams()
        if init_consumers:
            await self._init_consumers()

    async def close(self) -> None:
        for sub in self.subscriptions:
            await sub.unsubscribe()
        await self.client.drain()

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(
            self,
            exc_type: Type[Exception] | None,
            exc_val: Exception | None,
            exc_tb: TracebackType | None,
    ) -> None:
        if exc_val is not None:
            await log.aexception('NATSAdapter error', exc_info=exc_val)
        await self.close()

    async def core_publish(
            self,
            subject: str,
            payload: bytes = b'',
            reply: str = '',
            headers: dict[str, str] | None = None
    ) -> None:
        return await self.client.publish(subject, payload, reply, headers)

    async def core_request(
            self,
            subject: str,
            payload: bytes = b'',
            timeout: float = 0.5,
            old_style: bool = False,
            headers: dict[str, Any] | None = None,
    ):
        return await self.client.request(subject, payload, timeout, old_style, headers)

    def auto_unsubscribe(self, sub: Unsubscribable) -> None:
        self.subscriptions.append(sub)

    async def core_subscribe(
            self,
            subject: str,
            queue: str = "",
            cb: Callable[[Msg], Awaitable[None]] | None = None,
            future: asyncio.Future | None = None,
            max_msgs: int = 0,
            pending_msgs_limit: int = DEFAULT_SUB_PENDING_MSGS_LIMIT,
            pending_bytes_limit: int = DEFAULT_SUB_PENDING_BYTES_LIMIT,
    ) -> Subscription:
        sub = await self.client.subscribe(
            subject, queue, cb, future, max_msgs, pending_msgs_limit, pending_bytes_limit,
        )
        return sub

    async def jetstream_publish(
            self,
            subject: str,
            payload: bytes = b'',
            timeout: float | None = None,
            stream: str | None = None,
            headers: dict | None = None
    ) -> api.PubAck:
        return await self.jetstream.publish(subject, payload, timeout, stream, headers)

    async def jetstream_subscribe(
            self,
            stream: str,
            config: api.ConsumerConfig,
            consumer: str,
            cb: Callback | None = None,
            manual_ack: bool = False,
            ordered_consumer: bool = False,
            pending_msgs_limit: int = DEFAULT_JS_SUB_PENDING_MSGS_LIMIT,
            pending_bytes_limit: int = DEFAULT_JS_SUB_PENDING_BYTES_LIMIT,
    ) -> JetStreamContext.PushSubscription:
        sub = await self.jetstream.subscribe_bind(
            stream, config, consumer, cb, manual_ack, ordered_consumer, pending_msgs_limit, pending_bytes_limit,
        )
        return sub

    async def jetstream_pull_subscribe(
            self,
            durable: str,
            stream: str,
            inbox_prefix: bytes = api.INBOX_PREFIX,
            pending_msgs_limit: int = DEFAULT_JS_SUB_PENDING_MSGS_LIMIT,
            pending_bytes_limit: int = DEFAULT_JS_SUB_PENDING_BYTES_LIMIT,
    ) -> JetStreamContext.PullSubscription:
        sub = await self.jetstream.pull_subscribe_bind(
            durable, stream, inbox_prefix, pending_msgs_limit, pending_bytes_limit,
        )
        return sub

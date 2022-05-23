import logging
from typing import Literal, Any, NoReturn

import aiohttp
from aiohttp import ClientResponse

log = logging.getLogger(__name__)


async def send_request(
        *,
        url: str,
        timeout: int = 30,
        method: Literal['GET', 'PUT', 'POST', 'DELETE'] = 'GET',
        params: dict = None,
        session: aiohttp.ClientSession = None,
        headers: Any = None,
        data: Any = None,
        json: Any = None,
        **session_kwargs: Any
) -> ClientResponse | NoReturn:
    is_user_session = True
    if session is None:
        session = aiohttp.ClientSession(**session_kwargs)
        is_user_session = False
    try:
        result = await session.request(
            method, url, params=params, timeout=timeout, data=data, headers=headers, json=json
        )
    except Exception as e:
        log.exception(e)
        result = e
    finally:
        if not is_user_session:
            await session.close()
    if isinstance(result, Exception):
        raise result
    return result

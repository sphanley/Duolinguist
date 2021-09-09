"""Sample API Client."""
import logging
import asyncio
import socket
from typing import Optional
import duolingo

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)


class DuolingoApiClient:
    def __init__(self, username: str, password: str) -> None:
        """Duolingo API Client."""
        self._username = username
        self._password = password

    def get_streak_data(self) -> dict:
        """Get data from the API."""

        return duolingo.Duolingo(self._username, self._password).get_streak_info()

    # async def api_wrapper(
    #     self, method: str, url: str, data: dict = {}, headers: dict = {}
    # ) -> dict:
    #     """Get information from the API."""
    #     try:
    #         async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
    #             if method == "get":
    #                 response = await self._session.get(url, headers=headers)
    #                 return await response.json()

    #             elif method == "put":
    #                 await self._session.put(url, headers=headers, json=data)

    #             elif method == "patch":
    #                 await self._session.patch(url, headers=headers, json=data)

    #             elif method == "post":
    #                 await self._session.post(url, headers=headers, json=data)

    #     except asyncio.TimeoutError as exception:
    #         _LOGGER.error(
    #             "Timeout error fetching information from %s - %s",
    #             url,
    #             exception,
    #         )

    #     except (KeyError, TypeError) as exception:
    #         _LOGGER.error(
    #             "Error parsing information from %s - %s",
    #             url,
    #             exception,
    #         )
    #     except (aiohttp.ClientError, socket.gaierror) as exception:
    #         _LOGGER.error(
    #             "Error fetching information from %s - %s",
    #             url,
    #             exception,
    #         )
    #     except Exception as exception:  # pylint: disable=broad-except
    #         _LOGGER.error("Something really wrong happened! - %s", exception)
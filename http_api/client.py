from __future__ import annotations

from enum import Enum

import httpx
from httpx import BasicAuth


class ResponseFormat(Enum):
    ND_JSON = "JSONEachRow"
    JSON = "JSON"
    COMPACT_JSON = "JSONCompact"


class Client:
    def __init__(self, url: str, basic_auth: str | None = None, token_auth: str | None = None):
        assert basic_auth is not None or token_auth is not None, "Set either basic_auth xor token_auth"
        assert not (basic_auth is not None and token_auth is not None), "Set either basic_auth xor token_auth"

        self._url = url
        self._basic_auth = basic_auth
        self._token_auth = token_auth

    def execute_query(self, sql: str, response_format: ResponseFormat):
        headers = {"format": response_format.value}

        if self._token_auth:
            headers["X-API-Key"] = self._token_auth

        auth = None
        if self._basic_auth:
            username, password = self._basic_auth.split(":")
            auth = BasicAuth(username, password)

        with httpx.Client() as client:
            response = client.get(self._url, params={"q": sql}, headers=headers, auth=auth)
            response.raise_for_status()
            return response.json()

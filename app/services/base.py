from __future__ import annotations

from typing import Any, Callable

import requests
from flask import current_app, flash
from flask_login import current_user


class APIClientError(Exception):
    pass


class APIClient:
    @staticmethod
    def _headers(include_auth: bool = True, token: str | None = None) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        bearer = None
        if token:
            bearer = token
        elif include_auth and getattr(current_user, "access_token", None):
            bearer = current_user.access_token
        if bearer:
            headers["Authorization"] = f"Bearer {bearer}"
        return headers

    @classmethod
    def _handle_response(cls, response: requests.Response) -> Any:
        if response.ok:
            if response.content:
                return response.json()
            return None
        try:
            data = response.json()
        except ValueError as exc:
            raise APIClientError(response.text) from exc
        message = data.get("detail") if isinstance(data, dict) else data
        if isinstance(message, list):
            for error in message:
                loc = ".".join(str(part) for part in error.get("loc", []))
                flash(f"{loc}: {error.get('msg')}", "danger")
        else:
            flash(str(message), "danger")
        raise APIClientError(str(message))

    @classmethod
    def request(
        cls,
        method: str,
        endpoint: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        include_auth: bool = True,
        on_success: Callable[[Any], None] | None = None,
        token: str | None = None,
    ) -> Any:
        base_url = current_app.config["API_BASE_URL"].rstrip("/")
        url = f"{base_url}{endpoint}"
        response = requests.request(
            method,
            url,
            headers=cls._headers(include_auth=include_auth, token=token),
            json=json,
            params=params,
            timeout=15,
        )
        data = cls._handle_response(response)
        if on_success:
            on_success(data)
        return data

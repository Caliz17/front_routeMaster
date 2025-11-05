from __future__ import annotations

from typing import Any

from .base import APIClient


class ClienteService:
    @staticmethod
    def list(skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        return APIClient.request("GET", "/clientes/", params={"skip": skip, "limit": limit})

    @staticmethod
    def create(payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("POST", "/clientes/", json=payload)

    @staticmethod
    def get(cliente_id: int) -> dict[str, Any]:
        return APIClient.request("GET", f"/clientes/{cliente_id}")

    @staticmethod
    def update(cliente_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("PUT", f"/clientes/{cliente_id}", json=payload)

    @staticmethod
    def delete(cliente_id: int) -> dict[str, Any]:
        return APIClient.request("DELETE", f"/clientes/{cliente_id}")

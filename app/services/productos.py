from __future__ import annotations

from typing import Any

from .base import APIClient


class ProductoService:
    @staticmethod
    def list(skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        return APIClient.request("GET", "/productos/", params={"skip": skip, "limit": limit})

    @staticmethod
    def create(payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("POST", "/productos/", json=payload)

    @staticmethod
    def get(producto_id: int) -> dict[str, Any]:
        return APIClient.request("GET", f"/productos/{producto_id}")

    @staticmethod
    def update(producto_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("PUT", f"/productos/{producto_id}", json=payload)

    @staticmethod
    def delete(producto_id: int) -> dict[str, Any]:
        return APIClient.request("DELETE", f"/productos/{producto_id}")

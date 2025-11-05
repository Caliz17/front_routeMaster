from __future__ import annotations

from typing import Any

from .base import APIClient


class PedidoService:
    @staticmethod
    def list(skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        return APIClient.request("GET", "/pedidos/", params={"skip": skip, "limit": limit})

    @staticmethod
    def create(payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("POST", "/pedidos/", json=payload)

    @staticmethod
    def get(pedido_id: int) -> dict[str, Any]:
        return APIClient.request("GET", f"/pedidos/{pedido_id}")

    @staticmethod
    def update(pedido_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("PUT", f"/pedidos/{pedido_id}", json=payload)

    @staticmethod
    def delete(pedido_id: int) -> dict[str, Any]:
        return APIClient.request("DELETE", f"/pedidos/{pedido_id}")

    @staticmethod
    def list_by_cliente(cliente_id: int) -> list[dict[str, Any]]:
        return APIClient.request("GET", f"/pedidos/cliente/{cliente_id}")

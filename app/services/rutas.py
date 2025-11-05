from __future__ import annotations

from typing import Any

from .base import APIClient


class RutaService:
    @staticmethod
    def list(skip: int = 0, limit: int = 100, tipo: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if tipo:
            params["tipo"] = tipo
        return APIClient.request("GET", "/rutas/", params=params)

    @staticmethod
    def create(payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("POST", "/rutas/", json=payload)

    @staticmethod
    def get(ruta_id: int) -> dict[str, Any]:
        return APIClient.request("GET", f"/rutas/{ruta_id}")

    @staticmethod
    def update(ruta_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("PUT", f"/rutas/{ruta_id}", json=payload)

    @staticmethod
    def delete(ruta_id: int) -> dict[str, Any]:
        return APIClient.request("DELETE", f"/rutas/{ruta_id}")

    @staticmethod
    def add_cliente(ruta_id: int, cliente_id: int, orden: int) -> dict[str, Any]:
        return APIClient.request(
            "POST",
            f"/rutas/{ruta_id}/clientes/{cliente_id}",
            json={"orden": orden},
        )

    @staticmethod
    def remove_cliente(ruta_cliente_id: int) -> dict[str, Any]:
        return APIClient.request("DELETE", f"/rutas/clientes/{ruta_cliente_id}")

    @staticmethod
    def assign_usuario(ruta_id: int, usuario_id: int) -> dict[str, Any]:
        return APIClient.request("POST", f"/rutas/{ruta_id}/asignar/{usuario_id}")

    @staticmethod
    def get_activas() -> list[dict[str, Any]]:
        return APIClient.request("GET", "/rutas/activas")

    @staticmethod
    def get_optimizada(ruta_id: int) -> dict[str, Any]:
        return APIClient.request("GET", f"/rutas/{ruta_id}/optimizada")

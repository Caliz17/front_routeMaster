from __future__ import annotations

from typing import Any

from .base import APIClient


class DashboardService:
    @staticmethod
    def resumen() -> dict[str, Any]:
        return APIClient.request("GET", "/dashboard/resumen")

    @staticmethod
    def metricas_ventas() -> dict[str, Any]:
        return APIClient.request("GET", "/dashboard/metricas-ventas")

    @staticmethod
    def productos_populares() -> list[dict[str, Any]]:
        return APIClient.request("GET", "/dashboard/productos-populares")

    @staticmethod
    def pedidos_pendientes() -> list[dict[str, Any]]:
        return APIClient.request("GET", "/dashboard/pedidos-pendientes")

    @staticmethod
    def rutas_activas() -> list[dict[str, Any]]:
        return APIClient.request("GET", "/dashboard/rutas-activas")

    @staticmethod
    def ventas_mensuales() -> list[dict[str, Any]]:
        return APIClient.request("GET", "/dashboard/ventas-mensuales")

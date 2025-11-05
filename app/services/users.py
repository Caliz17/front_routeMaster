from __future__ import annotations

from typing import Any

from .base import APIClient


class UserService:
    @staticmethod
    def get_current_user() -> dict[str, Any]:
        return APIClient.request("GET", "/users/me")

    @staticmethod
    def update_current_user(payload: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("PUT", "/users/me", json=payload)

    @staticmethod
    def list_users(skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        return APIClient.request("GET", "/admin/users", params={"skip": skip, "limit": limit})

    @staticmethod
    def list_roles(skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        return APIClient.request("GET", "/admin/roles", params={"skip": skip, "limit": limit})

    @staticmethod
    def update_role(user_id: int, role_id: int, is_active: bool | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"role_id": role_id}
        if is_active is not None:
            payload["is_active"] = is_active
        return APIClient.request(
            "PUT", f"/admin/users/{user_id}/role", json=payload
        )

    @staticmethod
    def get_permissions() -> list[str]:
        data = APIClient.request("GET", "/users/me/permissions")
        return data or []

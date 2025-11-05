from __future__ import annotations

from typing import Any

from flask import flash
from flask_login import login_user, logout_user

from ..models.user import User
from .base import APIClient


class AuthService:
    SESSION_CACHE: dict[str, User] = {}

    @classmethod
    def login(cls, email: str, password: str) -> User | None:
        payload = {"email": email, "password": password}
        data = APIClient.request("POST", "/auth/login", json=payload, include_auth=False)
        if not data:
            return None
        token = {
            "access_token": data.get("access_token"),
            "token_type": data.get("token_type"),
        }
        user_profile = APIClient.request(
            "GET", "/users/me", include_auth=False, token=token["access_token"]
        )
        permissions = APIClient.request(
            "GET", "/users/me/permissions", include_auth=False, token=token["access_token"]
        )
        if user_profile is None:
            return None
        user_profile["permissions"] = permissions or []
        user = User.from_api_response(user_profile, token)
        login_user(user)
        flash(data.get("message", "Inicio de sesión exitoso"), "success")
        return user

    @classmethod
    def logout(cls) -> None:
        from flask_login import current_user

        if current_user.is_authenticated:
            User.remove_session_user(str(current_user.id))
        logout_user()
        flash("Sesión finalizada", "info")

    @classmethod
    def register(cls, form_data: dict[str, Any]) -> dict[str, Any]:
        return APIClient.request("POST", "/auth/register", json=form_data, include_auth=False)

    @classmethod
    def refresh_token(cls, user: User) -> None:
        data = APIClient.request("POST", "/auth/refresh-token")
        user.access_token = data.get("access_token")
        user.token_type = data.get("token_type")

    @staticmethod
    def get_session_user(user_id: str) -> User | None:
        return User.get_session_user(user_id)

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

from flask_login import UserMixin


def _default_permissions() -> set[str]:
    return set()


@dataclass
class User(UserMixin):
    id: int
    username: str
    email: str
    role: dict[str, Any] | None = None
    permissions: set[str] = field(default_factory=_default_permissions)
    access_token: str | None = None
    token_type: str | None = None

    _session_users: ClassVar[dict[str, "User"]] = {}

    @classmethod
    def from_api_response(cls, data: dict[str, Any], token: dict[str, Any] | None = None) -> "User":
        role = data.get("role") if data else None
        permissions = set(data.get("permissions", [])) if data else set()
        user = cls(
            id=data.get("id") if data else 0,
            username=data.get("username") or data.get("email"),
            email=data.get("email"),
            role=role,
            permissions=permissions,
            access_token=token.get("access_token") if token else None,
            token_type=token.get("token_type") if token else None,
        )
        user._session_users[str(user.id)] = user
        return user

    @classmethod
    def get_session_user(cls, user_id: str) -> "User" | None:
        return cls._session_users.get(str(user_id))

    @classmethod
    def remove_session_user(cls, user_id: str) -> None:
        cls._session_users.pop(str(user_id), None)

    @property
    def is_admin(self) -> bool:
        return bool(self.role and self.role.get("name") == "admin")

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

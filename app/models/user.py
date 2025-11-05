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
        # Debug completo de la respuesta
        print("=" * 50)
        print("FULL API RESPONSE DATA:")
        print(data)
        print("=" * 50)
        
        role = data.get("role") if data else None
        
        # Verifica la estructura real de los permisos
        permissions_data = data.get("permissions")
        print(f"Raw permissions data: {permissions_data}")
        print(f"Type of permissions data: {type(permissions_data)}")
        
        if permissions_data is None:
            print("WARNING: No 'permissions' key found in API response")
            permissions = set()
        elif isinstance(permissions_data, list):
            permissions = set(permissions_data)
        elif isinstance(permissions_data, str):
            permissions = {permissions_data}
        else:
            print(f"WARNING: Unexpected permissions type: {type(permissions_data)}")
            permissions = set()
        
        print(f"Final permissions set: {permissions}")
        
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
        print(f"Checking permission for user {self.id}: {permission}")
        print(f"User permissions: {self.permissions}")
        print(f"Is admin: {self.is_admin}")
        print(f"Role: {self.role}")
        
        # Si el usuario tiene rol de admin, otorga todos los permisos
        if self.is_admin:
            print("User is admin, granting all permissions")
            return True
        
        # Verifica si el permiso está directamente en los permisos del usuario
        has_perm = permission in self.permissions
        print(f"Permission {permission} in permissions: {has_perm}")
        
        return has_perm

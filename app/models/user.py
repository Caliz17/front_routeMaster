from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar
import requests
from flask import current_app
from flask_login import UserMixin


def _default_permissions() -> set[str]:
    return set()


@dataclass
class User(UserMixin):
    id: int
    username: str
    email: str
    role: str | dict[str, Any] | None = None  # ✅ Puede ser string o dict
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
        
        # ✅ MANEJO MEJORADO DEL ROL (puede ser string o dict)
        role_data = data.get("role")
        print(f"Raw role data: {role_data}, type: {type(role_data)}")
        
        # Si el rol es un string, lo convertimos a un formato consistente
        if isinstance(role_data, str):
            role_name = role_data
        elif isinstance(role_data, dict):
            role_name = role_data.get("name")
        else:
            role_name = None
        
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
            role=role_data,  # ✅ Guardamos el rol tal como viene
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
    def role_name(self) -> str:
        """
        Obtener el nombre del rol de forma segura
        """
        if isinstance(self.role, str):
            return self.role
        elif isinstance(self.role, dict):
            return self.role.get("name", "")
        return ""

    @property
    def is_admin(self) -> bool:
        """
        Verificar si el usuario es administrador de forma segura
        """
        role_name = self.role_name.lower()
        return role_name in ["admin", "administrador"]

    def _fetch_current_permissions(self) -> set[str]:
        """
        Obtener los permisos actualizados del usuario desde la API
        """
        if not self.access_token:
            print("No access token available")
            return set()

        try:
            # Configura la URL base de tu API
            api_base_url = current_app.config.get('API_BASE_URL', 'http://localhost:8000')
            url = f"{api_base_url}/users/me/permissions"
            
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            print(f"Fetching permissions from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"Permissions API response: {data}")
                
                # Actualizar los permisos locales
                permissions_list = data.get('permissions', [])
                self.permissions = set(permissions_list)
                
                # ✅ MANEJO MEJORADO: Actualizar el rol (puede ser string)
                if 'role' in data:
                    self.role = data['role']
                
                print(f"Updated permissions: {self.permissions}")
                print(f"Updated role: {self.role} (type: {type(self.role)})")
                return self.permissions
            else:
                print(f"Error fetching permissions: {response.status_code} - {response.text}")
                return set()
                
        except requests.exceptions.RequestException as e:
            print(f"Request error fetching permissions: {e}")
            return set()
        except Exception as e:
            print(f"Unexpected error fetching permissions: {e}")
            return set()

    def has_permission(self, permission: str, use_cache: bool = True) -> bool:
        """
        Verificar si el usuario tiene un permiso específico
        
        Args:
            permission: El nombre del permiso a verificar
            use_cache: Si es True, usa los permisos en caché. Si es False, hace una petición fresh a la API
        """
        print(f"Checking permission for user {self.id}: {permission}")
        print(f"Current cached permissions: {self.permissions}")
        print(f"Is admin: {self.is_admin}")
        print(f"Role: {self.role} (type: {type(self.role)})")
        print(f"Role name: {self.role_name}")
        
        # Si el usuario tiene rol de admin, otorga todos los permisos
        if self.is_admin:
            print("User is admin, granting all permissions")
            return True
        
        # Si no queremos usar caché o no tenemos permisos cacheados, hacer petición fresh
        if not use_cache or not self.permissions:
            print("Fetching fresh permissions from API...")
            fresh_permissions = self._fetch_current_permissions()
            if fresh_permissions:
                self.permissions = fresh_permissions
                print(f"Fresh permissions loaded: {self.permissions}")
        
        # Verifica si el permiso está en los permisos del usuario
        has_perm = permission in self.permissions
        print(f"Permission {permission} in permissions: {has_perm}")
        
        return has_perm

    def refresh_permissions(self) -> bool:
        """
        Forzar la actualización de permisos desde la API
        Returns True si se actualizaron correctamente
        """
        print("Forcing permissions refresh...")
        fresh_permissions = self._fetch_current_permissions()
        if fresh_permissions:
            self.permissions = fresh_permissions
            print(f"Permissions refreshed successfully: {self.permissions}")
            return True
        return False
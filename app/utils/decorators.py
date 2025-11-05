from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar

from flask import flash, redirect, url_for
from flask_login import current_user, login_required

F = TypeVar("F", bound=Callable)


def permission_required(permission: str) -> Callable[[F], F]:
    def decorator(view_func: F) -> F:
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_required(view_func)(*args, **kwargs)
            if not current_user.has_permission(permission):
                flash("No tienes permiso para realizar esta acción", "warning")
                return redirect(url_for("dashboard.index"))
            return view_func(*args, **kwargs)

        return wrapped  # type: ignore[return-value]

    return decorator

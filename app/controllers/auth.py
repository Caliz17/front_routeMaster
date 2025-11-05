from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..forms.auth_forms import LoginForm, RegisterForm
from ..services.auth import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = LoginForm()
    if form.validate_on_submit():
        AuthService.login(form.email.data, form.password.data)
        return redirect(request.args.get("next") or url_for("dashboard.index"))
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        AuthService.register(
            {
                "username": form.username.data,
                "email": form.email.data,
                "password": form.password.data,
                "role_id": int(form.role_id.data),
            }
        )
        flash("Usuario registrado correctamente. Inicia sesión para continuar.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    AuthService.logout()
    return redirect(url_for("auth.login"))

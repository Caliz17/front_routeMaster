from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..forms.user_forms import UserProfileForm, UserRoleForm
from ..services.users import UserService
from ..utils.decorators import permission_required


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/me", methods=["GET", "POST"])
@login_required
def profile():
    user_data = UserService.get_current_user()
    form = UserProfileForm(data=user_data)
    if form.validate_on_submit():
        payload = {
            "username": form.username.data,
            "email": form.email.data,
            "telefono": form.telefono.data,
        }
        UserService.update_current_user(payload)
        return redirect(url_for("users.profile"))
    return render_template("users/profile.html", form=form)


@users_bp.route("/manage", methods=["GET", "POST"])
@login_required
@permission_required("users.manage")
def manage():
    form = UserRoleForm()
    users = UserService.list_users()
    roles = UserService.list_roles()
    form.user_id.choices = [(user["id"], f"{user['username']} ({user['email']})") for user in users]
    form.role_id.choices = [(role["id"], role["name"]) for role in roles]

    if request.method == "POST" and form.validate_on_submit():
        UserService.update_role(
            form.user_id.data, form.role_id.data, form.is_active.data
        )
        return redirect(url_for("users.manage"))

    return render_template(
        "users/manage.html",
        form=form,
        users=users,
        roles=roles,
        current_user=current_user,
    )

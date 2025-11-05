from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserProfileForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email()])
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=20)])
    submit = SubmitField("Actualizar perfil")


class UserRoleForm(FlaskForm):
    user_id = SelectField("Usuario", coerce=int, validators=[DataRequired()])
    role_id = SelectField("Rol", coerce=int, validators=[DataRequired()])
    is_active = BooleanField("Activo")
    submit = SubmitField("Actualizar rol")

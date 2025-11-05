from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Length, Optional


class ClienteForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    nit = StringField("NIT", validators=[DataRequired(), Length(max=20)])
    direccion = StringField("Dirección", validators=[Optional(), Length(max=200)])
    telefono = TelField("Teléfono", validators=[Optional(), Length(max=20)])
    contacto = StringField("Contacto", validators=[Optional(), Length(max=100)])
    latitud = DecimalField("Latitud", validators=[Optional()])
    longitud = DecimalField("Longitud", validators=[Optional()])
    direccion_geocodificada = StringField("Dirección geocodificada", validators=[Optional(), Length(max=250)])
    estado = BooleanField("Activo", default=True)
    submit = SubmitField("Guardar cliente")

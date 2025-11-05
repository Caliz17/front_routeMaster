from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class RutaClienteForm(FlaskForm):
    cliente_id = SelectField("Cliente", coerce=int, validators=[DataRequired()])
    orden = IntegerField("Orden", validators=[DataRequired(), NumberRange(min=1)])


class RutaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=120)])
    tipo = SelectField(
        "Tipo",
        choices=[("venta", "Venta"), ("entrega", "Entrega"), ("mixta", "Mixta")],
        validators=[DataRequired()],
    )
    creada_por_id = IntegerField("ID creador", validators=[DataRequired()])
    clientes = FieldList(FormField(RutaClienteForm), min_entries=1, max_entries=20)
    submit = SubmitField("Guardar ruta")

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    sku = StringField("SKU", validators=[DataRequired(), Length(max=50)])
    descripcion = TextAreaField("Descripción", validators=[Length(max=500)])
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    estado = BooleanField("Activo", default=True)
    submit = SubmitField("Guardar producto")

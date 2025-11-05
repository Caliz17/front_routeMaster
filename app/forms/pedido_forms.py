from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import DateField, FieldList, FormField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class PedidoDetalleForm(FlaskForm):
    producto_id = SelectField("Producto", coerce=int, validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1)])
    precio_unitario = IntegerField("Precio unitario", validators=[DataRequired(), NumberRange(min=0)])


class PedidoForm(FlaskForm):
    cliente_id = SelectField("Cliente", coerce=int, validators=[DataRequired()])
    vendedor_id = SelectField("Vendedor", coerce=int, validators=[DataRequired()])
    fecha_pedido = DateField("Fecha del pedido", validators=[DataRequired()])
    estado = SelectField(
        "Estado",
        choices=[
            ("pendiente_entrega", "Pendiente de entrega"),
            ("en_ruta", "En ruta"),
            ("entregado", "Entregado"),
            ("cancelado", "Cancelado"),
        ],
        validators=[DataRequired()],
    )
    detalles = FieldList(FormField(PedidoDetalleForm), min_entries=1, max_entries=10)
    submit = SubmitField("Guardar pedido")


class PedidoEstadoForm(FlaskForm):
    estado = SelectField(
        "Estado",
        choices=[
            ("pendiente_entrega", "Pendiente de entrega"),
            ("en_ruta", "En ruta"),
            ("entregado", "Entregado"),
            ("cancelado", "Cancelado"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Actualizar estado")

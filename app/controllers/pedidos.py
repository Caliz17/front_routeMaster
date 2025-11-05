from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from ..forms.pedido_forms import PedidoEstadoForm, PedidoForm
from ..services.clientes import ClienteService
from ..services.pedidos import PedidoService
from ..services.productos import ProductoService
from ..services.users import UserService
from ..utils.decorators import permission_required


pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")


@pedidos_bp.route("/", methods=["GET"])
@login_required
def list_view():
    pedidos = PedidoService.list()
    clientes = {cliente["id"]: cliente for cliente in ClienteService.list()}
    usuarios = {user["id"]: user for user in UserService.list_users()}
    return render_template(
        "pedidos/list.html",
        pedidos=pedidos,
        clientes=clientes,
        usuarios=usuarios,
    )


@pedidos_bp.route("/crear", methods=["GET", "POST"])
@login_required
@permission_required("pedidos.create")
def create():
    form = PedidoForm()
    clientes = ClienteService.list()
    usuarios = UserService.list_users()
    productos = ProductoService.list()
    form.cliente_id.choices = [(cliente["id"], cliente["nombre"]) for cliente in clientes]
    form.vendedor_id.choices = [(user["id"], user["username"]) for user in usuarios]
    for detalle in form.detalles:
        detalle.producto_id.choices = [(prod["id"], prod["nombre"]) for prod in productos]

    if form.validate_on_submit():
        payload = {
            "cliente_id": form.cliente_id.data,
            "vendedor_id": form.vendedor_id.data,
            "fecha_pedido": form.fecha_pedido.data.isoformat(),
            "estado": form.estado.data,
            "detalles": [
                {
                    "producto_id": detalle.producto_id.data,
                    "cantidad": detalle.cantidad.data,
                    "precio_unitario": detalle.precio_unitario.data,
                }
                for detalle in form.detalles
            ],
        }
        PedidoService.create(payload)
        return redirect(url_for("pedidos.list_view"))

    return render_template(
        "pedidos/form.html",
        form=form,
        title="Crear pedido",
        clientes=clientes,
        usuarios=usuarios,
    )


@pedidos_bp.route("/<int:pedido_id>/estado", methods=["GET", "POST"])
@login_required
@permission_required("pedidos.update")
def update_estado(pedido_id: int):
    pedido = PedidoService.get(pedido_id)
    form = PedidoEstadoForm(data={"estado": pedido.get("estado")})
    if form.validate_on_submit():
        PedidoService.update(pedido_id, {"estado": form.estado.data})
        return redirect(url_for("pedidos.list_view"))
    return render_template("pedidos/estado.html", form=form, pedido=pedido)


@pedidos_bp.route("/<int:pedido_id>/eliminar", methods=["POST"])
@login_required
@permission_required("pedidos.delete")
def delete(pedido_id: int):
    PedidoService.delete(pedido_id)
    return redirect(url_for("pedidos.list_view"))

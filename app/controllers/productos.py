from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from ..forms.producto_forms import ProductoForm
from ..services.productos import ProductoService
from ..utils.decorators import permission_required


productos_bp = Blueprint("productos", __name__, url_prefix="/productos")


@productos_bp.route("/", methods=["GET"])
@login_required
def list_view():
    productos = ProductoService.list()
    return render_template("productos/list.html", productos=productos)


@productos_bp.route("/crear", methods=["GET", "POST"])
@login_required
@permission_required("productos.create")
def create():
    form = ProductoForm()
    if form.validate_on_submit():
        payload = {
            "nombre": form.nombre.data,
            "sku": form.sku.data,
            "descripcion": form.descripcion.data,
            "precio": float(form.precio.data or 0),
            "stock": form.stock.data,
            "estado": form.estado.data,
        }
        ProductoService.create(payload)
        return redirect(url_for("productos.list_view"))
    return render_template("productos/form.html", form=form, title="Crear producto")


@productos_bp.route("/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
@permission_required("productos.update")
def edit(producto_id: int):
    producto = ProductoService.get(producto_id)
    form = ProductoForm(data=producto)
    if form.validate_on_submit():
        payload = {
            "nombre": form.nombre.data,
            "sku": form.sku.data,
            "descripcion": form.descripcion.data,
            "precio": float(form.precio.data or 0),
            "stock": form.stock.data,
            "estado": form.estado.data,
        }
        ProductoService.update(producto_id, payload)
        return redirect(url_for("productos.list_view"))
    return render_template("productos/form.html", form=form, title="Editar producto")


@productos_bp.route("/<int:producto_id>/eliminar", methods=["POST"])
@login_required
@permission_required("productos.delete")
def delete(producto_id: int):
    ProductoService.delete(producto_id)
    return redirect(url_for("productos.list_view"))

from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from ..forms.cliente_forms import ClienteForm
from ..services.clientes import ClienteService
from ..utils.decorators import permission_required
from ..utils.helpers import clean_payload


clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@clientes_bp.route("/", methods=["GET"])
@login_required
def list_view():
    clientes = ClienteService.list()
    return render_template("clientes/list.html", clientes=clientes)


@clientes_bp.route("/crear", methods=["GET", "POST"])
@login_required
@permission_required("clientes.create")
def create():
    form = ClienteForm()
    if form.validate_on_submit():
        payload = clean_payload({
            "nombre": form.nombre.data,
            "nit": form.nit.data,
            "direccion": form.direccion.data,
            "telefono": form.telefono.data,
            "contacto": form.contacto.data,
            "latitud": float(form.latitud.data) if form.latitud.data is not None else None,
            "longitud": float(form.longitud.data) if form.longitud.data is not None else None,
            "direccion_geocodificada": form.direccion_geocodificada.data,
        })
        ClienteService.create(payload)
        return redirect(url_for("clientes.list_view"))
    return render_template("clientes/form.html", form=form, title="Crear cliente")


@clientes_bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
@login_required
@permission_required("clientes.update")
def edit(cliente_id: int):
    cliente = ClienteService.get(cliente_id)
    form = ClienteForm(data=cliente)
    if form.validate_on_submit():
        payload = clean_payload({
            "nombre": form.nombre.data,
            "nit": form.nit.data,
            "direccion": form.direccion.data,
            "telefono": form.telefono.data,
            "contacto": form.contacto.data,
            "latitud": float(form.latitud.data) if form.latitud.data is not None else None,
            "longitud": float(form.longitud.data) if form.longitud.data is not None else None,
            "direccion_geocodificada": form.direccion_geocodificada.data,
            "estado": form.estado.data,
        })
        ClienteService.update(cliente_id, payload)
        return redirect(url_for("clientes.list_view"))
    return render_template("clientes/form.html", form=form, title="Editar cliente")


@clientes_bp.route("/<int:cliente_id>/eliminar", methods=["POST"])
@login_required
@permission_required("clientes.delete")
def delete(cliente_id: int):
    ClienteService.delete(cliente_id)
    return redirect(url_for("clientes.list_view"))

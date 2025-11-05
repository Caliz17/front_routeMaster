from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from ..forms.ruta_forms import RutaForm
from ..services.clientes import ClienteService
from ..services.rutas import RutaService
from ..services.users import UserService
from ..utils.decorators import permission_required


rutas_bp = Blueprint("rutas", __name__, url_prefix="/rutas")


@rutas_bp.route("/", methods=["GET"])
@login_required
def list_view():
    rutas = RutaService.list()
    usuarios = {user["id"]: user for user in UserService.list_users()}
    return render_template("rutas/list.html", rutas=rutas, usuarios=usuarios)


@rutas_bp.route("/crear", methods=["GET", "POST"])
@login_required
@permission_required("rutas.create")
def create():
    form = RutaForm()
    clientes = ClienteService.list()
    form.tipo.choices = [("venta", "Venta"), ("entrega", "Entrega"), ("mixta", "Mixta")]
    for subform in form.clientes:
        subform.cliente_id.choices = [(cliente["id"], cliente["nombre"]) for cliente in clientes]

    if form.validate_on_submit():
        payload = {
            "nombre": form.nombre.data,
            "tipo": form.tipo.data,
            "creada_por_id": form.creada_por_id.data,
            "clientes": [
                {"cliente_id": cliente_form.cliente_id.data, "orden": cliente_form.orden.data}
                for cliente_form in form.clientes
            ],
        }
        RutaService.create(payload)
        return redirect(url_for("rutas.list_view"))

    return render_template("rutas/form.html", form=form, title="Crear ruta", clientes=clientes)


@rutas_bp.route("/<int:ruta_id>/editar", methods=["GET", "POST"])
@login_required
@permission_required("rutas.update")
def edit(ruta_id: int):
    ruta = RutaService.get(ruta_id)
    clientes = ClienteService.list()
    form = RutaForm()
    while len(form.clientes) < max(1, len(ruta.get("rutas_clientes", []))):
        form.clientes.append_entry()
    if request.method == "GET":
        form.nombre.data = ruta.get("nombre")
        form.tipo.data = ruta.get("tipo")
        form.creada_por_id.data = ruta.get("creada_por_id")
        for entry, cliente_data in zip(form.clientes, ruta.get("rutas_clientes", [])):
            entry.cliente_id.data = cliente_data.get("cliente_id")
            entry.orden.data = cliente_data.get("orden")
    for subform in form.clientes:
        subform.cliente_id.choices = [(cliente["id"], cliente["nombre"]) for cliente in clientes]
    if form.validate_on_submit():
        payload = {
            "nombre": form.nombre.data,
            "tipo": form.tipo.data,
            "creada_por_id": form.creada_por_id.data,
            "clientes": [
                {"cliente_id": cliente_form.cliente_id.data, "orden": cliente_form.orden.data}
                for cliente_form in form.clientes
            ],
        }
        RutaService.update(ruta_id, payload)
        return redirect(url_for("rutas.list_view"))

    return render_template("rutas/form.html", form=form, title="Editar ruta", clientes=clientes)


@rutas_bp.route("/<int:ruta_id>/eliminar", methods=["POST"])
@login_required
@permission_required("rutas.delete")
def delete(ruta_id: int):
    RutaService.delete(ruta_id)
    return redirect(url_for("rutas.list_view"))


@rutas_bp.route("/<int:ruta_id>/optimizada", methods=["GET"])
@login_required
def optimizada(ruta_id: int):
    ruta = RutaService.get(ruta_id)
    optimizada = RutaService.get_optimizada(ruta_id)
    return render_template("rutas/optimizada.html", ruta=ruta, optimizada=optimizada)

from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import login_required

from ..services.dashboard import DashboardService


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="")


@dashboard_bp.route("/")
@login_required
def index():
    resumen = DashboardService.resumen() or {}
    metricas = DashboardService.metricas_ventas() or {}
    productos_populares = DashboardService.productos_populares() or []
    pedidos_pendientes = DashboardService.pedidos_pendientes() or []
    rutas_activas = DashboardService.rutas_activas() or []
    ventas_mensuales = DashboardService.ventas_mensuales() or []

    return render_template(
        "dashboard/index.html",
        resumen=resumen,
        metricas=metricas,
        productos_populares=productos_populares,
        pedidos_pendientes=pedidos_pendientes,
        rutas_activas=rutas_activas,
        ventas_mensuales=ventas_mensuales,
    )

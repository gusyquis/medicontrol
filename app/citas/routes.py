from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Cita, Medico, Paciente

bp_citas = Blueprint("citas", __name__, template_folder="templates")


def _datos_formulario():
    return dict(
        medicos=Medico.query.order_by(Medico.nombre).all(),
        pacientes=Paciente.query.order_by(Paciente.nombre).all(),
    )


@bp_citas.route("/")
def lista():
    citas = Cita.query.order_by(Cita.fecha, Cita.hora).all()
    return render_template("citas/lista.html", citas=citas)


@bp_citas.route("/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        cita = Cita(
            fecha=datetime.strptime(request.form["fecha"], "%Y-%m-%d").date(),
            hora=datetime.strptime(request.form["hora"], "%H:%M").time(),
            medico_id=int(request.form["medico_id"]),
            paciente_id=int(request.form["paciente_id"]),
        )
        db.session.add(cita)
        db.session.commit()
        flash("Cita registrada correctamente.", "success")
        return redirect(url_for("citas.lista"))
    return render_template("citas/formulario.html", cita=None, **_datos_formulario())


@bp_citas.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    cita = db.get_or_404(Cita, id)
    if request.method == "POST":
        cita.fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        cita.hora = datetime.strptime(request.form["hora"], "%H:%M").time()
        cita.medico_id = int(request.form["medico_id"])
        cita.paciente_id = int(request.form["paciente_id"])
        db.session.commit()
        flash("Cita actualizada correctamente.", "success")
        return redirect(url_for("citas.lista"))
    return render_template("citas/formulario.html", cita=cita, **_datos_formulario())


@bp_citas.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    cita = db.get_or_404(Cita, id)
    db.session.delete(cita)
    db.session.commit()
    flash("Cita eliminada.", "success")
    return redirect(url_for("citas.lista"))
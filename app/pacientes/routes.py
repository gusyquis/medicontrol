from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Paciente

bp_pacientes = Blueprint("pacientes", __name__, template_folder="templates")


@bp_pacientes.route("/")
def lista():
    pacientes = Paciente.query.order_by(Paciente.id).all()
    return render_template("pacientes/lista.html", pacientes=pacientes)


@bp_pacientes.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        paciente = Paciente(
            nombre=request.form["nombre"].strip(),
            telefono=request.form["telefono"].strip(),
        )
        db.session.add(paciente)
        db.session.commit()
        flash("Paciente registrado correctamente.", "success")
        return redirect(url_for("pacientes.lista"))
    return render_template("pacientes/formulario.html", paciente=None)


@bp_pacientes.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    paciente = db.get_or_404(Paciente, id)
    if request.method == "POST":
        paciente.nombre = request.form["nombre"].strip()
        paciente.telefono = request.form["telefono"].strip()
        db.session.commit()
        flash("Paciente actualizado correctamente.", "success")
        return redirect(url_for("pacientes.lista"))
    return render_template("pacientes/formulario.html", paciente=paciente)


@bp_pacientes.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    paciente = db.get_or_404(Paciente, id)
    if paciente.citas:
        flash("No se puede eliminar: el paciente tiene citas registradas.", "danger")
    else:
        db.session.delete(paciente)
        db.session.commit()
        flash("Paciente eliminado.", "success")
    return redirect(url_for("pacientes.lista"))
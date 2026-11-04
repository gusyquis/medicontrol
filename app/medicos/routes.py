from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Medico

bp_medicos = Blueprint("medicos", __name__, template_folder="templates")


@bp_medicos.route("/")
def lista():
    medicos = Medico.query.order_by(Medico.id).all()
    return render_template("medicos/lista.html", medicos=medicos)


@bp_medicos.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        medico = Medico(
            nombre=request.form["nombre"].strip(),
            especialidad=request.form["especialidad"].strip(),
        )
        db.session.add(medico)
        db.session.commit()
        flash("Medico registrado correctamente.", "success")
        return redirect(url_for("medicos.lista"))
    return render_template("medicos/formulario.html", medico=None)


@bp_medicos.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    medico = db.get_or_404(Medico, id)
    if request.method == "POST":
        medico.nombre = request.form["nombre"].strip()
        medico.especialidad = request.form["especialidad"].strip()
        db.session.commit()
        flash("Medico actualizado correctamente.", "success")
        return redirect(url_for("medicos.lista"))
    return render_template("medicos/formulario.html", medico=medico)


@bp_medicos.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    medico = db.get_or_404(Medico, id)
    if medico.citas:
        flash("No se puede eliminar: el medico tiene citas registradas.", "danger")
    else:
        db.session.delete(medico)
        db.session.commit()
        flash("Medico eliminado.", "success")
    return redirect(url_for("medicos.lista"))
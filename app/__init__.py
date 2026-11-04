from flask import Flask, render_template
from config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)


    from app import models

   
    from app.medicos.routes import bp_medicos
    from app.pacientes.routes import bp_pacientes
    from app.citas.routes import bp_citas

    app.register_blueprint(bp_medicos, url_prefix="/medicos")
    app.register_blueprint(bp_pacientes, url_prefix="/pacientes")
    app.register_blueprint(bp_citas, url_prefix="/citas")

   
    from app.seed import registrar_comandos
    registrar_comandos(app)

    @app.route("/")
    def inicio():
        return render_template(
            "inicio.html",
            total_medicos=models.Medico.query.count(),
            total_pacientes=models.Paciente.query.count(),
            total_citas=models.Cita.query.count(),
        )

    return app
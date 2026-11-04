from datetime import date, time
from app.extensions import db
from app.models import Medico, Paciente, Cita


def registrar_comandos(app):
    @app.cli.command("sembrar")
    def sembrar():
        """Carga datos de prueba en las tablas."""
        if Medico.query.count() > 0:
            print("La base ya tiene datos. No se cargo nada.")
            return

        medicos = [
            Medico(nombre="Dra. Ana Torrico", especialidad="Cardiologia"),
            Medico(nombre="Dr. Luis Mamani", especialidad="Pediatria"),
            Medico(nombre="Dra. Rosa Quispe", especialidad="Dermatologia"),
        ]
        pacientes = [
            Paciente(nombre="Carlos Rojas", telefono="70011122"),
            Paciente(nombre="Laura Flores", telefono="70033344"),
            Paciente(nombre="Diego Condori", telefono="70055566"),
            Paciente(nombre="Maria Apaza", telefono="70077788"),
        ]
        db.session.add_all(medicos + pacientes)
        db.session.flush() 

        db.session.add_all([
            Cita(fecha=date(2026, 11, 10), hora=time(8, 30), medico=medicos[0], paciente=pacientes[0]),
            Cita(fecha=date(2026, 11, 10), hora=time(9, 15), medico=medicos[1], paciente=pacientes[1]),
            Cita(fecha=date(2026, 11, 11), hora=time(10, 0), medico=medicos[0], paciente=pacientes[2]),
            Cita(fecha=date(2026, 11, 12), hora=time(15, 45), medico=medicos[2], paciente=pacientes[3]),
            Cita(fecha=date(2026, 11, 13), hora=time(11, 30), medico=medicos[1], paciente=pacientes[0]),
        ])
        db.session.commit()
        print("Datos de prueba cargados: 3 medicos, 4 pacientes y 5 citas.")
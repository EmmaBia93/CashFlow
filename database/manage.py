from database.models import Cajero,SesionCaja,BilleteSesion,Transferencias,init_db
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound

Session = init_db()

def get_session():
    return Session()


def crear_cajero(nombre, usuario, contrasena):
    session = get_session()
    try:
        contrasena_hash = generate_password_hash(contrasena)
        nuevo_cajero = Cajero(
            nombre=nombre,
            usuario=usuario,
            contrasena_hash=contrasena_hash
        )   
        session.add(nuevo_cajero)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()


def save_sesion(cajero_id:int,total_wisp:float,observaciones:str,transferencias:dict,billetes:dict):
    session = get_session()

    try:
        nueva_sesion = SesionCaja(
        cajero_id=cajero_id,
        fecha_cierre=datetime.now(),
        total_importe=total_wisp,
        observaciones=observaciones
        )

        session.add(nueva_sesion)
        session.flush()

        for transferencia in transferencias:
            nueva_transferencia = Transferencias(
                nombre_cliente=transferencia['nombre'],
                importe_transferencia=transferencia['importe'],
                sesion_id=nueva_sesion.id  # ID de la sesión de caja
                )
            session.add(nueva_transferencia)

        for billete in billetes:
            nuevo_billete_sesion = BilleteSesion(
                denominacion=billete['denominacion'],
                cantidad=billete['cantidad'],
                sesion_id=nueva_sesion.id  # ID de la sesión de caja
            )
            session.add(nuevo_billete_sesion)


        session.commit()
        return True
    except:
        return False
    finally:
        session.close()


def get_sesion(cajero,fecha):
        
        try:
            session = get_session()
            sesion_seleccionada = session.query(SesionCaja).join(Cajero).filter(
            Cajero.nombre == cajero,
            SesionCaja.fecha_cierre == fecha
            ).options(
            joinedload(SesionCaja.billetes),  # Cargar los billetes asociados
            joinedload(SesionCaja.transferencias)  # Cargar las transferencias asociadas
            ).first()


            billetes_dict = {billete.denominacion: billete.cantidad for billete in sesion_seleccionada.billetes}

            transferencias_lista = [
                {'nombre_cliente': transferencia.nombre_cliente, 'importe_transferencia': transferencia.importe_transferencia}
                for transferencia in sesion_seleccionada.transferencias
            ]

            return {
                'billetes': billetes_dict,
                'transferencias': transferencias_lista
            }
        except NoResultFound:
            return False
        except Exception as e:
            return False
        finally:
            session.close()


def get_last_sesions():
    try:
        session = get_session()
        sesiones = session.query(
        SesionCaja.fecha_cierre,
        Cajero.nombre
        ).join(Cajero, SesionCaja.cajero_id == Cajero.id).order_by(SesionCaja.fecha_cierre.desc()).limit(5).all()

        return sesiones
    except:
        return False
    finally:
        session.close()
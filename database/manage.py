from database.models import Cajero,SesionCaja,BilleteSesion,Transferencias,init_db
from bcrypt import hashpw,checkpw,gensalt
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

Session = init_db()

def get_session():
    return Session()


def crear_cajero(nombre, usuario, contrasena):
    session = get_session()
    try:
        # Verificar si el usuario ya existe
        cajero_existente = session.query(Cajero).filter_by(usuario=usuario).first()
        if cajero_existente:
            print(f"Error: El usuario '{usuario}' ya existe.")
            return False

        # Crear hash de la contraseña
        contrasena_hash = hashpw(contrasena.encode('utf-8'), gensalt())

        # Crear nuevo cajero
        nuevo_cajero = Cajero(nombre=nombre, usuario=usuario, contrasena_hash=contrasena_hash)

        # Agregar y confirmar los cambios en la base de datos
        session.add(nuevo_cajero)
        session.commit()
        return True
    except IntegrityError as e:
        session.rollback()
        print(f"Error de integridad: {e}")  # Registrar el error para depuración
        return False
    except Exception as e:
        session.rollback()
        print(f"Error al crear el cajero: {e}")  # Registrar el error para diagnóstico
        return False
    finally:
        session.close()

def get_cajero(nombre:str):
    session = get_session()
    try:
         cajero = session.query(Cajero).filter_by(usuario=nombre).first()
         if cajero:
             return cajero
    except:
        return None
    finally:
        session.close()


def verificar_credenciales(usuario, contrasena):
    session = get_session()
    cajero = session.query(Cajero).filter_by(usuario=usuario).first()
    if cajero and checkpw(contrasena.encode('utf-8'),cajero.contrasena_hash):
        return True
    else:
        return False 
    
def save_sesion(cajero_id:int,total_wisp:float,total_sesion:float,transferencias:list,billetes:list,observaciones:str=None):
    session = get_session()
    
    try:
        
        nueva_sesion = SesionCaja (cajero_id=cajero_id,total_wisphub=total_wisp,total_importe = total_sesion,observaciones=observaciones)
        
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
    except Exception as e:
        print(e)
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
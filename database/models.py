from sqlalchemy import create_engine, Column, Integer, String,ForeignKey,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from datetime import datetime

Base = declarative_base()

class Cajero(Base):
    __tablename__ = 'cajeros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    usuario = Column(String, unique=True, nullable=False)
    contrasena_hash = Column(String, nullable=False)
    sesiones = relationship('SesionCaja', backref='cajero')


class SesionCaja(Base):
    __tablename__ = 'sesion_caja'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cajero_id = Column(Integer, ForeignKey('cajeros.id', ondelete='CASCADE'), nullable=False)
    fecha_cierre = Column(DateTime, default=datetime.now)
    total_clientes = Column(Integer, nullable=False)
    total_importe = Column(Float, nullable=False)
    observaciones = Column(String, nullable=True)
    transferencias = relationship('ClienteTransferencia', backref='sesion')
    billetes = relationship('BilleteSesion', backref='sesion')


class ClienteTransferencia(Base):
    __tablename__ = 'clientes_transferencia'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cliente = Column(String, nullable=False)
    importe_transferencia = Column(Float, nullable=False)
    sesion_id = Column(Integer, ForeignKey('sesion_caja.id', ondelete='CASCADE'), nullable=False)


class BilleteSesion(Base):
    __tablename__ = 'billetes_sesion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    denominacion = Column(Integer, nullable=False)
    cantidad = Column(Integer, nullable=False)
    sesion_id = Column(Integer, ForeignKey('sesion_caja.id', ondelete='CASCADE'), nullable=False)





def init_db():
    engine = create_engine('sqlite:///database/database.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


    

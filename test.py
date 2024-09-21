def verificar_caja(importe_caja, importe_dinero):
    diferencia = importe_caja - importe_dinero
    
    # Mapeo de condiciones a mensajes
    mensajes = {
        0: "Caja correcta",
        -1: "Falta",
        1: "Sobra"
    }

    # Determinar el mensaje según la diferencia
    return mensajes[(diferencia > 0) - (diferencia < 0)]

# Ejemplo de uso
importe_caja = 1000  # Cambia estos valores según necesites
importe_dinero = 1000
resultado = verificar_caja(importe_caja, importe_dinero)
print(resultado)

import re

def validar_contrasena(contrasena, confirmacion):
    # Regex para validar la contraseña
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
    
    # Verificar que ambas contraseñas coincidan
    if contrasena != confirmacion:
        return "Las contraseñas no coinciden."

    # Verificar que la contraseña cumpla con los requisitos
    if not re.match(regex, contrasena):
        return "La contraseña no cumple con los requisitos."

    return "Contraseña válida."

# Ejemplo de uso
contrasena = "Emma1234#"
confirmacion = "Emma1234#"
resultado = validar_contrasena(contrasena, confirmacion)
print(resultado)

def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Debe ser un número entero.")

def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto and texto.replace(" ", "").isalpha():
            return texto
        print("Error: Solo letras permitidas y no puede estar vacío.")

def leer_no_vacio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Error: No puede estar vacío.")

def leer_correo(mensaje):
    while True:
        correo = input(mensaje).strip()
        if correo.count("@") == 1:
            usuario, dominio = correo.split("@")
            if "." in dominio and not dominio.startswith(".") and not dominio.endswith("."):
                return correo
        print("Error: Correo inválido. Formato: usuario@dominio.com")

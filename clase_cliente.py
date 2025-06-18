import sqlite3
from sqlite3 import Error
import lectura_datos
from lectura_datos import leer_entero
from lectura_datos import leer_texto
from lectura_datos import leer_no_vacio
from lectura_datos import leer_correo

#creacion y conexion con la bas ede datos
def conexionBD():
    try:
        # se crea repositorio fisico-objeto de conexcion a la base de datos 
        con=sqlite3.connect('basemibanco.db')
        print('la conexion fue exitosa')
        return con
    except Error:
        print(Error)

#cierre conexion

def cerrarDB(con):
    con.close()



    
def crearTablaClientes(con):
    #creamos el objeto para recorrer la base de datos
    cursor=con.cursor()
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes(
                                                noIdCliente INTEGER PRIMARY KEY,
                                                nombre TEXT NOT NULL,
                                                apellido TEXT NOT NULL,
                                                direccion TEXT,
                                                telefono TEXT,
                                                correo TEXT) ''')
    #aseguramos la persistencia con un commit
    con.commit()


def insertarCliente1(con, cliente):
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO Clientes VALUES (?, ?, ?, ?, ?, ?)", cliente)
        con.commit()
        print("Cliente creado correctamente.")
    #esta ecepcion me permite que si hay un cliente que escriba un id ya existente , no lo permita
    #y el programa no seje de funcionar, en cambio le anuncie al cliente que  el id ya existe
    except sqlite3.IntegrityError:
        print("Ya existe un cliente con ese ID.")

def insertarCliente(con, cliente):
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO Clientes VALUES (?, ?, ?, ?, ?, ?)", cliente)
        con.commit()
        print("Cliente creado correctamente. Para continuar debes adquirir un producto")
    #esta ecepcion me permite que si hay un cliente que escriba un id ya existente , no lo permita
    #y el programa no seje de funcionar, en cambio le anuncie al cliente que  el id ya existe
    except sqlite3.IntegrityError:
        print("Ya existe un cliente con ese ID.")


def leerCliente():
    noIdCliente = leer_entero("ID cliente (número): ")
    nombre = leer_texto("Nombre: ")
    apellido = leer_texto("Apellido: ")
    direccion = leer_no_vacio("Dirección: ")
    telefono = leer_entero("Teléfono (número): ")
    correo = leer_correo("Correo: ")
    return noIdCliente, nombre, apellido, direccion, str(telefono), correo


def actualizarDireccion(con):
    idCliente = input("ID del cliente: ")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Clientes WHERE noIdCliente=?", (idCliente,))
    cliente = cursor.fetchone()
    

def consultarInformacionCliente(con):
    idCliente = input("ID del cliente a consultar: ")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Clientes WHERE noIdCliente=?", (idCliente,))
    c = cursor.fetchone()
    if c:
        print(f"\nID: {c[0]}\nNombre: {c[1]} {c[2]}\nDirección: {c[3]}\nTeléfono: {c[4]}\nCorreo: {c[5]}")
    else:
        print("Cliente no encontrado.")

        

def menuClinetes(con):
#se vuelven a llamar las variables que permite salir con el fin
#de que si el usuario entra a la opcion y vuelve a salir
#pueda volver a entrar a la opcion

    salirClientes = False
    while not salirClientes:
        opPrincipal = input('''
                            MENU CLIENTES

                            1. Crear cliente
                            2. Actualizar dirección
                            3. Consultar información vigente de un cliente
                            4. Volver a  menú Principal

                            Seleccione un a opccion>>>: 

                            ''')
        if(opPrincipal == '1'):
            cliente = leerCliente()
            insertarCliente(con, cliente)
            
        elif (opPrincipal == '2'):
            actualizarDireccion(con)
        elif (opPrincipal == '3'):
            consultarInformacionCliente(con)
        elif (opPrincipal == '4'):
            salirClientes = True
        else:
            print("Elija opcion válida.")


def borrar_tabla(con):
    cursorObj=con.cursor()
    cad="DROP TABLE IF EXISTS CLIENTES"
    cursorObj.execute(cad)
    print("Tabla borrada exitosamente")
    
#micon=conexionBD()
#crearTablaClientes(micon)

#borrar_tabla(micon)

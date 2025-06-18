import sqlite3
from sqlite3 import Error
import lectura_datos
from lectura_datos import leer_entero
from lectura_datos import leer_texto
from lectura_datos import leer_no_vacio
from lectura_datos import leer_correo
from clase_productos import consultarProducto1


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
    print('conexion cerrada')



    
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


def leerProductoContratado1(con):
    cursor = con.cursor()
    print('Las opciones de productos que podemos ofrecer son')
    consultarProducto1(con)
    # Leer ID del producto
    
    idProducto = leer_entero("Número de producto a contratar: ")
    
    cursor.execute("SELECT tipoProducto, remuneracion FROM Productos WHERE noIdProducto=?", (idProducto,))
    row = cursor.fetchone()
    if not row:
        print(" Producto no encontrado.")
        return

    tipo = int(row[0])
    interes = float(row[1])
    tipoTexto = "CRÉDITO" if tipo == 1 else "AHORROS"
    print(f"Tipo de producto detectado: {tipoTexto}")

    # Leer ID del cliente y verificar existencia
    idCliente = input("ID del cliente: ")
    cursor.execute("SELECT * FROM Clientes WHERE noIdCliente=?", (idCliente,))
    cliente = cursor.fetchone()
    if not cliente:
        print(" Cliente no registrado. Debe crear el cliente primero.")
        return

    # Continuar con el registro según tipo
    try:
        if tipo == 1:
            capital = float(input("Capital inicial: "))
            plazo = int(input("Plazo en meses: "))
            fecha = concafecha()
            saldo = capital
            plazoPendiente = plazo
        else:
            capital=int(0)
            while capital<100000:
                
                print('el monto minimo inicial de ahorro es de 100000')
                capital = float(input("Monto inicial de ahorro: "))
            
            plazo = 0
            
            fecha = concafecha()
            saldo = capital
            plazoPendiente = 0
    except ValueError:
        print(" Error: valores inválidos en capital o plazo.")
        return

    # Insertar en base de datos y obtener ID generado
    cursor.execute('''
        INSERT INTO ProductosContratados
        (idProducto, idCliente, capitalInicial, plazoMeses, fechaEntrega, saldoCapital, sumatoriaInteresesPagados, plazoPendiente)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (idProducto, idCliente, capital, plazo, fecha, saldo, 0, plazoPendiente))
    con.commit()
    idCuenta = cursor.lastrowid

    print(" Producto contratado registrado correctamente.")
    print(f" Su número de cuenta u obligación es: {idCuenta}")




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
        leerProductoContratado1(con)
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
    nuevdirec = leer_no_vacio('Ingrese la nueva dirección: ')
    
    cursor = con.cursor()
    cad = "UPDATE Clientes SET direccion = ? WHERE noIdCliente = ?"
    cursor.execute(cad, (nuevdirec, idCliente))
    
    # Aseguramos la persistencia con un commit
    con.commit()
    

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
#cerrarDB(micon)    
#actualizarDireccion(micon)
#crearTablaClientes(micon)
#cliente1=leerCliente()
#insertarCliente(micon,cliente1)
#borrar_tabla(micon)

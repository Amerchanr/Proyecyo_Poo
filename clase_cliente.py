import sqlite3
from sqlite3 import Error
from lectura_datos import *
from clase_productos import *
from clase_ProdAdqu import *

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

## Cliente -----------------------------------------------------------------------------------------------------------------------------------

## Creacion de un formato que te pregunta la fecha
def concafecha():
    dia=input('ingrese el dia en formato DD')
    mes=input('ingrese el mes en formato MM')
    año=input('ingrese el año en formato AAAA')
    fechacon=(dia+'/'+mes+'/'+año)
    print(fechacon)
    return fechacon

# Toma el producto cliente y la funcion leerProductoContratado1 para verificar id

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



#inserta  lso espacion referente a cada clienmte en este caso son 6 espacios que se definen en las tablas
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

#Se dan definiciones sobre los datos del clientes 
def leerCliente():
    noIdCliente = leer_entero("ID cliente (número): ")
    nombre = leer_texto("Nombre: ")
    apellido = leer_texto("Apellido: ")
    direccion = leer_no_vacio("Dirección: ")
    telefono = leer_entero("Teléfono (número): ")
    correo = leer_correo("Correo: ")
    return noIdCliente, nombre, apellido, direccion, str(telefono), correo

# En caso de que el cliente quiera actualziar datos 
def actualizarDireccion(con):
    idCliente = input("ID del cliente: ")
    nuevdirec = leer_no_vacio('Ingrese la nueva dirección: ')
    
    cursor = con.cursor()
    cad = "UPDATE Clientes SET direccion = ? WHERE noIdCliente = ?"
    cursor.execute(cad, (nuevdirec, idCliente))
    
    # Aseguramos la persistencia con un commit
    con.commit()
    
#En funcion a la idea de que el cliente decida saber su informacion 
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

#No imolementado, pero es eleminiar dato y tabla
def borrar_tabla(con):
    cursorObj=con.cursor()
    cad="DROP TABLE IF EXISTS CLIENTES"
    cursorObj.execute(cad)
    print("Tabla borrada exitosamente")
    

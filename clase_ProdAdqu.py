import sqlite3
from sqlite3 import Error
import lectura_datos
from lectura_datos import leer_entero
from lectura_datos import leer_texto
from lectura_datos import leer_no_vacio
from lectura_datos import leer_correo
import clase_cliente
from clase_cliente import insertarCliente1
from clase_cliente import leerCliente


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


def crearTablaProducAdq(con):
    #creamos el objeto para recorrer la base de datos
    cursor=con.cursor()
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductosContratados(
                                                idCuentaCredito INTEGER PRIMARY KEY AUTOINCREMENT,
                                                idProducto INTEGER,
                                                idCliente INTEGER,
                                                capitalInicial REAL,
                                                plazoMeses INTEGER,
                                                fechaEntrega TEXT,
                                                saldoCapital REAL,
                                                sumatoriaInteresesPagados REAL DEFAULT 0,
                                                plazoPendiente INTEGER,
                                                FOREIGN KEY(idProducto) REFERENCES Productos(noIdProducto),
                                                FOREIGN KEY(idCliente) REFERENCES Clientes(noIdCliente))  ''')
    #aseguramos la persistencia con un commit
    con.commit()



        
def consultarProductosExistentes(con):
    NoIdProducto=leer_entero('ingrese el iD del producto adquirido')
    
    #creamos el objeto para recorrer la base de datos
    cursorObj=con.cursor()
    #CREAMOS LA CADENA CON EL SQL QUE QUEREMOS EJECUTAR
    cad='''SELECT idCuentaCredito,idProducto,idCliente,capitalInicial,plazoMeses,fechaEntrega,saldoCapital,sumatoriaInteresesPagados,
                plazoPendiente FROM PRODUCTOS WHERE idProducto='''+NoIdProducto
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursorObj.execute(cad)
    filas=cursorObj.fetchall()
    if filas==[]:
        print('el Id del producto consultado no existe')
    for row in filas:
        id1=row[0]
        tipo=row[2]
        nombre=row[1]
        remuneracion=row[3]
        print("NoIdProducto: ",id1,"\nNombreProducto: ",nombre,"\nTipoProducto: ",tipo,"\nRemuneracion: ",remuneracion)



def leerProductoContratado(con):
    cursor = con.cursor()

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
            fecha = input("Fecha de apertura (DD/MM/AAAA): ")
            saldo = capital
            plazoPendiente = plazo
        else:
            capital = float(input("Monto inicial de ahorro: "))
            plazo = 0
            fecha = input("Fecha de apertura (DD/MM/AAAA): ")
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

    
def insertarProductoContratado(con, datos):
    if datos:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO ProductosContratados
            (idProducto, idCliente, capitalInicial, plazoMeses, fechaEntrega, saldoCapital, sumatoriaInteresesPagados, plazoPendiente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', datos)
        con.commit()
        print("Producto contratado registrado correctamente.")

def MenuCrearProducto(con):
    salirProductosContratados = False
    while not salirProductosContratados:
        opPrincipal = input('''
                            MENU Aquirir un Producto

                            1. Ya soy cliente
                            2. No soy cliente
                            3. Volver a  menú Productos Adquiridos
                            

                            Seleccione un a opccion>>>: 

                            ''')
        if(opPrincipal == '1'):
            datos = leerProductoContratado(con)
            insertarProductoContratado(con, datos)
        elif (opPrincipal == '2'):
            cliente=leerCliente()
            insertarCliente1(con,cliente)
            datos = leerProductoContratado(con)
            insertarProductoContratado(con, datos)
        elif (opPrincipal == '3'):
            salirProductosContratados = True
        else:
            print("Opción no válida.")




def menuProductosContratados(con):
    salirProductosContratados = False
    while not salirProductosContratados:
        opPrincipal = input('''
                            MENU Productos Adquiridos 

                            1. Crear productos 
                            2. Consultar productos existentes
                            3. Volver a  menú Principal
                            

                            Seleccione un a opccion>>>: 

                            ''')
        if(opPrincipal == '1'):
            MenuCrearProducto(con)
        elif (opPrincipal == '2'):
            consultarProductosExistentes(con)

        elif (opPrincipal == '3'):
            salirProductosContratados = True
        else:
            print("Opción no válida.")


            
#micon=conexionBD()
#menuProductosContratados(micon)
            
